from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START, END

# =====================================================
# IMPORT AGENTS
# =====================================================

from app.agents.planner_agent import create_plan
from app.agents.financial_agent import get_financial_data
from app.agents.historical_agent import get_historical_returns
from app.agents.news_agent import get_news
from app.agents.ranking_agent import rank_company
from app.agents.decision_agent import get_decision
from app.agents.report_agent import generate_report


# =====================================================
# STATE
# =====================================================

class StockState(TypedDict):

    query: str
    period: str

    company: dict

    financial: dict
    historical: dict
    news: dict

    ranking: dict
    decision: dict
    report: dict


# =====================================================
# PLANNER
# =====================================================

def planner_node(state):

    print("\nRunning Planner Agent...")

    plan = create_plan(
        state["query"],
        state["period"]
    )

    if plan["status"] == "failed":
        raise Exception("Company not found")

    state["company"] = plan["company"]

    return state


# =====================================================
# FINANCIAL
# =====================================================

def financial_node(state):

    print("\nRunning Financial Agent...")

    state["financial"] = \
        get_financial_data(
            state["company"]
        )

    return state


# =====================================================
# HISTORICAL
# =====================================================

def historical_node(state):

    print("\nRunning Historical Agent...")

    hist = \
        get_historical_returns(
            state["company"]
        )

    state["historical"] = hist

    # merge into financial dict
    state["financial"][
        "historical_returns"
    ] = hist

    return state


# =====================================================
# NEWS
# =====================================================

def news_node(state):

    print("\nRunning News Agent...")

    news = \
        get_news(
            state["company"]
        )

    print(
        "NEWS TYPE:",
        type(news)
    )

    state["news"] = news

    return state


# =====================================================
# RANKING
# =====================================================

def ranking_node(state):

    print(
        "\nRunning Ranking Agent..."
    )

    state["ranking"] = \
        rank_company(

            state["company"],

            state["financial"],

            state["news"],

            state["period"]
        )

    return state


# =====================================================
# DECISION
# =====================================================

def decision_node(state):

    print("\nRunning Decision Agent...")

    print(
        "NEWS TYPE:",
        type(state["news"])
    )

    decision = \
        get_decision(

            state["company"],

            state["ranking"],

            state["financial"],

            state["news"],

            state["period"]
        )

    state["decision"] = decision

    return state


# =====================================================
# REPORT
# =====================================================

def report_node(
        state
):

    print(
        "\nRunning Report Agent..."
    )

    state["report"] = \
        generate_report(

            state["company"],

            state["financial"],

            state["news"],

            state["ranking"],

            state["decision"]
        )

    return state


# =====================================================
# GRAPH
# =====================================================

graph_builder = StateGraph(
    StockState
)

graph_builder.add_node(
    "planner",
    planner_node
)

graph_builder.add_node(
    "financial",
    financial_node
)

graph_builder.add_node(
    "historical",
    historical_node
)

graph_builder.add_node(
    "news",
    news_node
)

graph_builder.add_node(
    "ranking",
    ranking_node
)

graph_builder.add_node(
    "decision",
    decision_node
)

graph_builder.add_node(
    "report",
    report_node
)


# =====================================================
# FLOW
# =====================================================

graph_builder.add_edge(
    START,
    "planner"
)

graph_builder.add_edge(
    "planner",
    "financial"
)

graph_builder.add_edge(
    "financial",
    "historical"
)

graph_builder.add_edge(
    "historical",
    "news"
)

graph_builder.add_edge(
    "news",
    "ranking"
)

graph_builder.add_edge(
    "ranking",
    "decision"
)

graph_builder.add_edge(
    "decision",
    "report"
)

graph_builder.add_edge(
    "report",
    END
)


# =====================================================
# COMPILE
# =====================================================

stock_graph = \
    graph_builder.compile()


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = \
        stock_graph.invoke(

            {

                "query":
                "NMDC Limited",

                "period":
                "1y"
            }
        )

    print()
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print()

    print(
        result["report"]
    )
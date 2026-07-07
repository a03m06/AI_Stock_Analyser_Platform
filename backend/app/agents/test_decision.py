from planner_agent import create_plan
from financial_agent import get_financial_data
from news_agent import get_news
from ranking_agent import rank_company
from decision_agent import get_decision


companies = [

    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "SBIN",
    "TITAN",
    "BAHETI",
    "BONDADA",
    "SOLEX"
]

period = "3y"

results = []


for stock in companies:

    print("\n===================")
    print(stock)
    print("===================")

    plan = create_plan(stock)

    if plan["status"] != "success":
        continue

    company = plan["company"]

    financial = get_financial_data(
        company
    )

    news = get_news(
        company
    )

    ranking = rank_company(

        company,
        financial,
        news,
        period
    )

    decision = get_decision(

        company,
        ranking,
        financial,
        news,
        period
    )

    results.append(
        decision
    )


results = sorted(

    results,

    key=lambda x:
        x["score"],

    reverse=True
)


print("\n")
print("="*70)
print("FINAL DECISIONS")
print("="*70)

for i, company in enumerate(results):

    print(

        i+1,

        company["symbol"],

        "|",

        company["recommendation"],

        "|",

        company["score"]
    )

    print(

        "Reasons:",
        company["reasons"]
    )

    print()
from planner_agent import create_plan
from financial_agent import get_financial_data
from news_agent import get_news
from ranking_agent import rank_company


companies = [

    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "SBIN",
    "TITAN"

]

period = "1y"

results = []

for stock in companies:

    print("\n================================")
    print("Processing:", stock)
    print("================================")

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

    results.append(
        ranking
    )


results = sorted(

    results,

    key=lambda x:
        x["score"],

    reverse=True
)


print("\n")
print("="*60)
print("RANKINGS FOR", period)
print("="*60)

for i, company in enumerate(results):

    print(

        i+1,

        company["symbol"],

        ":",

        company["score"]
    )
from planner_agent import create_plan
from financial_agent import get_financial_data
from news_agent import get_news
from ranking_agent import rank_company


plan = create_plan(
    "TCS"
)

company = plan["company"]

financial = get_financial_data(
    company
)

news = get_news(
    company
)

print("\n====================")
print("RANKINGS")
print("====================")

for period in [

    "1m",
    "3m",
    "6m",
    "1y",
    "3y",
    "5y"

]:

    result = rank_company(

        company,
        financial,
        news,
        period

    )

    print(result)
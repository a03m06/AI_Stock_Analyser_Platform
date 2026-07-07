import pandas as pd

companies = pd.read_csv(
    "database/fundamentals/fundamentals_final.csv"
)

companies["company_name"] = (
    companies["company_name"]
    .astype(str)
    .str.strip()
)

companies["symbol"] = (
    companies["symbol"]
    .astype(str)
    .str.strip()
)


def find_company(query):

    query = str(query).lower().strip()

    rows = companies[
        companies["company_name"]
        .str.lower()
        == query
    ]

    if len(rows):
        return rows.iloc[0]

    rows = companies[
        companies["symbol"]
        .str.lower()
        == query
    ]

    if len(rows):
        return rows.iloc[0]

    rows = companies[
        companies["company_name"]
        .str.lower()
        .str.contains(
            query,
            na=False
        )
    ]

    if len(rows):
        return rows.iloc[0]

    return None


def create_plan(query, period="1y"):

    print("\nRunning Planner Agent...")

    company = find_company(query)

    if company is None:

        return {
            "status": "failed"
        }

    exchange = "NSE"

    if "exchange" in company.index:
        exchange = str(
            company["exchange"]
        )

    sector = "Unknown"

    if "sector" in company.index:
        sector = str(
            company["sector"]
        )

    return {

        "status": "success",

        "company": {

            "company_name":
            company["company_name"],

            "symbol":
            company["symbol"],

            "exchange":
            exchange,

            "sector":
            sector
        },

        "period":
        period
    }
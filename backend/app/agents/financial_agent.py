import pandas as pd

fundamentals = pd.read_csv(
    "database/fundamentals/fundamentals_final.csv"
)


def safe_float(x):

    try:

        if pd.isna(x):
            return None

        if str(x).strip() == "":
            return None

        return float(x)

    except:

        return None


def find_company(company):

    name = str(
        company["company_name"]
    ).lower()

    rows = fundamentals[
        fundamentals[
            "company_name"
        ]
        .astype(str)
        .str.lower()
        ==
        name
    ]

    if len(rows):

        return rows.iloc[0]

    rows = fundamentals[
        fundamentals[
            "company_name"
        ]
        .astype(str)
        .str.lower()
        .str.contains(
            name,
            na=False
        )
    ]

    if len(rows):

        return rows.iloc[0]

    return None


def get_financial_data(company):

    print(
        "\nRunning Financial Agent..."
    )

    row = find_company(
        company
    )

    if row is None:

        return {}

    return {

        "market_cap":
        safe_float(
            row.get("market_cap")
        ),

        "np_qtr":
        safe_float(
            row.get("np_qtr")
        ),

        "roce":
        safe_float(
            row.get("roce")
        ),

        "debt_equity":
        safe_float(
            row.get("debt_equity")
        ),

        "eps":
        safe_float(
            row.get("eps_12m")
        ),

        "promoter_holding":
        safe_float(
            row.get(
                "promoter_holding"
            )
        ),

        "cmp_pcf":
        safe_float(
            row.get("cmp_pcf")
        ),

        "roe":
        safe_float(
            row.get("roe")
        ),

        "pat":
        safe_float(
            row.get("pat_12m")
        ),

        "opm":
        safe_float(
            row.get("opm")
        ),

        "sales_growth":
        safe_float(
            row.get(
                "sales_growth_3y"
            )
        ),

        "profit_growth":
        safe_float(
            row.get(
                "profit_growth_3y"
            )
        ),

        "fii_holding":
        safe_float(
            row.get(
                "fii_holding"
            )
        ),

        "dii_holding":
        safe_float(
            row.get(
                "dii_holding"
            )
        )
    }
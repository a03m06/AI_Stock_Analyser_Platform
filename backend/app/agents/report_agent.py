# =====================================================
# REPORT AGENT
# =====================================================

def generate_report(

        company,

        financial,

        news,

        ranking,

        decision
):

    report = {

        # ====================================
        # COMPANY
        # ====================================

        "company_name":
        company.get(
            "company_name"
        ),

        "symbol":
        company.get(
            "symbol"
        ),

        "cap_category":
        ranking.get(
            "cap_category"
        ),

        "sector":
        company.get(
            "sector"
        ),

        "industry":
        company.get(
            "industry",
            "Unknown"
        ),

        # ====================================
        # AI SCORES
        # ====================================

        "ai_score":
        ranking.get(
            "score"
        ),

        "financial_score":
        ranking.get(
            "financial_score"
        ),

        "historical_score":
        ranking.get(
            "historical_score"
        ),

        "news_score":
        ranking.get(
            "news_score"
        ),

        # ====================================
        # RECOMMENDATION
        # ====================================

        "recommendation":
        decision.get(
            "recommendation"
        ),

        "reasons":
        decision.get(
            "reasons",
            []
        ),

        # ====================================
        # FINANCIALS
        # ====================================

        "market_cap":
        financial.get(
            "market_cap"
        ),

        "roe":
        financial.get(
            "roe"
        ),

        "roce":
        financial.get(
            "roce"
        ),

        "debt_equity":
        financial.get(
            "debt_equity"
        ),

        "eps_12m":
        financial.get(
            "eps"
        ),

        "pat_12m":
        financial.get(
            "pat"
        ),

        "opm":
        financial.get(
            "opm"
        ),

        "sales_growth_3y":
        financial.get(
            "sales_growth"
        ),

        "profit_growth_3y":
        financial.get(
            "profit_growth"
        ),

        # ====================================
        # HOLDINGS
        # ====================================

        "promoter_holding":
        financial.get(
            "promoter_holding"
        ),

        "fii_holding":
        financial.get(
            "fii_holding"
        ),

        "dii_holding":
        financial.get(
            "dii_holding"
        ),

        # ====================================
        # HISTORICAL RETURNS
        # ====================================

        "historical_returns":
        financial.get(
            "historical_returns",
            {}
        ),

        # ====================================
        # NEWS
        # ====================================

        "news_sentiment":
        news.get(
            "sentiment",
            50
        ),

        "headlines":
        news.get(
            "headlines",
            []
        ),

        "expansion_news":
        news.get(
            "expansion_news",
            []
        ),

        "order_news":
        news.get(
            "order_news",
            []
        )
    }

    return report


# =====================================================
# PRINT REPORT
# =====================================================

def print_report(
        report
):

    print()
    print("=" * 70)
    print(
        report["company_name"]
    )
    print("=" * 70)

    print()

    print(
        "AI Score:",
        report["ai_score"]
    )

    print(
        "Recommendation:",
        report["recommendation"]
    )

    print()

    print(
        "Financial Score:",
        report[
            "financial_score"
        ]
    )

    print(
        "Historical Score:",
        report[
            "historical_score"
        ]
    )

    print(
        "News Score:",
        report[
            "news_score"
        ]
    )

    print()

    print(
        "ROE:",
        report["roe"]
    )

    print(
        "ROCE:",
        report["roce"]
    )

    print(
        "Debt/Equity:",
        report["debt_equity"]
    )

    print(
        "OPM:",
        report["opm"]
    )

    print()

    print(
        "Sales Growth:",
        report[
            "sales_growth_3y"
        ]
    )

    print(
        "Profit Growth:",
        report[
            "profit_growth_3y"
        ]
    )

    print()

    print(
        "Historical Returns"
    )

    for k, v in \
            report[
                "historical_returns"
            ].items():

        print(
            k,
            ":",
            str(v) + "%"
        )

    print()

    print(
        "Reasons:"
    )

    for r in \
            report[
                "reasons"
            ]:

        print(
            "-",
            r
        )

    print()

    print(
        "News Sentiment:",
        report[
            "news_sentiment"
        ]
    )

    print()

    print(
        "Latest News:"
    )

    for h in \
            report[
                "headlines"
            ][:5]:

        print(
            "-",
            h
        )
# =========================================
# Helper
# =========================================

def normalize(value, min_val, max_val):

    if value is None:
        return 50

    try:
        value = float(value)

        if max_val == min_val:
            return 50

        score = (
            (value - min_val)
            /
            (max_val - min_val)
        ) * 100

        return max(
            0,
            min(100, score)
        )

    except:
        return 50


# =========================================
# Financial Score
# =========================================

def calculate_financial_score(financial):

    score = 0

    score += normalize(
        financial.get("roce"),
        0,
        40
    ) * 0.15

    score += normalize(
        financial.get("roe"),
        0,
        40
    ) * 0.15

    score += normalize(
        financial.get("sales_growth"),
        -50,
        100
    ) * 0.15

    score += normalize(
        financial.get("profit_growth"),
        -50,
        100
    ) * 0.15

    score += normalize(
        financial.get("opm"),
        0,
        40
    ) * 0.10

    debt = financial.get(
        "debt_equity"
    )

    if debt is None:
        debt_score = 50

    elif debt <= 0.2:
        debt_score = 100

    elif debt <= 0.5:
        debt_score = 80

    elif debt <= 1:
        debt_score = 60

    elif debt <= 2:
        debt_score = 30

    else:
        debt_score = 0

    score += debt_score * 0.10

    score += normalize(
        financial.get(
            "promoter_holding"
        ),
        0,
        75
    ) * 0.05

    score += normalize(
        financial.get(
            "fii_holding"
        ),
        0,
        50
    ) * 0.05

    score += normalize(
        financial.get(
            "dii_holding"
        ),
        0,
        50
    ) * 0.05

    score += normalize(
        financial.get(
            "eps"
        ),
        0,
        200
    ) * 0.03

    score += normalize(
        financial.get(
            "pat"
        ),
        0,
        5000
    ) * 0.02

    return round(
        score,
        2
    )


# =========================================
# Historical Score
# =========================================

def calculate_historical_score(
        financial,
        period
):

    returns = (
        financial
        .get(
            "historical_returns",
            {}
        )
        .get(period)
    )

    if returns is None:
        return 50

    return max(
        0,
        min(
            100,
            (returns + 100) / 2
        )
    )


# =========================================
# News Score
# =========================================

def calculate_news_score(
        news
):

    if not isinstance(
            news,
            dict
    ):
        return 50

    score = news.get(
        "sentiment",
        50
    )

    score += min(
        len(
            news.get(
                "expansion_news",
                []
            )
        ) * 5,
        20
    )

    score += min(
        len(
            news.get(
                "order_news",
                []
            )
        ) * 5,
        20
    )

    return min(
        score,
        100
    )


# =========================================
# AI Score
# =========================================

def calculate_ai_score(

        financial_score,

        historical_score,

        news_score
):

    return round(

        financial_score * 0.70 +

        historical_score * 0.20 +

        news_score * 0.10,

        2
    )


# =========================================
# Market Cap Category
# =========================================

def get_market_cap_category(
        market_cap
):

    if market_cap is None:
        return "unknown"

    if market_cap >= 50000:
        return "large"

    elif market_cap >= 10000:
        return "mid"

    elif market_cap >= 1000:
        return "small"

    else:
        return "micro"


# =========================================
# Rank Company
# =========================================

def rank_company(

        company,

        financial,

        news,

        period="1y"
):

    financial_score = \
        calculate_financial_score(
            financial
        )

    historical_score = \
        calculate_historical_score(
            financial,
            period
        )

    news_score = \
        calculate_news_score(
            news
        )

    ai_score = \
        calculate_ai_score(

            financial_score,

            historical_score,

            news_score
        )

    market_cap = \
        financial.get(
            "market_cap"
        )

    return {

        "company_name":
        company[
            "company_name"
        ],

        "symbol":
        company[
            "symbol"
        ],

        "exchange":
        company.get(
            "exchange",
            "NSE"
        ),

        "historical_score":
        round(
            historical_score,
            2
        ),

        "financial_score":
        round(
            financial_score,
            2
        ),

        "news_score":
        round(
            news_score,
            2
        ),

        "score":
        ai_score,

        "market_cap_category":
        get_market_cap_category(
            market_cap
        ),

        "sector":
        company.get(
            "sector",
            "Unknown"
        ),

        "industry":
        company.get(
            "industry",
            "Unknown"
        ),

        "ranking_period":
        period
    }
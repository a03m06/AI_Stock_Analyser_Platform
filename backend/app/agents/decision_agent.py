# =========================================
# Recommendation
# =========================================

def get_recommendation(score):

    if score >= 75:
        return "STRONG BUY"

    elif score >= 60:
        return "BUY"

    elif score >= 45:
        return "HOLD"

    elif score >= 30:
        return "AVOID"

    else:
        return "SELL"


# =========================================
# Reasons
# =========================================

def generate_reasons(

        financial,

        news,

        period="1y"
):

    reasons = []

    # ROE
    roe = financial.get("roe")

    if roe is not None:

        if roe >= 20:
            reasons.append(
                f"Strong ROE ({roe}%)"
            )

        elif roe <= 10:
            reasons.append(
                f"Weak ROE ({roe}%)"
            )

    # ROCE
    roce = financial.get("roce")

    if roce is not None:

        if roce >= 20:
            reasons.append(
                f"Strong ROCE ({roce}%)"
            )

    # Sales growth
    sales = financial.get(
        "sales_growth"
    )

    if sales is not None:

        if sales >= 20:
            reasons.append(
                f"Strong sales growth ({sales}%)"
            )

        elif sales <= 0:
            reasons.append(
                f"Weak sales growth ({sales}%)"
            )

    # Profit growth
    profit = financial.get(
        "profit_growth"
    )

    if profit is not None:

        if profit >= 20:
            reasons.append(
                f"Strong profit growth ({profit}%)"
            )

        elif profit <= 0:
            reasons.append(
                f"Weak profit growth ({profit}%)"
            )

    # OPM
    opm = financial.get("opm")

    if opm is not None:

        if opm >= 20:
            reasons.append(
                f"Healthy margins ({opm}%)"
            )

    # Debt
    debt = financial.get(
        "debt_equity"
    )

    if debt is not None:

        if debt <= 0.5:
            reasons.append(
                f"Low debt ({debt})"
            )

        elif debt >= 2:
            reasons.append(
                f"High debt ({debt})"
            )

    # Historical return
    returns = \
        financial.get(
            "historical_returns",
            {}
        ).get(period)

    if returns is not None:

        if returns > 20:

            reasons.append(
                f"Strong {period} return ({returns}%)"
            )

        elif returns < -20:

            reasons.append(
                f"Weak {period} return ({returns}%)"
            )

    # News sentiment
    sentiment = \
        news.get(
            "sentiment",
            50
        )

    if sentiment > 60:

        reasons.append(
            "Positive news sentiment"
        )

    elif sentiment < 40:

        reasons.append(
            "Negative news sentiment"
        )

    # Expansion
    if len(
        news.get(
            "expansion_news",
            []
        )
    ):

        reasons.append(
            "Expansion activities detected"
        )

    # Orders
    if len(
        news.get(
            "order_news",
            []
        )
    ):

        reasons.append(
            "Recent order wins detected"
        )

    return reasons


# =========================================
# Decision Agent
# =========================================

def get_decision(

        company,

        ranking,

        financial,

        news,

        period="1y"
):

    score = ranking["score"]

    recommendation = \
        get_recommendation(
            score
        )

    reasons = \
        generate_reasons(

            financial,

            news,

            period
        )

    return {

        "company_name":
        company["company_name"],

        "symbol":
        company["symbol"],

        "period":
        period,

        "financial_score":
        ranking[
            "financial_score"
        ],

        "historical_score":
        ranking[
            "historical_score"
        ],

        "news_score":
        ranking[
            "news_score"
        ],

        "score":
        score,

        "recommendation":
        recommendation,

        "reasons":
        reasons
    }
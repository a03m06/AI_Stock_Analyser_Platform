from app.scoring.ai_score import (
    calculate_ai_score
)


sample = {

    "market_cap": 100000,

    "expansion_value": 20000,

    "revenue_cagr": 18,

    "pat_growth": 22,

    "eps_growth": 16,

    "order_book": 50000,

    "roe": 24,

    "roce": 28,

    "ebitda_margin": 25,

    "debt_equity": 0.1,

    "cash_flow_ratio": 1.1,

    "promoter_holding": 72,

    "institutional_holding": 15
}


result = calculate_ai_score(
    sample
)

print(result)
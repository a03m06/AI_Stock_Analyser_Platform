from app.scoring.weights import WEIGHTS
from app.scoring.benchmarks import BENCHMARKS
from app.scoring.helpers import (
    higher_is_better,
    lower_is_better
)


def calculate_ai_score(data):

    scores = {}

    market_cap = data.get(
        "market_cap",
        1
    )

    market_cap = max(
        float(market_cap or 1),
        1
    )

    # =====================================
    # Expansion
    # =====================================

    expansion_value = float(
        data.get(
            "expansion_value",
            0
        ) or 0
    )

    expansion_ratio = (
        expansion_value /
        market_cap
    )

    scores["expansion_plan"] = round(

        min(
            expansion_ratio,
            1
        )

        *

        WEIGHTS[
            "expansion_plan"
        ],

        2
    )

    # =====================================
    # Revenue CAGR
    # =====================================

    scores["revenue_cagr"] = \
        higher_is_better(

            data.get(
                "revenue_cagr",
                0
            ),

            BENCHMARKS[
                "revenue_cagr"
            ],

            WEIGHTS[
                "revenue_cagr"
            ]
        )

    # =====================================
    # PAT Growth
    # =====================================

    scores["pat_growth"] = \
        higher_is_better(

            data.get(
                "pat_growth",
                0
            ),

            BENCHMARKS[
                "pat_growth"
            ],

            WEIGHTS[
                "pat_growth"
            ]
        )

    # =====================================
    # EPS Growth
    # =====================================

    scores["eps_growth"] = \
        higher_is_better(

            data.get(
                "eps_growth",
                0
            ),

            BENCHMARKS[
                "eps_growth"
            ],

            WEIGHTS[
                "eps_growth"
            ]
        )

    # =====================================
    # Order Book
    # =====================================

    order_book = float(
        data.get(
            "order_book",
            0
        ) or 0
    )

    order_ratio = (
        order_book /
        market_cap
    )

    scores["order_book"] = round(

        min(
            order_ratio,
            1
        )

        *

        WEIGHTS[
            "order_book"
        ],

        2
    )

    # =====================================
    # ROE
    # =====================================

    scores["roe"] = \
        higher_is_better(

            data.get(
                "roe",
                0
            ),

            BENCHMARKS[
                "roe"
            ],

            WEIGHTS[
                "roe"
            ]
        )

    # =====================================
    # ROCE
    # =====================================

    scores["roce"] = \
        higher_is_better(

            data.get(
                "roce",
                0
            ),

            BENCHMARKS[
                "roce"
            ],

            WEIGHTS[
                "roce"
            ]
        )

    # =====================================
    # EBITDA Margin
    # =====================================

    scores["ebitda_margin"] = \
        higher_is_better(

            data.get(
                "ebitda_margin",
                0
            ),

            BENCHMARKS[
                "ebitda_margin"
            ],

            WEIGHTS[
                "ebitda_margin"
            ]
        )

    # =====================================
    # Debt
    # =====================================

    scores["debt_equity"] = \
        lower_is_better(

            data.get(
                "debt_equity",
                0
            ),

            0.2,

            WEIGHTS[
                "debt_equity"
            ]
        )

    # =====================================
    # Cash Flow
    # =====================================

    scores["cash_flow"] = \
        higher_is_better(

            data.get(
                "cash_flow_ratio",
                0
            ),

            BENCHMARKS[
                "cash_flow_ratio"
            ],

            WEIGHTS[
                "cash_flow"
            ]
        )

    # =====================================
    # Promoter
    # =====================================

    promoter = float(
        data.get(
            "promoter_holding",
            0
        ) or 0
    )

    scores[
        "promoter_holding"
    ] = round(

        min(

            promoter /

            BENCHMARKS[
                "promoter_holding"
            ],

            1
        )

        *

        WEIGHTS[
            "promoter_holding"
        ],

        2
    )

    # =====================================
    # Institutional
    # =====================================

    institutional = float(

        data.get(
            "institutional_holding",
            0
        ) or 0
    )

    scores[
        "institutional_holding"
    ] = round(

        min(

            institutional /

            BENCHMARKS[
                "institutional_holding"
            ],

            1
        )

        *

        WEIGHTS[
            "institutional_holding"
        ],

        2
    )

    # =====================================
    # FINAL SCORE
    # =====================================

    total_score = round(
        sum(
            scores.values()
        ),
        2
    )

    return {

        "score":
            total_score,

        "breakdown":
            scores
    }
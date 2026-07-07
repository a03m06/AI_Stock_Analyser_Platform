import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.scoring.ai_score import calculate_ai_score
from app.agents.historical_agent import get_return


# =====================================================
# SHORT-LIVED RESULT CACHE
# =====================================================
# Caches the fully computed ranking table per
# (endpoint, filters) combination for a short time so
# repeat requests (e.g. re-rendering the same page,
# switching tabs and back) return instantly instead of
# re-fetching from Yahoo Finance again.

_RESULT_CACHE = {}
_RESULT_CACHE_TTL_SECONDS = 60 * 10  # 10 minutes


def _result_cache_get(key):
    entry = _RESULT_CACHE.get(key)

    if not entry:
        return None

    value, expires_at = entry

    if time.time() > expires_at:
        _RESULT_CACHE.pop(key, None)
        return None

    return value.copy()


def _result_cache_set(key, value):
    _RESULT_CACHE[key] = (value.copy(), time.time() + _RESULT_CACHE_TTL_SECONDS)


# =====================================================
# LOAD DATA
# =====================================================

fundamentals = pd.read_csv(
    "database/fundamentals/fundamentals_final.csv"
)

fundamentals = fundamentals.fillna(0)


# =====================================================
# FILTER
# =====================================================

def filter_companies(
        cap_category=None,
        sector=None,
        industry=None
):

    df = fundamentals.copy()

    # ------------------------------
    # Market Cap
    # ------------------------------
    if (
        cap_category and
        cap_category != "All"
    ):

        df = df[
            df["cap_category"]
            ==
            cap_category
        ]

    # ------------------------------
    # Sector
    # ------------------------------
    if (
        sector and
        sector != "All"
    ):

        df = df[
            df["sector"]
            ==
            sector
        ]

    # ------------------------------
    # Industry
    # ------------------------------
    if (
        industry and
        industry != "All"
    ):

        df = df[
            df["industry"]
            ==
            industry
        ]

    return df


# =====================================================
# CAP CATEGORIES
# =====================================================

def get_cap_categories():

    return sorted(

        fundamentals[
            "cap_category"
        ]
        .dropna()
        .unique()
        .tolist()
    )


# =====================================================
# SECTORS
# =====================================================

def get_sectors(
        cap_category=None
):

    df = fundamentals.copy()

    if (
        cap_category and
        cap_category != "All"
    ):

        df = df[
            df["cap_category"]
            ==
            cap_category
        ]

    sectors = sorted(

        df["sector"]
        .dropna()
        .unique()
        .tolist()
    )

    return ["All"] + sectors

# =====================================================
# INDUSTRIES
# =====================================================

def get_industries(

        cap_category=None,
        sector=None
):

    df = fundamentals.copy()

    if (
        cap_category and
        cap_category != "All"
    ):

        df = df[
            df["cap_category"]
            ==
            cap_category
        ]

    if (
        sector and
        sector != "All"
    ):

        df = df[
            df["sector"]
            ==
            sector
        ]

    industries = sorted(

        df["industry"]
        .dropna()
        .unique()
        .tolist()
    )

    return ["All"] + industries


# =====================================================
# AI RANKING
# =====================================================

def ai_ranking(

        cap_category=None,
        sector=None,
        industry=None,
        top_n=None
):

    cache_key = (
        "ai",
        cap_category,
        sector,
        industry
    )

    cached = _result_cache_get(cache_key)

    if cached is None:

        df = filter_companies(

            cap_category,
            sector,
            industry
        )

        scores = []

        for _, row in df.iterrows():

            try:

                result = \
                    calculate_ai_score(
                        row.to_dict()
                    )

                score = \
                    result.get(
                        "score",
                        0
                    )

            except Exception as e:

                print(
                    "AI SCORE ERROR:",
                    e
                )

                score = 0

            scores.append(
                score
            )

        df = df.copy()

        df["ai_score"] = \
            scores

        df = df.sort_values(

            "ai_score",

            ascending=False
        )[
            [
                "company_name",
                "symbol",
                "cap_category",
                "sector",
                "industry",
                "ai_score"
            ]
        ]

        _result_cache_set(cache_key, df)

        cached = df

    # top_n=None means "return every company in this category"
    if top_n is None:
        return cached

    return cached.head(top_n)


# =====================================================
# HISTORICAL RANKING
# =====================================================

def _fetch_one_return(company, period):

    try:
        return get_return(company, period)

    except Exception as e:

        print(
            "RETURN ERROR:",
            e
        )

        return 0


def historical_ranking(

        cap_category=None,
        sector=None,
        industry=None,
        period="1y",
        top_n=None
):

    cache_key = (
        "historical",
        cap_category,
        sector,
        industry,
        period
    )

    cached = _result_cache_get(cache_key)

    if cached is None:

        df = filter_companies(

            cap_category,
            sector,
            industry
        )

        companies = [
            {
                "company_name": row["company_name"],
                "symbol": row["symbol"]
            }
            for _, row in df.iterrows()
        ]

        # Fetch returns concurrently instead of one-by-one.
        # Each call is a network request to Yahoo Finance, so
        # doing them sequentially for hundreds of companies is
        # what was causing the 15+ minute load times. Fanning
        # them out across a thread pool (I/O-bound, so threads
        # work fine here) turns that into a matter of seconds,
        # and results are cached afterwards so it's instant on
        # repeat requests for the same filters/period.
        returns = [0] * len(companies)

        with ThreadPoolExecutor(max_workers=25) as executor:

            future_to_index = {
                executor.submit(_fetch_one_return, company, period): i
                for i, company in enumerate(companies)
            }

            for future in as_completed(future_to_index):
                i = future_to_index[future]
                returns[i] = future.result()

        df = df.copy()

        df["historical_return"] = returns

        df = df.sort_values(

            "historical_return",

            ascending=False
        )[
            [
                "company_name",
                "symbol",
                "cap_category",
                "sector",
                "industry",
                "historical_return"
            ]
        ]

        _result_cache_set(cache_key, df)

        cached = df

    # top_n=None means "return every company in this category"
    if top_n is None:
        return cached

    return cached.head(top_n)


# =====================================================
# COMPANY DETAILS
# =====================================================

def get_company_details(
        company_name
):

    row = fundamentals[

        fundamentals[
            "company_name"
        ]
        ==
        company_name
    ]

    if len(row) == 0:

        return None

    row = row.iloc[0]

    try:

        result = \
            calculate_ai_score(
                row.to_dict()
            )

        ai_score = \
            result.get(
                "score",
                0
            )

        breakdown = \
            result.get(
                "breakdown",
                {}
            )

    except Exception as e:

        print(
            "DETAIL SCORE ERROR:",
            e
        )

        ai_score = 0
        breakdown = {}

    try:

        historical = \
            get_return(

                {
                    "company_name":
                    row.company_name,

                    "symbol":
                    row.symbol
                },

                "1y"
            )

    except:

        historical = 0

    return {

        "company_name":
        row.company_name,

        "symbol":
        row.symbol,

        "cap_category":
        row.cap_category,

        "sector":
        row.sector,

        "industry":
        row.industry,

        "market_cap":
        row.market_cap,

        "np_qtr":
        row.np_qtr,

        "roce":
        row.roce,

        "debt_equity":
        row.debt_equity,

        "eps_12m":
        row.eps_12m,

        "promoter_holding":
        row.promoter_holding,

        "cmp_pcf":
        row.cmp_pcf,

        "roe":
        row.roe,

        "pat_12m":
        row.pat_12m,

        "opm":
        row.opm,

        "sales_growth_3y":
        row.sales_growth_3y,

        "profit_growth_3y":
        row.profit_growth_3y,

        "fii_holding":
        row.fii_holding,

        "dii_holding":
        row.dii_holding,

        "ai_score":
        ai_score,

        "score_breakdown":
        breakdown,

        "historical_1y":
        historical
    }


# =====================================================
# PRINT AI
# =====================================================

def print_ai(df):

    print()
    print("=" * 70)
    print("AI RANKING")
    print("=" * 70)

    for i, row in enumerate(
            df.itertuples(),
            1
    ):

        print(

            f"{i:2d}",

            row.company_name,

            round(
                row.ai_score,
                2
            )
        )


# =====================================================
# PRINT HISTORICAL
# =====================================================

def print_historical(df):

    print()
    print("=" * 70)
    print(
        "HISTORICAL RANKING"
    )
    print("=" * 70)

    for i, row in enumerate(
            df.itertuples(),
            1
    ):

        print(

            f"{i:2d}",

            row.company_name,

            str(

                round(
                    row.historical_return,
                    2
                )

            ) + "%"
        )


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    ai = ai_ranking(

        cap_category=
        "Large Cap",

        sector=
        "Metals and Mining",

        top_n=10
    )

    print_ai(ai)

    hist = historical_ranking(

        cap_category=
        "Large Cap",

        sector=
        "Metals and Mining",

        period="1y",

        top_n=10
    )

    print_historical(
        hist
    )    
import time
import yfinance as yf


# ============================================
# Simple in-memory TTL cache
# ============================================
# Historical returns/price history don't need to be
# recomputed on every single request - they only change
# meaningfully once a day. Caching turns a slow live
# fetch into a near-instant response on repeat requests.

_CACHE = {}
_CACHE_TTL_SECONDS = 60 * 30  # 30 minutes


def _cache_get(key):
    entry = _CACHE.get(key)

    if not entry:
        return None

    value, expires_at = entry

    if time.time() > expires_at:
        _CACHE.pop(key, None)
        return None

    return value


def _cache_set(key, value):
    _CACHE[key] = (value, time.time() + _CACHE_TTL_SECONDS)


# ============================================
# Get Yahoo Symbol
# ============================================

def get_yahoo_symbol(company):

    symbol = str(
        company.get(
            "symbol",
            ""
        )
    ).strip()

    if not symbol:
        return None

    return symbol + ".NS"


# ============================================
# Calculate Return % from a history dataframe
# ============================================

def _return_from_history(hist):

    if hist is None or len(hist) < 2:
        return 0

    try:
        old_price = float(hist["Close"].iloc[0])
        current_price = float(hist["Close"].iloc[-1])

        if old_price == 0:
            return 0

        return round(((current_price - old_price) / old_price) * 100, 2)

    except Exception:
        return 0


# ============================================
# Single Period Return (fetches ONLY the requested
# period instead of 1m/3m/6m/1y/3y/5y every time)
# ============================================

PERIOD_MAP = {
    "1m": "1mo",
    "3m": "3mo",
    "6m": "6mo",
    "1y": "1y",
    "3y": "3y",
    "5y": "5y",
}


def get_return(company, period="1y"):

    yahoo_symbol = get_yahoo_symbol(company)

    if yahoo_symbol is None:
        return 0

    cache_key = ("return", yahoo_symbol, period)

    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    yf_period = PERIOD_MAP.get(period, "1y")

    try:
        stock = yf.Ticker(yahoo_symbol)

        hist = stock.history(
            period=yf_period,
            auto_adjust=True
        )

        value = _return_from_history(hist)

    except Exception as e:
        print(yahoo_symbol, e)
        value = 0

    _cache_set(cache_key, value)

    return value


# ============================================
# Historical Returns (all periods - used on the
# company detail page, not on the ranking list)
# ============================================

def get_historical_returns(company):

    return {
        p: get_return(company, p)
        for p in PERIOD_MAP.keys()
    }


# ============================================
# Price History (for graph)
# ============================================

def get_price_history(company, period="1y"):

    yahoo_symbol = get_yahoo_symbol(company)

    if yahoo_symbol is None:
        return []

    cache_key = ("price_history", yahoo_symbol, period)

    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    try:
        stock = yf.Ticker(yahoo_symbol)

        hist = stock.history(
            period=PERIOD_MAP.get(period, "1y"),
            auto_adjust=True
        )

        if hist.empty:
            result = []
        else:
            result = [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "price": round(float(row["Close"]), 2)
                }
                for date, row in hist.iterrows()
            ]

    except Exception as e:
        print(yahoo_symbol, e)
        result = []

    _cache_set(cache_key, result)

    return result


# ============================================
# TEST
# ============================================

if __name__ == "__main__":

    company = {
        "company_name": "TCS",
        "symbol": "TCS"
    }

    print(get_historical_returns(company))

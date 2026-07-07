import time
import pandas as pd
import yfinance as yf
from fastapi import APIRouter

router = APIRouter()



# The previous version of this endpoint returned fully
# hardcoded numbers - that's why it never looked "live".
# This version pulls real index levels and computes real
# gainers/losers/sentiment from your dataset via yfinance.

# Two things worth knowing:
# 1. yfinance is an UNOFFICIAL, free wrapper around Yahoo
#    Finance - it's fine for a personal project/dev, but
#    for a real product you'll eventually want a licensed
#    delayed-data vendor (this matches what we discussed
#    earlier re: Global Datafeeds / TrueData).
# 2. Double-check the index tickers below actually resolve
#    on your machine (network is disabled in this sandbox
#    so I couldn't verify live). ^NSEI, ^BSESN and ^NSEBANK
#    are well-established Yahoo tickers. The midcap/smallcap
#    ones are more inconsistent across data providers - if
#    they come back empty, swap in whatever ticker your
#    yfinance version resolves them to.
# =====================================================

INDEX_TICKERS = {
    "NIFTY50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANKNIFTY": "^NSEBANK",
    "MIDCAP": "^NSEMDCP50",
    "SMALLCAP": "^CNXSC",
}

# How many of the largest companies in your dataset to scan
# for top gainers/losers. Keep this modest - it's a single
# batched network call either way, but a smaller watchlist
# means a snappier response.
GAINERS_LOSERS_WATCHLIST_SIZE = 40

_CACHE = {"data": None, "expires_at": 0}
_CACHE_TTL_SECONDS = 60 * 10  # 10 minutes - fewer hits to Yahoo, still feels "live enough"


# =====================================================
# NOTE: yfinance calls occasionally fail wholesale when
# run from a cloud host (Yahoo rate-limits/blocks known
# datacenter IP ranges more aggressively than home IPs).
# When that happens we now fall back to the last
# successfully fetched snapshot instead of showing 0%
# everywhere, and flag is_live=False so the frontend can
# make that visible if it wants to.
# =====================================================

_LAST_GOOD = {"data": None, "captured_at": None}


def _get_index_changes():
    """Fetches all indices in a single batched yf.download call
    instead of 5 separate yf.Ticker(...).history() calls - fewer
    round trips to Yahoo means less chance of hitting a rate limit.
    """

    changes = {name: {"change": 0, "value": 0} for name in INDEX_TICKERS}

    try:
        tickers = list(INDEX_TICKERS.values())

        data = yf.download(
            tickers=tickers,
            period="2d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )

        for name, ticker in INDEX_TICKERS.items():

            try:
                closes = data[ticker]["Close"].dropna()

                if len(closes) < 2:
                    continue

                prev_close = float(closes.iloc[-2])
                last_close = float(closes.iloc[-1])

                changes[name] = {
                    "change": round(((last_close - prev_close) / prev_close) * 100, 2),
                    "value": round(last_close, 2),
                }

            except Exception as e:
                print("INDEX PARSE ERROR:", name, e)

    except Exception as e:
        print("INDEX FETCH ERROR:", e)

    return changes


def _get_gainers_losers():
    """Top gainers/losers from the market-cap watchlist.

    NOTE: this used to also derive "market sentiment" from the average
    change of this same watchlist - a *different* set of stocks than the
    headline indices shown in the Market Overview panel. That's why
    sentiment could say BEARISH even while NIFTY/SENSEX were both green.
    Sentiment is now derived from the actual indices - see
    _get_market_sentiment() below.
    """

    try:
        fundamentals = pd.read_csv("database/fundamentals/fundamentals_final.csv")
        fundamentals = fundamentals.fillna(0)

        watchlist = (
            fundamentals
            .sort_values("market_cap", ascending=False)
            .head(GAINERS_LOSERS_WATCHLIST_SIZE)
        )

        tickers = [f"{sym}.NS" for sym in watchlist["symbol"].tolist()]

        # One batched call instead of one call per company
        data = yf.download(
            tickers=tickers,
            period="2d",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )

        day_changes = {}

        for symbol, ticker in zip(watchlist["symbol"], tickers):

            try:
                closes = data[ticker]["Close"].dropna()

                if len(closes) < 2:
                    continue

                prev_close = float(closes.iloc[-2])
                last_close = float(closes.iloc[-1])

                pct = ((last_close - prev_close) / prev_close) * 100

                company_name = watchlist.loc[
                    watchlist["symbol"] == symbol, "company_name"
                ].iloc[0]

                day_changes[company_name] = pct

            except Exception:
                continue

        if not day_changes:
            return [], []

        sorted_changes = sorted(day_changes.items(), key=lambda x: x[1], reverse=True)

        top_gainers = [name for name, _ in sorted_changes[:3]]
        top_losers = [name for name, _ in sorted_changes[-3:]][::-1]

        return top_gainers, top_losers

    except Exception as e:
        print("GAINERS/LOSERS ERROR:", e)
        return [], []


# Indices that drive the headline "market sentiment" label. BANKNIFTY is
# included as a broad-market proxy; MIDCAP/SMALLCAP are left out since
# they can move independently of the broader tape and aren't what most
# people mean by "is the market up or down today".
SENTIMENT_INDICES = ["NIFTY50", "SENSEX", "BANKNIFTY"]


def _get_market_sentiment(indices):
    """Derives BULLISH/BEARISH/NEUTRAL from the actual index % changes
    (the same numbers shown in the Market Overview cards) so the label
    always agrees with what the user sees on screen.
    """

    changes = [
        indices[name]["change"]
        for name in SENTIMENT_INDICES
        if name in indices
    ]

    if not changes:
        return "NEUTRAL"

    avg_change = sum(changes) / len(changes)

    if avg_change > 0:
        return "BULLISH"
    elif avg_change < 0:
        return "BEARISH"
    return "NEUTRAL"


def _looks_like_real_data(indices, top_gainers, top_losers):
    """A crude but effective check: if every index came back as 0/0
    AND we got no gainers/losers, that's not "the market is flat" -
    that's yfinance failing wholesale (e.g. Yahoo blocking this
    server's IP). Real flat/holiday days would still have nonzero
    index *values* even if change is 0.
    """

    any_real_value = any(
        idx["value"] not in (0, None) for idx in indices.values()
    )

    return any_real_value or bool(top_gainers) or bool(top_losers)


@router.get("/api/dashboard")
def market_dashboard():

    now = time.time()

    if _CACHE["data"] is not None and now < _CACHE["expires_at"]:
        return _CACHE["data"]

    indices = _get_index_changes()
    top_gainers, top_losers = _get_gainers_losers()
    market_sentiment = _get_market_sentiment(indices)

    fetch_succeeded = _looks_like_real_data(indices, top_gainers, top_losers)

    if fetch_succeeded:
        result = {
            "indices": indices,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "market_sentiment": market_sentiment,
            "is_live": True,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        _LAST_GOOD["data"] = result
        _LAST_GOOD["captured_at"] = result["last_updated"]

        # Real data - safe to trust it for the full TTL
        _CACHE["data"] = result
        _CACHE["expires_at"] = now + _CACHE_TTL_SECONDS

    elif _LAST_GOOD["data"] is not None:
        # Fresh fetch failed - serve the last snapshot that actually
        # worked, but label it clearly as not live, and keep the
        # original timestamp so it's obvious it's stale.
        result = {
            **_LAST_GOOD["data"],
            "is_live": False,
            "last_updated": _LAST_GOOD["captured_at"],
        }

        # Don't cache this for the full TTL - retry sooner in case
        # the block/rate-limit was transient.
        _CACHE["data"] = result
        _CACHE["expires_at"] = now + 30

    else:
        # No fetch has ever succeeded yet (e.g. right after a fresh
        # deploy) - nothing good to fall back to.
        result = {
            "indices": indices,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "market_sentiment": market_sentiment,
            "is_live": False,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        _CACHE["data"] = result
        _CACHE["expires_at"] = now + 30

    return result

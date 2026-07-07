import feedparser
from urllib.parse import quote
from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)


# =========================================
# SENTIMENT
# =========================================

def analyze_sentiment(headlines):

    analyzer = \
        SentimentIntensityAnalyzer()

    score = 0

    for headline in headlines:

        score += \
            analyzer.polarity_scores(
                headline
            )["compound"]

    if len(headlines):
        score /= len(headlines)
    else:
        score = 0

    return round(
        (score + 1) * 50,
        2
    )


# =========================================
# EXPANSION NEWS
# =========================================

def detect_expansion(news_items):

    keywords = [

        "expansion",
        "expand",
        "factory",
        "plant",
        "capex",
        "investment",
        "capacity",
        "acquisition",
        "new facility",
        "manufacturing"
    ]

    result = []

    for item in news_items:

        text = item["title"].lower()

        for word in keywords:

            if word in text:

                result.append(
                    item
                )

                break

    return result


# =========================================
# ORDER NEWS
# =========================================

def detect_orders(news_items):

    keywords = [

        "order",
        "orders",
        "contract",
        "deal",
        "project",
        "agreement",
        "wins",
        "award",
        "purchase"
    ]

    result = []

    for item in news_items:

        text = item["title"].lower()

        for word in keywords:

            if word in text:

                result.append(
                    item
                )

                break

    return result


# =========================================
# DEFAULT RESULT
# =========================================

def empty_news():

    return {

        "headlines": [],

        "sentiment": 50,

        "news_period_score": {

            "1m": 50,
            "3m": 50,
            "6m": 50,
            "1y": 50,
            "3y": 50,
            "5y": 50
        },

        "expansion_news": [],

        "order_news": []
    }


# =========================================
# NEWS AGENT
# =========================================

def get_news(company):

    print(
        "\nRunning News Agent..."
    )

    try:

        company_name = \
            company[
                "company_name"
            ]

        query = quote(
            f"{company_name} stock"
        )

        rss = \
            "https://news.google.com/rss/search?q=" \
            + query

        print(
            "Searching:",
            company_name
        )

        feed = \
            feedparser.parse(
                rss
            )

        news_items = []

        for entry in \
                feed.entries[:10]:

            # Google News RSS titles look like "Headline - Publisher Name"
            # and entry.source.title (when present) holds the publisher.
            source_name = None

            if getattr(entry, "source", None):
                source_name = getattr(
                    entry.source, "title", None
                )

            news_items.append({
                "title": entry.title,
                # entry.link goes through Google News and redirects to
                # the original article on the publisher's site (India
                # Today, Moneycontrol, etc.) when opened in a browser.
                "link": entry.link,
                "source": source_name
            })

        headlines = [
            item["title"] for item in news_items
        ]

        # no news found
        if len(headlines) == 0:

            return empty_news()

        sentiment = \
            analyze_sentiment(
                headlines
            )

        expansion = \
            detect_expansion(
                news_items
            )

        orders = \
            detect_orders(
                news_items
            )

        return {

            "headlines":
            news_items,

            "sentiment":
            sentiment,

            "news_period_score": {

                "1m":
                sentiment,

                "3m":
                sentiment,

                "6m":
                sentiment,

                "1y":
                sentiment,

                "3y":
                sentiment,

                "5y":
                sentiment
            },

            "expansion_news":
            expansion,

            "order_news":
            orders
        }

    except Exception as e:

        print(
            "News Error:",
            e
        )

        return empty_news()


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    company = {

        "company_name":
        "NMDC Limited"
    }

    news = \
        get_news(
            company
        )

    print()

    print(
        type(news)
    )

    print()

    print(
        news
    )
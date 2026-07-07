import { useEffect, useState } from "react";
import { getCompanyNews } from "../../api/api";
import Loader from "../common/Loader";
import "./NewsHighlights.css";

export default function NewsHighlights({ companyName }) {
    const [news, setNews] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getCompanyNews(companyName)
            .then(setNews)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [companyName]);

    if (loading) return <Loader />;
    if (!news) return null;

    const { headlines, sentiment, expansion_news, order_news } = news;

    // headlines/expansion_news/order_news are lists of {title, link, source}.
    // Fall back gracefully in case a plain string ever comes through.
    const renderNewsItem = (item, i, extraClass = "") => {
        const title = typeof item === "string" ? item : item.title;
        const link = typeof item === "string" ? null : item.link;

        if (!link) {
            return (
                <p key={i} className={`news-item ${extraClass}`}>
                    {title}
                </p>
            );
        }

        return (
            <a
                key={i}
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className={`news-item ${extraClass}`}
            >
                {title}
            </a>
        );
    };

    return (
        <div className="news-highlights">
            <div className="news-header">
                <h3>News</h3>
                <span className={`sentiment-badge ${sentiment >= 50 ? "positive" : "negative"}`}>
                    Sentiment: {sentiment}/100
                </span>
            </div>

            {expansion_news.length > 0 && (
                <div className="news-tag-group">
                    <h4>Expansion News</h4>
                    {expansion_news.map((h, i) => renderNewsItem(h, i, "tag-expansion"))}
                </div>
            )}

            {order_news.length > 0 && (
                <div className="news-tag-group">
                    <h4>Order Wins</h4>
                    {order_news.map((h, i) => renderNewsItem(h, i, "tag-order"))}
                </div>
            )}

            <div className="news-tag-group">
                <h4>Recent Headlines</h4>
                {headlines.length === 0 ? (
                    <p className="empty-state">No recent news found.</p>
                ) : (
                    headlines.map((h, i) => renderNewsItem(h, i))
                )}
            </div>
        </div>
    );
}
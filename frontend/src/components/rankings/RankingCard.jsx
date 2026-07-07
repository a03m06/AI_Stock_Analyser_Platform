import { useNavigate } from "react-router-dom";

export default function RankingCard({ company, showScore }) {
    const navigate = useNavigate();

    return (
        <div
            className="ranking-card"
            onClick={() => navigate(`/company/${encodeURIComponent(company.company_name)}`)}
        >
            <div className="ranking-card-header">
                <h3>{company.company_name}</h3>
                <span className="symbol-badge">{company.symbol}</span>
            </div>

            <div className="ranking-card-meta">
                <span>{company.sector}</span>
                <span className="dot">•</span>
                <span>{company.cap_category}</span>
            </div>

            <div className="ranking-card-score">
                {showScore === "ai" && (
                    <span className="score-badge">AI Score: {Number(company.ai_score).toFixed(1)}</span>
                )}
                {showScore === "historical" && (
                    <span className={`score-badge ${company.historical_return >= 0 ? "positive" : "negative"}`}>
                        {Number(company.historical_return).toFixed(2)}% Return
                    </span>
                )}
            </div>
        </div>
    );
}
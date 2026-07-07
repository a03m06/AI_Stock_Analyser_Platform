import { useNavigate } from "react-router-dom";

export default function RankingTable({ companies, loading, showScore }) {
    const navigate = useNavigate();

    if (loading) return <div className="loader">Loading rankings...</div>;

    if (!companies || companies.length === 0) {
        return <div className="empty-state">No companies match these filters.</div>;
    }

    return (
        <div className="ranking-table-wrapper">
            <table className="ranking-table">
                <thead>
                    <tr>
                        <th className="col-rank">#</th>
                        <th className="col-name">Company</th>
                        <th className="col-symbol">Symbol</th>
                        <th className="col-sector">Sector</th>
                        <th className="col-cap">Market Cap</th>
                        <th className="col-score">
                            {showScore === "ai" ? "AI Score" : "Return"}
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {companies.map((c, index) => (
                        <tr
                            key={c.symbol}
                            onClick={() => navigate(`/company/${encodeURIComponent(c.company_name)}`)}
                        >
                            <td className="col-rank">{index + 1}</td>
                            <td className="col-name">{c.company_name}</td>
                            <td className="col-symbol">
                                <span className="symbol-badge">{c.symbol}</span>
                            </td>
                            <td className="col-sector">{c.sector}</td>
                            <td className="col-cap">{c.cap_category}</td>
                            <td className="col-score">
                                {showScore === "ai" && (
                                    <span className="score-badge">
                                        {Number(c.ai_score).toFixed(1)}
                                    </span>
                                )}
                                {showScore === "historical" && (
                                    <span
                                        className={`score-badge ${
                                            c.historical_return >= 0 ? "positive" : "negative"
                                        }`}
                                    >
                                        {c.historical_return >= 0 ? "+" : ""}
                                        {Number(c.historical_return).toFixed(2)}%
                                    </span>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

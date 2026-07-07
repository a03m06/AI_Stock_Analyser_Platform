import { useEffect, useState } from "react";
import Filters from "./Filters";
import RankingTable from "./RankingTable";
import { getAiRanking } from "../../api/api";
import "../../styles/rankings.css";

export default function AIRanking() {
    const [companies, setCompanies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState(false);
    const [filters, setFilters] = useState({
        capCategory: "All", sector: "All", industry: "All"
    });

    useEffect(() => {
        setLoading(true);
        getAiRanking({
            capCategory: filters.capCategory,
            sector: filters.sector,
            industry: filters.industry,
            // Collapsed view: a quick top-3 preview.
            // Expanded view: every company in this category, not just 20.
            topN: expanded ? null : 3
        })
            .then(setCompanies)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [filters, expanded]);

    return (
        <section className="ranking-section">
            <div className="ranking-section-header">
                <h2>
                    Future Multibagger Stocks by AI
                    {expanded && companies.length > 0 && (
                        <span className="ranking-count"> ({companies.length})</span>
                    )}
                </h2>
                <button className="filter-toggle" onClick={() => setExpanded(!expanded)}>
                    {expanded ? "Hide Filters" : "View All & Filter"}
                </button>
            </div>

            {expanded && <Filters showPeriod={false} onChange={setFilters} />}

            <RankingTable companies={companies} loading={loading} showScore="ai" />
        </section>
    );
}
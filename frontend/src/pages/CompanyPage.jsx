import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getCompanyDetails } from "../api/api";
import Loader from "../components/common/Loader";
import CompanyGraph from "../components/company/CompanyGraph";
import Shareholding from "../components/company/Shareholding";
import NewsHighlights from "../components/company/NewsHighlights";
import "./CompanyPage.css";

export default function CompanyPage() {
    const { company: companyName } = useParams();
    const [company, setCompany] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        getCompanyDetails(companyName)
            .then((data) => {
                if (!data) {
                    setError("Company not found.");
                } else {
                    setCompany(data);
                }
            })
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, [companyName]);

    if (loading) return <Loader />;
    if (error) return <div className="empty-state">{error}</div>;
    if (!company) return null;

    return (
        <div className="company-page">
            <div className="company-header">
                <div>
                    <h1>{company.company_name}</h1>
                    <p className="company-meta">
                        {[
                            company.symbol,
                            company.sector,
                            company.industry && company.industry !== company.sector
                                ? company.industry
                                : null,
                            company.cap_category,
                        ]
                            .filter(Boolean)
                            .join(" • ")}
                    </p>
                </div>
                <div className="ai-score-box">
                    <span>AI Score</span>
                    <h2>{Number(company.ai_score).toFixed(1)}</h2>
                </div>
            </div>

            <div className="company-stats-grid">
                <Stat label="Market Cap" value={company.market_cap} suffix=" Cr" />
                <Stat label="ROE" value={company.roe} suffix="%" />
                <Stat label="ROCE" value={company.roce} suffix="%" />
                <Stat label="Debt/Equity" value={company.debt_equity} />
                <Stat label="EPS (12M)" value={company.eps_12m} />
                <Stat label="OPM" value={company.opm} suffix="%" />
                <Stat label="Sales Growth 3Y" value={company.sales_growth_3y} suffix="%" />
                <Stat label="Profit Growth 3Y" value={company.profit_growth_3y} suffix="%" />
                <Stat label="1Y Return" value={company.historical_1y} suffix="%" />
                <Stat label="Promoter Holding" value={company.promoter_holding} suffix="%" />
            </div>

            <CompanyGraph companyName={company.company_name} />
            <Shareholding company={company} />
            <NewsHighlights companyName={company.company_name} />
        </div>
    );
}

function Stat({ label, value, suffix = "" }) {
    return (
        <div className="stat-box">
            <span className="stat-box-label">{label}</span>
            <span className="stat-box-value">{value}{suffix}</span>
        </div>
    );
}
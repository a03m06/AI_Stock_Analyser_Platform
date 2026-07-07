import MarketDashboard
from "../components/dashboard/MarketDashboard";

import HistoricalRanking
from "../components/rankings/HistoricalRanking";

import AIRanking
from "../components/rankings/AIRanking";

import "../styles/app.css";

export default function Home() {

    return (

        <div className="home-page">

            <MarketDashboard />

            <HistoricalRanking />

            <AIRanking />

        </div>
    );
}
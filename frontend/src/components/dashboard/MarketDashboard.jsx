import { useEffect, useState } from "react";
import { getMarketDashboard } from "../../api/api";
import Loader from "../common/Loader";
import "./MarketDashboard.css";

export default function MarketDashboard() {

    const [data, setData] = useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState(null);


    useEffect(() => {

        getMarketDashboard()

            .then(setData)

            .catch(
                (err) =>
                    setError(
                        err.message
                    )
            )

            .finally(
                () =>
                    setLoading(false)
            );

    }, []);


    if (loading)
        return <Loader />;

    if (error)
        return (

            <div className="dashboard-error">

                Failed to load market data:

                {" "}

                {error}

            </div>
        );

    if (!data)
        return null;


    const {

        indices,

        top_gainers,

        top_losers,

        market_sentiment,

        is_live,

        last_updated

    } = data;


    return (

        <div className="market-dashboard">

            <div className="dashboard-top-row">

                <h2 className="dashboard-title">

                    Market Overview

                </h2>


                {
                    is_live && (

                        <span
                            className="live-badge"
                        >

                            <span
                                className="live-dot"
                            />

                            LIVE

                            {
                                last_updated

                                ?

                                ` · updated ${last_updated}`

                                :

                                ""
                            }

                        </span>
                    )
                }

            </div>


            <div className="indices-row">

                {
                    Object.entries(
                        indices
                    ).map(

                        ([name, indexData]) => {

                            const change =
                                typeof indexData === "object"
                                    ? indexData.change
                                    : indexData;

                            const value =
                                typeof indexData === "object"
                                    ? indexData.value
                                    : null;

                            return (

                                <div
                                    className="index-card"
                                    key={name}
                                >

                                    <h3>
                                        {name}
                                    </h3>

                                    <p
                                        className={
                                            change >= 0
                                                ?
                                                "positive"
                                                :
                                                "negative"
                                        }
                                    >

                                        {
                                            change >= 0
                                                ?
                                                "+"
                                                :
                                                ""
                                        }

                                        {change}%

                                    </p>

                                    {
                                        value !== null && (
                                            <span className="index-value-badge">
                                                {value.toLocaleString("en-IN")}
                                            </span>
                                        )
                                    }

                                </div>
                            );
                        }
                    )
                }

            </div>


            <hr className="dashboard-divider" />


            <div className="movers-row">

                <div className="movers-col">

                    <h3 className="section-heading">

                        Top Gainers

                    </h3>

                    {
                        top_gainers.map(
                            (name) => (

                                <p
                                    key={name}
                                >
                                    {name}
                                </p>
                            )
                        )
                    }

                </div>


                <div className="movers-col">

                    <h3 className="section-heading">

                        Top Losers

                    </h3>

                    {
                        top_losers.map(
                            (name) => (

                                <p
                                    key={name}
                                >
                                    {name}
                                </p>
                            )
                        )
                    }

                </div>


                <div className="movers-col sentiment-col">

                    <h3 className="section-heading">

                        Market Sentiment

                    </h3>

                    <h2

                        className={
                            market_sentiment
                                ===
                            "BULLISH"

                                ?

                                "positive"

                                :

                                "negative"
                        }
                    >

                        {
                            market_sentiment
                        }

                    </h2>

                </div>

            </div>

        </div>
    );
}
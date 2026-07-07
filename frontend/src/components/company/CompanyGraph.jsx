import { useEffect, useState } from "react";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
}
from "recharts";

import {
    getCompanyPriceHistory
}
from "../../api/api";

import Loader
from "../common/Loader";

import "./CompanyGraph.css";


const PERIODS = [
    "1m",
    "6m",
    "1y",
    "3y",
    "5y"
];


export default function CompanyGraph({
    companyName
}) {

    const [data,
        setData] = useState([]);

    const [period,
        setPeriod] = useState("1y");

    const [loading,
        setLoading] = useState(true);


    useEffect(() => {

        setLoading(true);

        getCompanyPriceHistory(
            companyName,
            period
        )
        .then(setData)
        .catch(console.error)
        .finally(() =>
            setLoading(false)
        );

    }, [
        companyName,
        period
    ]);


    return (

        <div className="company-graph">

            <div className="graph-header">

                <h3>
                    Price Chart
                </h3>

                <div className="period-tabs">

                    {
                        PERIODS.map(

                            (p) => (

                                <button
                                    key={p}
                                    className={
                                        p === period
                                        ?
                                        "period-tab active"
                                        :
                                        "period-tab"
                                    }
                                    onClick={() =>
                                        setPeriod(p)
                                    }
                                >

                                    {
                                        p.toUpperCase()
                                    }

                                </button>
                            )
                        )
                    }

                </div>

            </div>


            {
                loading
                ?

                <Loader />

                :

                data.length === 0
                ?

                <div className="empty-state">
                    No price data available.
                </div>

                :

                <ResponsiveContainer
                    width="100%"
                    height={320}
                >

                    <LineChart
                        data={data}
                    >

                        <CartesianGrid
                            strokeDasharray="3 3"
                            stroke="#647184"
                        />

                        <XAxis
                            dataKey="date"
                            tick={{
                                fontSize: 11,
                                fill: "#0d0d0e"
                            }}
                            minTickGap={40}
                            tickFormatter={
                                (value) => {

                                    const d =
                                        new Date(
                                            value
                                        );

                                    return d
                                        .toLocaleDateString(
                                            "en-GB",
                                            {
                                                day:
                                                "2-digit",

                                                month:
                                                "2-digit",

                                                year:
                                                "numeric"
                                            }
                                        );
                                }
                            }
                        />

                        <YAxis
                            tick={{
                                fontSize: 14,
                                fill: "#1c1e20"
                            }}
                            domain={[
                                "auto",
                                "auto"
                            ]}
                        />

                        <Tooltip

                            labelFormatter={
                                (value) => {

                                    const d =
                                        new Date(
                                            value
                                        );

                                    return d
                                        .toLocaleDateString(
                                            "en-GB",
                                            {
                                                day:
                                                "2-digit",

                                                month:
                                                "2-digit",

                                                year:
                                                "numeric"
                                            }
                                        );
                                }
                            }

                            contentStyle={{
                                background:
                                "#1e1e1f",

                                border:
                                "1px solid #374151"
                            }}

                            labelStyle={{
                                color:
                                "#ffffff"
                            }}
                        />

                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke="#6366f1"
                            dot={false}
                            strokeWidth={2}
                        />

                    </LineChart>

                </ResponsiveContainer>
            }

        </div>
    );
}
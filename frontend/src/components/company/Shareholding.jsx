import "./Shareholding.css";

export default function Shareholding({ company }) {
    const promoter = Number(company.promoter_holding) || 0;
    const fii = Number(company.fii_holding) || 0;
    const dii = Number(company.dii_holding) || 0;
    const others = Math.max(0, 100 - (promoter + fii + dii));

    const rows = [
        { label: "Promoters", value: promoter, color: "#6366f1" },
        { label: "FIIs", value: fii, color: "#22c55e" },
        { label: "DIIs", value: dii, color: "#eab308" },
        { label: "Public / Others", value: others, color: "#9ca3af" }
    ];

    return (
        <div className="shareholding">
            <h3>Shareholding Pattern</h3>

            <div className="shareholding-bar">
                {rows.map((r) => (
                    <div
                        key={r.label}
                        style={{ width: `${r.value}%`, background: r.color }}
                        title={`${r.label}: ${r.value.toFixed(2)}%`}
                    />
                ))}
            </div>

            <div className="shareholding-legend">
                {rows.map((r) => (
                    <div className="legend-item" key={r.label}>
                        <span className="legend-dot" style={{ background: r.color }} />
                        {r.label}: <strong>{r.value.toFixed(2)}%</strong>
                    </div>
                ))}
            </div>
        </div>
    );
}
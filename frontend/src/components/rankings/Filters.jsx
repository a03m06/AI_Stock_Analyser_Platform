import { useEffect, useState } from "react";
import Select from "react-select";
import { getCaps, getSectors } from "../../api/api";

const PERIOD_OPTIONS = [
    { value: "1m", label: "1 Month" },
    { value: "6m", label: "6 Months" },
    { value: "1y", label: "1 Year" },
    { value: "3y", label: "3 Years" },
    { value: "5y", label: "5 Years" }
];

// Note: "Sector" and "Industry" were removed as separate filters
// because in this dataset they hold identical values for every
// company - showing both was just a duplicate control.

// Keeps dropdown text/options black (instead of react-select's default
// blue) and renders the open menu in a portal with a high z-index so it
// no longer gets hidden behind the sticky table header.
const SELECT_STYLES = {
    control: (base) => ({
        ...base,
        color: "black"
    }),
    singleValue: (base) => ({
        ...base,
        color: "black"
    }),
    option: (base, state) => ({
        ...base,
        color: "black",
        backgroundColor: state.isFocused ? "#e5e7eb" : "white"
    }),
    menuPortal: (base) => ({
        ...base,
        zIndex: 9999
    }),
    menu: (base) => ({
        ...base,
        zIndex: 9999
    })
};

// showPeriod: false for AI Ranking (no period concept), true for Historical Ranking
export default function Filters({ showPeriod = false, onChange }) {
    const [caps, setCaps] = useState([]);
    const [sectors, setSectors] = useState([]);

    const [capCategory, setCapCategory] = useState("All");
    const [sector, setSector] = useState("All");
    const [period, setPeriod] = useState("1y");

    // Load cap categories once
    useEffect(() => {
        getCaps().then(setCaps).catch(console.error);
    }, []);

    // Reload sectors whenever cap category changes
    useEffect(() => {
        getSectors(capCategory).then(setSectors).catch(console.error);
        setSector("All");
    }, [capCategory]);

    // Push combined filter state up whenever anything changes.
    // "industry" is still sent through (mirroring sector) so the
    // backend API contract doesn't need to change.
    useEffect(() => {
        onChange({ capCategory, sector, industry: sector, period });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [capCategory, sector, period]);

    const toOptions = (arr) => [
        { value: "All", label: "All" },
        ...arr.map(v => ({ value: v, label: v }))
    ];

    return (
        <div className="filters-bar">
            <div className="filter-group">
                <label className="filter-label">Market Cap</label>
                <Select
                    className="filter-select"
                    classNamePrefix="filter-select"
                    menuPortalTarget={document.body}
                    styles={SELECT_STYLES}
                    options={toOptions(caps)}
                    value={{ value: capCategory, label: capCategory }}
                    onChange={(opt) => setCapCategory(opt.value)}
                    placeholder="Market Cap"
                />
            </div>

            <div className="filter-group">
                <label className="filter-label">Sector</label>
                <Select
                    className="filter-select"
                    classNamePrefix="filter-select"
                    menuPortalTarget={document.body}
                    styles={SELECT_STYLES}
                    options={toOptions(sectors)}
                    value={{ value: sector, label: sector }}
                    onChange={(opt) => setSector(opt.value)}
                    placeholder="Sector"
                />
            </div>

            {showPeriod && (
                <div className="filter-group">
                    <label className="filter-label">Period</label>
                    <Select
                        className="filter-select"
                        classNamePrefix="filter-select"
                        menuPortalTarget={document.body}
                        styles={SELECT_STYLES}
                        options={PERIOD_OPTIONS}
                        value={PERIOD_OPTIONS.find(p => p.value === period)}
                        onChange={(opt) => setPeriod(opt.value)}
                        placeholder="Period"
                    />
                </div>
            )}
        </div>
    );
}
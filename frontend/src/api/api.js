import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
});

export default api;

// =====================================
// SCREENER / RANKING
// =====================================

export const getCaps = () =>
    api.get("/caps").then(res => res.data.caps);

export const getSectors = (capCategory = "All") =>
    api.get("/sectors", { params: { cap_category: capCategory } })
        .then(res => res.data.sectors);

export const getIndustries = (capCategory = "All", sector = "All") =>
    api.get("/industries", { params: { cap_category: capCategory, sector } })
        .then(res => res.data.industries);

export const getAiRanking = ({ capCategory = "All", sector = "All", industry = "All", topN = null }) =>
    api.get("/ranking/ai", {
        params: {
            cap_category: capCategory,
            sector,
            industry,
            ...(topN != null ? { top_n: topN } : {})
        }
    }).then(res => res.data);

export const getHistoricalRanking = ({ capCategory = "All", sector = "All", industry = "All", period = "1y", topN = null }) =>
    api.get("/ranking/historical", {
        params: {
            cap_category: capCategory,
            sector,
            industry,
            period,
            ...(topN != null ? { top_n: topN } : {})
        }
    }).then(res => res.data);

// =====================================
// DASHBOARD
// =====================================

export const getMarketDashboard = () =>
    api.get("/api/dashboard").then(res => res.data);

// =====================================
// COMPANY
// =====================================

export const getCompanyDetails = (companyName) =>
    api.get(`/company/${encodeURIComponent(companyName)}`).then(res => res.data);

export const getCompanyNews = (companyName) =>
    api.get(`/company/${encodeURIComponent(companyName)}/news`).then(res => res.data);

export const getCompanyPriceHistory = (companyName, period = "1y") =>
    api.get(`/company/${encodeURIComponent(companyName)}/history`, {
        params: { period }
    }).then(res => res.data);
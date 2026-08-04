import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// ─── Articles ────────────────────────────────────────────────────────────────

export const fetchAllArticles = () => api.get("/articles");
export const fetchArticlesByStatus = (status) => api.get(`/status/${status}`);
export const fetchSingleArticle = (hash) => api.get(`/article/${hash}`);

// ─── Stats ───────────────────────────────────────────────────────────────────

export const fetchStats = () => api.get("/stats");

// ─── Actions ─────────────────────────────────────────────────────────────────

export const approveArticle = (hash) => api.post(`/approve/${hash}`);
export const rejectArticle = (hash) => api.post(`/reject/${hash}`);
export const deleteArticle = (hash) => api.delete(`/delete/${hash}`);

// ─── Pipeline ────────────────────────────────────────────────────────────────

export const runPipeline = (city = "Anantapur") =>
  api.post(`/pipeline/run?city=${encodeURIComponent(city)}`);

export default api;
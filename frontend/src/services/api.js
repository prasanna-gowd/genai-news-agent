import axios from "axios";

const api = axios.create({
  baseURL: "https://localpulse-ai-news-agent.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

// ============================
// HEALTH CHECK
// ============================
export const getHealth = async () => {
  const response = await api.get("/");
  return response.data;
};

// ============================
// RUN PIPELINE
// ============================
export const runPipeline = async (city = "Anantapur") => {
  const response = await api.post("/pipeline/run", null, {
    params: {
      city,
    },
  });

  return response.data;
};

// ============================
// FETCH ALL ARTICLES
// ============================
export const fetchAllArticles = async () => {
  const response = await api.get("/articles");
  return response.data;
};

// ============================
// FETCH PENDING ARTICLES
// ============================
export const fetchPendingArticles = async () => {
  const response = await api.get("/pending");
  return response.data;
};

// ============================
// FETCH SINGLE ARTICLE
// ============================
export const fetchArticle = async (articleHash) => {
  const response = await api.get(`/article/${articleHash}`);
  return response.data;
};

// ============================
// APPROVE ARTICLE
// ============================
export const approveArticle = async (articleHash) => {
  const response = await api.post(`/approve/${articleHash}`);
  return response.data;
};

// ============================
// APPROVE ALL ARTICLES
// ============================
export const approveAllArticles = async () => {
  const response = await api.post("/approve-all");
  return response.data;
};

// ============================
// REJECT ARTICLE
// ============================
export const rejectArticle = async (articleHash) => {
  const response = await api.post(`/reject/${articleHash}`);
  return response.data;
};

// ============================
// DELETE ARTICLE
// ============================
export const deleteArticle = async (articleHash) => {
  const response = await api.delete(`/delete/${articleHash}`);
  return response.data;
};

// ============================
// ARTICLES BY STATUS
// ============================
export const fetchArticlesByStatus = async (status) => {
  const response = await api.get(`/status/${status}`);
  return response.data;
};

// ============================
// FETCH STATISTICS
// ============================
export const fetchStats = async () => {
  const response = await api.get("/stats");
  return response.data;
};

// ============================
// DEFAULT AXIOS INSTANCE
// ============================
export default api;
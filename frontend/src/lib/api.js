import axios from "axios";
const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(
    /\/$/,
    "",
  ),
  timeout: 20000,
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("clinic_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
api.interceptors.response.use(
  (r) => r,
  (e) => {
    if (e.response?.status === 401 && !e.config?.url?.includes("/auth/login")) {
      localStorage.removeItem("clinic_token");
      localStorage.removeItem("clinic_user");
      window.location.href = "/login";
    }
    return Promise.reject(e);
  },
);
export default api;
export const apiError = (e) =>
  e.response?.data?.detail || e.message || "Something went wrong";

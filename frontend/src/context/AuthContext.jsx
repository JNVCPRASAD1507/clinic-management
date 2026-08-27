import { createContext, useContext, useEffect, useState } from "react";
import api from "../lib/api";
const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(() =>
    JSON.parse(localStorage.getItem("clinic_user") || "null"),
  );
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const token = localStorage.getItem("clinic_token");

    if (!token) {
      setLoading(false);
      return;
    }

    api
      .get("/auth/me")
      .then((r) => {
        setUser(r.data);
        localStorage.setItem("clinic_user", JSON.stringify(r.data));
      })
      .catch(() => {
        localStorage.removeItem("clinic_token");
        localStorage.removeItem("clinic_user");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);
  const login = async (credentials) => {
    const { data } = await api.post("/auth/login", credentials);
    localStorage.setItem("clinic_token", data.access_token);
    localStorage.setItem("clinic_user", JSON.stringify(data.user));
    setUser(data.user);
  };
  const logout = () => {
    localStorage.removeItem("clinic_token");
    localStorage.removeItem("clinic_user");
    setUser(null);
  };
  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
export const useAuth = () => useContext(AuthContext);

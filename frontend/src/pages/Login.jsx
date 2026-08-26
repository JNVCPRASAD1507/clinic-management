import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { Stethoscope, Eye, EyeOff } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiError } from "../lib/api";
export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();
  const [show, setShow] = useState(false);
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(form);
      nav(loc.state?.from?.pathname || "/", { replace: true });
    } catch (err) {
      setError(apiError(err));
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-700 to-slate-900 p-4">
      <div className="mx-auto grid min-h-[calc(100vh-2rem)] max-w-6xl overflow-hidden rounded-3xl bg-white shadow-2xl lg:grid-cols-2">
        <div className="hidden bg-brand-900 p-12 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <div className="mb-10 flex items-center gap-3 text-xl font-bold">
              <span className="grid h-10 w-10 place-items-center rounded-xl bg-white/10">
                <Stethoscope />
              </span>
              CareFlow Clinic
            </div>
            <h1 className="max-w-md text-4xl font-bold leading-tight">
              A calmer way to run your clinic.
            </h1>
            <p className="mt-5 max-w-md text-brand-100">
              Appointments, patients, doctors and medical records in one secure
              workspace.
            </p>
          </div>
          <p className="text-sm text-brand-200">
            Clinic Management System · Production workspace
          </p>
        </div>
        <div className="flex items-center p-6 sm:p-12">
          <div className="mx-auto w-full max-w-md">
            <div className="mb-8 lg:hidden flex items-center gap-2 font-bold">
              <span className="grid h-9 w-9 place-items-center rounded-xl bg-brand-700 text-white">
                <Stethoscope size={18} />
              </span>
              CareFlow Clinic
            </div>
            <h2 className="text-3xl font-bold text-slate-900">Welcome back</h2>
            <p className="mt-2 text-sm text-slate-500">
              Sign in to access your clinic workspace.
            </p>
            {error && (
              <div className="mt-5 rounded-xl bg-red-50 p-3 text-sm text-red-700">
                {error}
              </div>
            )}
            <form onSubmit={submit} className="mt-7 space-y-5">
              <div>
                <label className="label">Email</label>
                <input
                  required
                  type="email"
                  className="input"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  placeholder="you@clinic.com"
                />
              </div>
              <div>
                <label className="label">Password</label>
                <div className="relative">
                  <input
                    required
                    type={show ? "text" : "password"}
                    className="input pr-10"
                    value={form.password}
                    onChange={(e) =>
                      setForm({ ...form, password: e.target.value })
                    }
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShow(!show)}
                    className="absolute right-3 top-2.5 text-slate-400"
                  >
                    {show ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>
              <button disabled={busy} className="btn-primary w-full">
                {busy ? "Signing in…" : "Sign in"}
              </button>
            </form>
            <p className="mt-6 text-center text-sm text-slate-500">
              Need an account?{" "}
              <Link to="/register" className="font-semibold text-brand-700">
                Create one
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

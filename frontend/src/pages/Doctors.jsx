import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import api, { apiError } from "../lib/api";
import PageHeader from "../components/PageHeader";
import Modal from "../components/Modal";
import { useAuth } from "../context/AuthContext";
const blank = {
  // user_id: "",
  full_name: "",
  specialization: "",
  qualification: "",
  phone: "",
  email: "",
  password: "",
  consultation_fee: "",
  available_timings: "09:00 AM - 05:00 PM",
};
export default function Doctors() {
  const { user } = useAuth();
  const [items, setItems] = useState([]),
    [open, setOpen] = useState(false),
    [form, setForm] = useState(blank),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const load = async () => {
    try {
      const response = await api.get("/doctors");
      setItems(response.data);
    } catch (e) {
      setError(apiError(e));
    }
  };

  useEffect(() => {
    load();
  }, []);
  const save = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.post("/doctors", {
        ...form,
        consultation_fee: Number(form.consultation_fee),
      });
      setOpen(false);
      setForm(blank);
      load();
    } catch (e) {
      setError(apiError(e));
    } finally {
      setBusy(false);
    }
  };
  const remove = async (id) => {
    if (!confirm("Delete this doctor?")) return;
    try {
      await api.delete(`/doctors/${id}`);
      load();
    } catch (e) {
      setError(apiError(e));
    }
  };
  return (
    <>
      <PageHeader
        title="Doctors"
        description="Manage clinical staff, qualifications and availability."
        action={
          user.role === "Admin" && (
            <button className="btn-primary" onClick={() => setOpen(true)}>
              <Plus size={17} />
              Add doctor
            </button>
          )
        }
      />
      {error && (
        <div className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((d) => (
          <div className="card p-5" key={d.id}>
            <div className="flex items-start justify-between">
              <div className="grid h-12 w-12 place-items-center rounded-2xl bg-brand-50 font-bold text-brand-700">
                {d.full_name.slice(0, 1)}
              </div>
              {user.role === "Admin" && (
                <button
                  className="btn-danger px-2.5"
                  onClick={() => remove(d.id)}
                >
                  <Trash2 size={15} />
                </button>
              )}
            </div>
            <h2 className="mt-4 font-bold">{d.full_name}</h2>
            <p className="text-sm font-medium text-brand-700">
              {d.specialization}
            </p>
            <div className="mt-4 space-y-2 text-sm text-slate-500">
              <p>{d.qualification}</p>
              <p>{d.phone}</p>
              <p>{d.email}</p>
              <p>
                ₹{d.consultation_fee} · {d.available_timings}
              </p>
            </div>
          </div>
        ))}
      </div>
      <Modal open={open} onClose={() => setOpen(false)} title="Add doctor">
        <form onSubmit={save} className="grid gap-4 sm:grid-cols-2">
          {[
            ["full_name", "Full name"],
            ["specialization", "Specialization"],
            ["qualification", "Qualification"],
            ["phone", "Phone"],
            ["email", "Email"],
            ["password", "Login password"],
            ["consultation_fee", "Consultation fee"],
            ["available_timings", "Available timings"],
          ].map(([k, l]) => (
            <div key={k}>
              <label className="label">{l}</label>
              <input
                required={k !== "user_id"}
                type={
                  k === "consultation_fee" || k === "user_id"
                    ? "number"
                    : k === "email"
                      ? "email"
                      : "text"
                }
                className="input"
                value={form[k]}
                onChange={(e) => setForm({ ...form, [k]: e.target.value })}
              />
            </div>
          ))}
          <button disabled={busy} className="btn-primary sm:col-span-2">
            {busy ? "Saving…" : "Save doctor"}
          </button>
        </form>
      </Modal>
    </>
  );
}

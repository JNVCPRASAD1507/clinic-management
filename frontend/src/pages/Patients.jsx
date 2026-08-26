import { useEffect, useState } from "react";
import { Plus, Search, Trash2 } from "lucide-react";
import api, { apiError } from "../lib/api";
import PageHeader from "../components/PageHeader";
import Modal from "../components/Modal";
import { useAuth } from "../context/AuthContext";
const blank = {
  full_name: "",
  age: "",
  gender: "Male",
  phone: "",
  address: "",
  blood_group: "",
  emergency_contact: "",
};
export default function Patients() {
  const { user } = useAuth();
  const [items, setItems] = useState([]),
    [q, setQ] = useState(""),
    [open, setOpen] = useState(false),
    [form, setForm] = useState(blank),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const load = async () => {
    try {
      const response = await api.get("/patients");
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
      await api.post("/patients", { ...form, age: Number(form.age) });
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
    if (!confirm("Delete this patient?")) return;
    try {
      await api.delete(`/patients/${id}`);
      load();
    } catch (e) {
      setError(apiError(e));
    }
  };
  const filtered = items.filter((x) =>
    `${x.full_name} ${x.phone}`.toLowerCase().includes(q.toLowerCase()),
  );
  return (
    <>
      <PageHeader
        title="Patients"
        description="Manage patient profiles and emergency information."
        action={
          (user.role === "Admin" || user.role === "Receptionist") && (
            <button className="btn-primary" onClick={() => setOpen(true)}>
              <Plus size={17} />
              Add patient
            </button>
          )
        }
      />
      {error && (
        <div className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}
      <div className="card overflow-hidden">
        <div className="border-b p-4">
          <div className="relative max-w-sm">
            <Search
              size={17}
              className="absolute left-3 top-3 text-slate-400"
            />
            <input
              className="input pl-9"
              placeholder="Search patients…"
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-5 py-3">Patient</th>
                <th className="px-5 py-3">Age / Gender</th>
                <th className="px-5 py-3">Phone</th>
                <th className="px-5 py-3">Blood group</th>
                {user.role === "Admin" && <th />}
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-t">
                  <td className="px-5 py-4">
                    <div className="font-semibold">{p.full_name}</div>
                    <div className="text-xs text-slate-500">#{p.id}</div>
                  </td>
                  <td className="px-5 py-4">
                    {p.age} / {p.gender}
                  </td>
                  <td className="px-5 py-4">{p.phone}</td>
                  <td className="px-5 py-4">{p.blood_group || "—"}</td>
                  {user.role === "Admin" && (
                    <td className="px-5 py-4 text-right">
                      <button
                        className="btn-danger px-2.5"
                        onClick={() => remove(p.id)}
                      >
                        <Trash2 size={15} />
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <Modal open={open} onClose={() => setOpen(false)} title="Add patient">
        <form onSubmit={save} className="grid gap-4 sm:grid-cols-2">
          {[
            ["full_name", "Full name"],
            ["age", "Age"],
            ["phone", "Phone"],
            ["emergency_contact", "Emergency contact"],
            ["blood_group", "Blood group"],
          ].map(([k, l]) => (
            <div key={k}>
              <label className="label">{l}</label>
              <input
                required={k !== "blood_group"}
                className="input"
                value={form[k]}
                onChange={(e) => setForm({ ...form, [k]: e.target.value })}
              />
            </div>
          ))}
          <div>
            <label className="label">Gender</label>
            <select
              className="input"
              value={form.gender}
              onChange={(e) => setForm({ ...form, gender: e.target.value })}
            >
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <div className="sm:col-span-2">
            <label className="label">Address</label>
            <textarea
              required
              className="input min-h-24"
              value={form.address}
              onChange={(e) => setForm({ ...form, address: e.target.value })}
            />
          </div>
          <button disabled={busy} className="btn-primary sm:col-span-2">
            {busy ? "Saving…" : "Save patient"}
          </button>
        </form>
      </Modal>
    </>
  );
}

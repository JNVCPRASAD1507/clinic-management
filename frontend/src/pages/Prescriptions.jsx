import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import api, { apiError } from "../lib/api";
import PageHeader from "../components/PageHeader";
import Modal from "../components/Modal";
import { useAuth } from "../context/AuthContext";
const blank = {
  appointment_id: "",
  diagnosis: "",
  medicines: "",
  dosage: "",
  instructions: "",
  follow_up_date: "",
};
export default function Prescriptions() {
  const { user } = useAuth();
  const [items, setItems] = useState([]),
    [appointments, setAppointments] = useState([]),
    [patients, setPatients] = useState([]),
    [doctors, setDoctors] = useState([]),
    [open, setOpen] = useState(false),
    [form, setForm] = useState(blank),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const load = () =>
    api
      .get("/prescriptions")
      .then((r) => setItems(r.data))
      .catch((e) => setError(apiError(e)));
  useEffect(() => {
    load();
    Promise.all([
      api.get("/appointments?page=1&page_size=100"),
      api.get("/patients"),
      api.get("/doctors"),
    ])
      .then(([a, p, d]) => {
        setAppointments(a.data.filter((x) => x.status === "Completed"));
        setPatients(p.data);
        setDoctors(d.data);
      })
      .catch((e) => setError(apiError(e)));
  }, []);
  const save = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.post("/prescriptions", {
        ...form,
        appointment_id: Number(form.appointment_id),
        follow_up_date: form.follow_up_date || null,
        instructions: form.instructions || null,
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
  return (
    <>
      <PageHeader
        title="Prescriptions"
        description="Clinical prescriptions linked to completed appointments."
        action={
          user.role === "Doctor" && (
            <button className="btn-primary" onClick={() => setOpen(true)}>
              <Plus size={17} />
              New prescription
            </button>
          )
        }
      />
      {error && (
        <div className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}
      <div className="grid gap-4 lg:grid-cols-2">
        {items.map((p) => (
          <div className="card p-5" key={p.id}>
            <div className="flex justify-between">
              <div>
                <p className="text-xs font-bold uppercase text-brand-700">
                  Prescription #{p.id}
                </p>
                <h2 className="mt-1 font-bold">
                  {patients.find((x) => x.id === p.patient_id)?.full_name ||
                    `Patient #${p.patient_id}`}
                </h2>
              </div>
              <span className="text-xs text-slate-500">
                {p.follow_up_date || "No follow-up"}
              </span>
            </div>
            <div className="mt-4 space-y-2 text-sm">
              <p>
                <b>Diagnosis:</b> {p.diagnosis}
              </p>
              <p>
                <b>Medicines:</b> {p.medicines}
              </p>
              <p>
                <b>Dosage:</b> {p.dosage}
              </p>
              {p.instructions && (
                <p>
                  <b>Instructions:</b> {p.instructions}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Create prescription"
      >
        <form onSubmit={save} className="space-y-4">
          <div>
            <label className="label">Completed appointment</label>
            <select
              required
              className="input"
              value={form.appointment_id}
              onChange={(e) =>
                setForm({ ...form, appointment_id: e.target.value })
              }
            >
              <option value="">Select appointment</option>
              {appointments.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.appointment_number} ·{" "}
                  {patients.find((p) => p.id === a.patient_id)?.full_name ||
                    "Patient"}{" "}
                  · {a.appointment_date}
                </option>
              ))}
            </select>
          </div>
          {[
            ["diagnosis", "Diagnosis"],
            ["medicines", "Medicines"],
            ["dosage", "Dosage"],
            ["instructions", "Instructions"],
          ].map(([k, l]) => (
            <div key={k}>
              <label className="label">{l}</label>
              <textarea
                className="input min-h-20"
                required={k !== "instructions"}
                value={form[k]}
                onChange={(e) => setForm({ ...form, [k]: e.target.value })}
              />
            </div>
          ))}
          <div>
            <label className="label">Follow-up date</label>
            <input
              type="date"
              className="input"
              value={form.follow_up_date}
              onChange={(e) =>
                setForm({ ...form, follow_up_date: e.target.value })
              }
            />
          </div>
          <button disabled={busy} className="btn-primary w-full">
            {busy ? "Saving…" : "Save prescription"}
          </button>
        </form>
      </Modal>
    </>
  );
}

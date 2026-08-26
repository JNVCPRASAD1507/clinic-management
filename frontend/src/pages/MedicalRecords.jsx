import { useEffect, useState } from "react";
import { Download, Upload } from "lucide-react";
import api, { apiError } from "../lib/api";
import PageHeader from "../components/PageHeader";
import { useAuth } from "../context/AuthContext";
export default function MedicalRecords() {
  const { user } = useAuth();
  const [patients, setPatients] = useState([]),
    [patientId, setPatientId] = useState(""),
    [records, setRecords] = useState([]),
    [file, setFile] = useState(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  useEffect(() => {
    api
      .get("/patients")
      .then((r) => setPatients(r.data))
      .catch((e) => setError(apiError(e)));
  }, []);
  const load = async (id) => {
    setPatientId(id);
    if (!id) {
      setRecords([]);
      return;
    }
    try {
      const r = await api.get(`/medical-records/${id}`);
      setRecords(r.data);
    } catch (e) {
      setError(apiError(e));
    }
  };
  const upload = async (e) => {
    e.preventDefault();
    if (!file || !patientId) return;
    setBusy(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      await api.post(`/medical-records/upload?patient_id=${patientId}`, fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      await load(patientId);
    } catch (e) {
      setError(apiError(e));
    } finally {
      setBusy(false);
    }
  };
  const download = async (r) => {
    try {
      const res = await api.get(`/medical-records/download/${r.id}`, {
        responseType: "blob",
      });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = r.file_name;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(apiError(e));
    }
  };
  return (
    <>
      <PageHeader
        title="Medical Records"
        description="Upload and securely retrieve patient reports."
      />
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="card p-5">
          <label className="label">Select patient</label>
          <select
            className="input"
            value={patientId}
            onChange={(e) => load(e.target.value)}
          >
            <option value="">Choose patient</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.full_name}
              </option>
            ))}
          </select>
          {patientId && (
            <form onSubmit={upload} className="mt-6 space-y-3">
              <label className="label">Upload PDF / JPG / PNG</label>
              <input
                required
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="block w-full text-sm"
              />
              <button disabled={busy || !file} className="btn-primary w-full">
                <Upload size={16} />
                {busy ? "Uploading…" : "Upload record"}
              </button>
            </form>
          )}
        </div>
        <div className="lg:col-span-2">
          {error && (
            <div className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}
          <div className="card divide-y">
            {!patientId ? (
              <div className="p-10 text-center text-sm text-slate-500">
                Select a patient to view records.
              </div>
            ) : records.length === 0 ? (
              <div className="p-10 text-center text-sm text-slate-500">
                No medical records found.
              </div>
            ) : (
              records.map((r) => (
                <div
                  className="flex items-center justify-between gap-4 p-4"
                  key={r.id}
                >
                  <div>
                    <p className="font-semibold">{r.file_name}</p>
                    <p className="text-xs text-slate-500">
                      {r.file_type.toUpperCase()} ·{" "}
                      {new Date(r.uploaded_at).toLocaleString()}
                    </p>
                  </div>
                  <button className="btn-secondary" onClick={() => download(r)}>
                    <Download size={16} />
                    Download
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </>
  );
}

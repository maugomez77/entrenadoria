import { useEffect, useState } from "react";
import { api, type Client, type FormAnalysis } from "../api";
import { useI18n } from "../i18n";

export default function Form() {
  const { t, lang } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [list, setList] = useState<FormAnalysis[]>([]);
  const [form, setForm] = useState({ client_id: "", exercise: "", description: "" });
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    const [c, f] = await Promise.all([api.get<Client[]>("/clients"), api.get<FormAnalysis[]>("/form-analyses")]);
    setClients(c.data); setList(f.data);
    if (!form.client_id && c.data.length) setForm((f) => ({ ...f, client_id: c.data[0].id }));
  };
  useEffect(() => { refresh(); }, []);

  const analyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/ai/form", { ...form, language: lang });
      setForm({ ...form, exercise: "", description: "" });
      refresh();
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h1 className="page-title">{t.form.title}</h1>
      <p className="page-sub">{t.form.sub}</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: 24 }}>
        <div className="card">
          <form className="form" onSubmit={analyze}>
            <label>{t.clients.name}
              <select value={form.client_id} onChange={(e) => setForm({ ...form, client_id: e.target.value })}>
                {clients.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </label>
            <label>{t.form.exercise}
              <input required value={form.exercise} onChange={(e) => setForm({ ...form, exercise: e.target.value })} />
            </label>
            <label>{t.form.desc}
              <textarea required rows={4} value={form.description}
                        onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </label>
            <button className="btn" disabled={loading} type="submit">
              {loading ? t.common.loading : t.form.analyze}
            </button>
          </form>
        </div>

        <div className="card">
          <table className="table">
            <thead><tr>
              <th>{t.form.exercise}</th><th>{t.form.score}</th>
              <th>{t.form.issues}</th><th>{t.form.corrections}</th>
            </tr></thead>
            <tbody>
              {list.map((f) => (
                <tr key={f.id}>
                  <td>{f.exercise}</td>
                  <td><span className={"badge " + (f.score >= 7 ? "badge-ok" : "badge-warn")}>{f.score}/10</span></td>
                  <td>{f.issues.join("; ")}</td>
                  <td>{f.corrections.join("; ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

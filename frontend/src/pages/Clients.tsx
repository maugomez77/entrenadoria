import { useEffect, useState } from "react";
import { api, type Client } from "../api";
import { useI18n } from "../i18n";

export default function Clients() {
  const { t } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [form, setForm] = useState({ name: "", phone: "", age: 30, goal: "general_fitness",
                                       level: "beginner", injuries: "", notes: "" });

  const refresh = async () => {
    const r = await api.get<Client[]>("/clients");
    setClients(r.data);
  };
  useEffect(() => { refresh(); }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/clients", form);
    setForm({ name: "", phone: "", age: 30, goal: "general_fitness",
              level: "beginner", injuries: "", notes: "" });
    refresh();
  };

  return (
    <div>
      <h1 className="page-title">{t.clients.title}</h1>
      <p className="page-sub">{t.clients.sub}</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.clients.add}</h3>
          <form className="form" onSubmit={submit}>
            <label>{t.clients.name}
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </label>
            <label>{t.clients.phone}
              <input required value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            </label>
            <label>{t.clients.age}
              <input type="number" value={form.age} onChange={(e) => setForm({ ...form, age: +e.target.value })} />
            </label>
            <label>{t.clients.goal}
              <select value={form.goal} onChange={(e) => setForm({ ...form, goal: e.target.value })}>
                {Object.entries(t.goals).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </label>
            <label>{t.clients.level}
              <select value={form.level} onChange={(e) => setForm({ ...form, level: e.target.value })}>
                {Object.entries(t.levels).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </label>
            <label>{t.clients.injuries}
              <input value={form.injuries} onChange={(e) => setForm({ ...form, injuries: e.target.value })} />
            </label>
            <label>{t.clients.notes}
              <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
            </label>
            <button className="btn" type="submit">{t.clients.save}</button>
          </form>
        </div>

        <div className="card">
          <table className="table">
            <thead><tr>
              <th>{t.clients.name}</th><th>{t.clients.goal}</th>
              <th>{t.clients.level}</th><th>{t.clients.phone}</th>
            </tr></thead>
            <tbody>
              {clients.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td><span className="badge">{c.goal}</span></td>
                  <td>{c.level}</td>
                  <td>{c.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

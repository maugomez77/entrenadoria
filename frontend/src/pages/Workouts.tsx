import { useEffect, useState } from "react";
import { api, type Client, type Workout } from "../api";
import { useI18n } from "../i18n";

export default function Workouts() {
  const { t, lang } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [clientId, setClientId] = useState("");
  const [duration, setDuration] = useState(45);
  const [workoutLang, setWorkoutLang] = useState<"es" | "en">(lang);
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    const [c, w] = await Promise.all([api.get<Client[]>("/clients"), api.get<Workout[]>("/workouts")]);
    setClients(c.data); setWorkouts(w.data);
    if (!clientId && c.data.length) setClientId(c.data[0].id);
  };
  useEffect(() => { refresh(); }, []);

  const generate = async () => {
    if (!clientId) return;
    setLoading(true);
    try {
      await api.post("/ai/workout", { client_id: clientId, duration_minutes: duration, language: workoutLang });
      await refresh();
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h1 className="page-title">{t.workouts.title}</h1>
      <p className="page-sub">{t.workouts.sub}</p>

      <div className="card" style={{ marginBottom: 20 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "end", flexWrap: "wrap" }}>
          <label>{t.workouts.forClient}
            <select value={clientId} onChange={(e) => setClientId(e.target.value)}>
              {clients.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </label>
          <label>{t.workouts.duration}
            <input type="number" value={duration} onChange={(e) => setDuration(+e.target.value)} />
          </label>
          <label>{t.workouts.language}
            <select value={workoutLang} onChange={(e) => setWorkoutLang(e.target.value as "es" | "en")}>
              <option value="es">Español</option><option value="en">English</option>
            </select>
          </label>
          <button className="btn" disabled={loading} onClick={generate}>
            {loading ? t.common.loading : t.workouts.generate}
          </button>
        </div>
      </div>

      <div className="grid grid-3">
        {workouts.map((w) => (
          <div key={w.id} className="card">
            <h3 style={{ color: "var(--text)" }}>{w.title}</h3>
            <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 8 }}>
              {w.focus} · {w.duration_minutes} min · {w.language.toUpperCase()}
            </div>
            <table className="table">
              <tbody>
                {w.exercises.map((ex, i) => (
                  <tr key={i}>
                    <td>{ex.name}</td>
                    <td style={{ textAlign: "right" }}>{ex.sets}×{ex.reps}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import { api, type Client, type Appointment, type Message } from "../api";
import { useI18n } from "../i18n";

export default function Dashboard() {
  const { t } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [appts, setAppts] = useState<Appointment[]>([]);
  const [msgs, setMsgs] = useState<Message[]>([]);
  const [workoutCount, setWorkoutCount] = useState(0);

  useEffect(() => {
    (async () => {
      try {
        const [c, a, m, w] = await Promise.all([
          api.get<Client[]>("/clients"),
          api.get<Appointment[]>("/appointments"),
          api.get<Message[]>("/messages"),
          api.get("/workouts"),
        ]);
        setClients(c.data); setAppts(a.data); setMsgs(m.data);
        setWorkoutCount(w.data.length);
      } catch {}
    })();
  }, []);

  const upcoming = appts.filter((a) => new Date(a.when) > new Date() && a.status === "scheduled").length;
  const goalCounts = clients.reduce<Record<string, number>>((acc, c) => {
    acc[c.goal] = (acc[c.goal] || 0) + 1; return acc;
  }, {});

  return (
    <div>
      <h1 className="page-title">{t.dash.title}</h1>
      <p className="page-sub">{t.dash.sub}</p>
      <div className="grid grid-4">
        <div className="card"><h3>{t.dash.totalClients}</h3><div className="big">{clients.length}</div></div>
        <div className="card"><h3>{t.dash.totalWorkouts}</h3><div className="big">{workoutCount}</div></div>
        <div className="card"><h3>{t.dash.upcoming}</h3><div className="big">{upcoming}</div></div>
        <div className="card"><h3>{t.dash.messages}</h3><div className="big">{msgs.length}</div></div>
      </div>

      <div className="grid grid-3" style={{ marginTop: 24 }}>
        <div className="card">
          <h3>{t.dash.byGoal}</h3>
          <table className="table">
            <tbody>
              {Object.entries(goalCounts).map(([k, v]) => (
                <tr key={k}><td>{k}</td><td style={{ textAlign: "right" }}>{v}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card" style={{ gridColumn: "span 2" }}>
          <h3>{t.dash.recentClients}</h3>
          <table className="table">
            <thead><tr><th>{t.clients.name}</th><th>{t.clients.goal}</th><th>{t.clients.level}</th></tr></thead>
            <tbody>
              {clients.slice(0, 5).map((c) => (
                <tr key={c.id}><td>{c.name}</td><td>{c.goal}</td><td>{c.level}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

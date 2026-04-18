import { useEffect, useState } from "react";
import { api, type Appointment, type Client } from "../api";
import { useI18n } from "../i18n";

export default function Schedule() {
  const { t } = useI18n();
  const [appts, setAppts] = useState<Appointment[]>([]);
  const [clients, setClients] = useState<Client[]>([]);

  useEffect(() => {
    (async () => {
      const [a, c] = await Promise.all([api.get<Appointment[]>("/appointments"), api.get<Client[]>("/clients")]);
      setAppts(a.data); setClients(c.data);
    })();
  }, []);

  const names = Object.fromEntries(clients.map((c) => [c.id, c.name]));

  return (
    <div>
      <h1 className="page-title">{t.schedule.title}</h1>
      <p className="page-sub">{t.schedule.sub}</p>
      <div className="card">
        <table className="table">
          <thead><tr>
            <th>{t.schedule.when}</th><th>{t.schedule.client}</th>
            <th>{t.schedule.location}</th><th>{t.schedule.status}</th>
          </tr></thead>
          <tbody>
            {appts.map((a) => (
              <tr key={a.id}>
                <td>{new Date(a.when).toLocaleString()}</td>
                <td>{names[a.client_id] || a.client_id}</td>
                <td>{a.location}</td>
                <td><span className="badge">{a.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import { api, type Client, type Message } from "../api";
import { useI18n } from "../i18n";

export default function WhatsApp() {
  const { t, lang } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState("");
  const [msgs, setMsgs] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const r = await api.get<Client[]>("/clients");
      setClients(r.data);
      if (r.data.length) setClientId(r.data[0].id);
    })();
  }, []);

  useEffect(() => {
    if (!clientId) return;
    (async () => {
      const r = await api.get<Message[]>(`/messages?client_id=${clientId}`);
      setMsgs(r.data);
    })();
  }, [clientId]);

  const send = async (direction: "in" | "out", body: string) => {
    if (!body.trim()) return;
    await api.post("/messages", { client_id: clientId, direction, body });
    setDraft("");
    const r = await api.get<Message[]>(`/messages?client_id=${clientId}`);
    setMsgs(r.data);
  };

  const suggest = async () => {
    const lastIn = [...msgs].reverse().find((m) => m.direction === "in");
    if (!lastIn) return;
    setLoading(true);
    try {
      const r = await api.post<{ suggestion: string }>("/ai/reply", {
        client_id: clientId, last_message: lastIn.body, language: lang,
      });
      setSuggestion(r.data.suggestion);
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h1 className="page-title">{t.wa.title}</h1>
      <p className="page-sub">{t.wa.sub}</p>

      <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", gap: 20 }}>
        <div className="card" style={{ padding: 8 }}>
          {clients.map((c) => (
            <div key={c.id}
                 onClick={() => setClientId(c.id)}
                 style={{
                   padding: "10px 12px", borderRadius: 6, cursor: "pointer",
                   background: c.id === clientId ? "var(--card-2)" : "transparent",
                 }}>
              <div style={{ fontSize: 14 }}>{c.name}</div>
              <div style={{ fontSize: 11, color: "var(--muted)" }}>{c.phone}</div>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="chat" style={{ marginBottom: 16 }}>
            {msgs.map((m) => (
              <div key={m.id}>
                <div className={"msg " + m.direction}>{m.body}</div>
                <div className="ts">{new Date(m.sent_at).toLocaleString()}</div>
              </div>
            ))}
          </div>

          {suggestion && (
            <div className="card" style={{ background: "var(--card-2)", marginBottom: 12 }}>
              <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 6 }}>{t.wa.suggest}</div>
              <div style={{ marginBottom: 8 }}>{suggestion}</div>
              <button className="btn" onClick={() => { setDraft(suggestion); setSuggestion(""); }}>
                {t.wa.reply}
              </button>
            </div>
          )}

          <div style={{ display: "flex", gap: 8 }}>
            <input
              style={{ flex: 1, background: "var(--bg)", color: "var(--text)",
                       border: "1px solid var(--border)", padding: 10, borderRadius: 6 }}
              placeholder={t.wa.message}
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") send("out", draft); }}
            />
            <button className="btn-secondary btn" onClick={suggest} disabled={loading}>
              {loading ? "..." : t.wa.suggest}
            </button>
            <button className="btn" onClick={() => send("out", draft)}>{t.wa.send}</button>
          </div>
        </div>
      </div>
    </div>
  );
}

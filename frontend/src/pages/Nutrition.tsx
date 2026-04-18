import { useEffect, useState } from "react";
import { api, type Client, type Nutrition } from "../api";
import { useI18n } from "../i18n";

export default function NutritionPage() {
  const { t, lang } = useI18n();
  const [clients, setClients] = useState<Client[]>([]);
  const [plans, setPlans] = useState<Nutrition[]>([]);
  const [form, setForm] = useState({ client_id: "", weight_kg: 75, activity_level: "moderate" });
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    const [c, n] = await Promise.all([api.get<Client[]>("/clients"), api.get<Nutrition[]>("/nutrition-plans")]);
    setClients(c.data); setPlans(n.data);
    if (!form.client_id && c.data.length) setForm((f) => ({ ...f, client_id: c.data[0].id }));
  };
  useEffect(() => { refresh(); }, []);

  const generate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/ai/nutrition", { ...form, language: lang });
      refresh();
    } finally { setLoading(false); }
  };

  return (
    <div>
      <h1 className="page-title">{t.nutrition.title}</h1>
      <p className="page-sub">{t.nutrition.sub}</p>

      <div className="card" style={{ marginBottom: 20 }}>
        <form className="form" style={{ gridTemplateColumns: "repeat(4, 1fr)", display: "grid", maxWidth: "none" }} onSubmit={generate}>
          <label>{t.clients.name}
            <select value={form.client_id} onChange={(e) => setForm({ ...form, client_id: e.target.value })}>
              {clients.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </label>
          <label>{t.nutrition.weight}
            <input type="number" step="0.1" value={form.weight_kg}
                   onChange={(e) => setForm({ ...form, weight_kg: +e.target.value })} />
          </label>
          <label>{t.nutrition.activity}
            <select value={form.activity_level} onChange={(e) => setForm({ ...form, activity_level: e.target.value })}>
              <option value="sedentary">sedentary</option>
              <option value="moderate">moderate</option>
              <option value="high">high</option>
            </select>
          </label>
          <button className="btn" type="submit" disabled={loading} style={{ alignSelf: "end" }}>
            {loading ? t.common.loading : t.nutrition.generate}
          </button>
        </form>
      </div>

      <div className="grid grid-3">
        {plans.map((p) => (
          <div key={p.id} className="card">
            <h3>{p.daily_calories} {t.nutrition.kcal}</h3>
            <div style={{ fontSize: 13, marginBottom: 8 }}>
              {t.nutrition.protein} {p.protein_g}g · {t.nutrition.carbs} {p.carbs_g}g · {t.nutrition.fats} {p.fats_g}g
            </div>
            <div style={{ fontSize: 12, color: "var(--muted)", marginBottom: 4 }}>{t.nutrition.meals}:</div>
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13 }}>
              {p.meal_ideas.map((m, i) => <li key={i}>{m}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

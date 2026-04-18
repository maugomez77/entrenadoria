import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

export type Lang = "es" | "en";

type Dict = {
  brand: string;
  brandSub: string;
  nav: {
    dashboard: string; clients: string; workouts: string; form: string;
    nutrition: string; schedule: string; whatsapp: string;
  };
  dash: {
    title: string; sub: string;
    totalClients: string; totalWorkouts: string; upcoming: string; messages: string;
    byGoal: string; recentClients: string;
  };
  clients: {
    title: string; sub: string; add: string; name: string; phone: string; age: string;
    goal: string; level: string; injuries: string; notes: string; save: string;
  };
  workouts: {
    title: string; sub: string; generate: string; duration: string; language: string;
    forClient: string; title2: string; focus: string;
  };
  form: {
    title: string; sub: string; exercise: string; desc: string; analyze: string;
    issues: string; corrections: string; score: string;
  };
  nutrition: {
    title: string; sub: string; weight: string; activity: string; generate: string;
    kcal: string; protein: string; carbs: string; fats: string; meals: string;
  };
  schedule: { title: string; sub: string; when: string; client: string; location: string; status: string };
  wa: { title: string; sub: string; thread: string; reply: string; suggest: string; send: string; message: string };
  goals: { weight_loss: string; muscle_gain: string; endurance: string; rehabilitation: string; general_fitness: string };
  levels: { beginner: string; intermediate: string; advanced: string };
  common: { loading: string; error: string; noData: string; selectClient: string };
};

const es: Dict = {
  brand: "EntrenadorIA",
  brandSub: "WhatsApp AI Coach — Morelia",
  nav: { dashboard: "Panel", clients: "Clientes", workouts: "Rutinas",
         form: "Análisis de técnica", nutrition: "Nutrición",
         schedule: "Agenda", whatsapp: "WhatsApp" },
  dash: { title: "Panel principal", sub: "Resumen de tu negocio",
          totalClients: "Clientes activos", totalWorkouts: "Rutinas creadas",
          upcoming: "Próximas sesiones", messages: "Mensajes",
          byGoal: "Por meta", recentClients: "Clientes recientes" },
  clients: { title: "Clientes", sub: "Administra tu cartera",
             add: "Agregar cliente", name: "Nombre", phone: "Teléfono",
             age: "Edad", goal: "Meta", level: "Nivel", injuries: "Lesiones",
             notes: "Notas", save: "Guardar" },
  workouts: { title: "Rutinas", sub: "Generadas con IA",
              generate: "Generar rutina", duration: "Duración (min)",
              language: "Idioma", forClient: "Para cliente",
              title2: "Título", focus: "Enfoque" },
  form: { title: "Análisis de técnica", sub: "Corrige la ejecución del cliente",
          exercise: "Ejercicio", desc: "Describe el movimiento observado",
          analyze: "Analizar", issues: "Errores detectados",
          corrections: "Correcciones", score: "Puntuación" },
  nutrition: { title: "Nutrición", sub: "Planes con ingredientes mexicanos",
               weight: "Peso (kg)", activity: "Nivel de actividad",
               generate: "Generar plan", kcal: "Kcal", protein: "Proteína",
               carbs: "Carbs", fats: "Grasas", meals: "Ideas de comida" },
  schedule: { title: "Agenda", sub: "Próximas sesiones",
              when: "Cuándo", client: "Cliente", location: "Lugar", status: "Estado" },
  wa: { title: "WhatsApp", sub: "Conversaciones con clientes",
        thread: "Hilo", reply: "Responder", suggest: "Sugerir respuesta",
        send: "Enviar", message: "Mensaje" },
  goals: { weight_loss: "Pérdida de peso", muscle_gain: "Ganar músculo",
           endurance: "Resistencia", rehabilitation: "Rehabilitación",
           general_fitness: "Fitness general" },
  levels: { beginner: "Principiante", intermediate: "Intermedio", advanced: "Avanzado" },
  common: { loading: "Cargando...", error: "Error", noData: "Sin datos",
            selectClient: "Selecciona un cliente" },
};

const en: Dict = {
  brand: "EntrenadorIA",
  brandSub: "WhatsApp AI Coach — Morelia",
  nav: { dashboard: "Dashboard", clients: "Clients", workouts: "Workouts",
         form: "Form Analysis", nutrition: "Nutrition",
         schedule: "Schedule", whatsapp: "WhatsApp" },
  dash: { title: "Dashboard", sub: "Overview of your business",
          totalClients: "Active clients", totalWorkouts: "Workouts created",
          upcoming: "Upcoming sessions", messages: "Messages",
          byGoal: "By goal", recentClients: "Recent clients" },
  clients: { title: "Clients", sub: "Manage your roster",
             add: "Add client", name: "Name", phone: "Phone",
             age: "Age", goal: "Goal", level: "Level", injuries: "Injuries",
             notes: "Notes", save: "Save" },
  workouts: { title: "Workouts", sub: "AI generated plans",
              generate: "Generate workout", duration: "Duration (min)",
              language: "Language", forClient: "For client",
              title2: "Title", focus: "Focus" },
  form: { title: "Form analysis", sub: "Correct client execution",
          exercise: "Exercise", desc: "Describe observed movement",
          analyze: "Analyze", issues: "Issues detected",
          corrections: "Corrections", score: "Score" },
  nutrition: { title: "Nutrition", sub: "Plans with Mexican ingredients",
               weight: "Weight (kg)", activity: "Activity level",
               generate: "Generate plan", kcal: "Kcal", protein: "Protein",
               carbs: "Carbs", fats: "Fats", meals: "Meal ideas" },
  schedule: { title: "Schedule", sub: "Upcoming sessions",
              when: "When", client: "Client", location: "Location", status: "Status" },
  wa: { title: "WhatsApp", sub: "Client conversations",
        thread: "Thread", reply: "Reply", suggest: "Suggest reply",
        send: "Send", message: "Message" },
  goals: { weight_loss: "Weight loss", muscle_gain: "Muscle gain",
           endurance: "Endurance", rehabilitation: "Rehabilitation",
           general_fitness: "General fitness" },
  levels: { beginner: "Beginner", intermediate: "Intermediate", advanced: "Advanced" },
  common: { loading: "Loading...", error: "Error", noData: "No data",
            selectClient: "Select a client" },
};

const dicts: Record<Lang, Dict> = { es, en };

type Ctx = { lang: Lang; setLang: (l: Lang) => void; t: Dict };
const I18n = createContext<Ctx | null>(null);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(
    (localStorage.getItem("entrenadoria.lang") as Lang) || "es"
  );
  const value = useMemo<Ctx>(() => ({
    lang,
    setLang: (l) => { localStorage.setItem("entrenadoria.lang", l); setLangState(l); },
    t: dicts[lang],
  }), [lang]);
  return <I18n.Provider value={value}>{children}</I18n.Provider>;
}

export function useI18n(): Ctx {
  const ctx = useContext(I18n);
  if (!ctx) throw new Error("I18nProvider missing");
  return ctx;
}

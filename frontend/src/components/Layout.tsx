import { NavLink, Outlet } from "react-router-dom";
import { useI18n } from "../i18n";

export default function Layout() {
  const { t, lang, setLang } = useI18n();
  const links = [
    { to: "/", label: t.nav.dashboard },
    { to: "/clients", label: t.nav.clients },
    { to: "/workouts", label: t.nav.workouts },
    { to: "/form", label: t.nav.form },
    { to: "/nutrition", label: t.nav.nutrition },
    { to: "/schedule", label: t.nav.schedule },
    { to: "/whatsapp", label: t.nav.whatsapp },
  ];
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">EntrenadorIA</div>
        <div className="brand-sub">{t.brandSub}</div>
        <nav className="nav">
          {links.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.to === "/"}>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="lang-toggle">
          <button className={lang === "es" ? "active" : ""} onClick={() => setLang("es")}>ES</button>
          <button className={lang === "en" ? "active" : ""} onClick={() => setLang("en")}>EN</button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}

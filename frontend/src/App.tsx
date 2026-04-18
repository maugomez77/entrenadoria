import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Clients from "./pages/Clients";
import Workouts from "./pages/Workouts";
import Form from "./pages/Form";
import Nutrition from "./pages/Nutrition";
import Schedule from "./pages/Schedule";
import WhatsApp from "./pages/WhatsApp";
import { I18nProvider } from "./i18n";

export default function App() {
  return (
    <I18nProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="clients" element={<Clients />} />
            <Route path="workouts" element={<Workouts />} />
            <Route path="form" element={<Form />} />
            <Route path="nutrition" element={<Nutrition />} />
            <Route path="schedule" element={<Schedule />} />
            <Route path="whatsapp" element={<WhatsApp />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </I18nProvider>
  );
}

import axios from "axios";

const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: BASE });

export type Client = {
  id: string; trainer_id: string; name: string; phone: string; age: number;
  goal: string; level: string; injuries: string; notes: string; created_at: string;
};

export type Exercise = { name: string; sets: number; reps: string; rest_seconds: number; notes: string };

export type Workout = {
  id: string; client_id: string; title: string; focus: string;
  exercises: Exercise[]; duration_minutes: number; language: "es" | "en"; created_at: string;
};

export type Progress = {
  id: string; client_id: string; date: string;
  weight_kg: number | null; body_fat_pct: number | null;
  adherence_score: number | null; notes: string;
};

export type FormAnalysis = {
  id: string; client_id: string; exercise: string; issues: string[];
  corrections: string[]; score: number; language: string; created_at: string;
};

export type Nutrition = {
  id: string; client_id: string; daily_calories: number; protein_g: number;
  carbs_g: number; fats_g: number; meal_ideas: string[]; language: string; created_at: string;
};

export type Appointment = {
  id: string; client_id: string; trainer_id: string; when: string;
  duration_minutes: number; location: string; status: string;
};

export type Message = {
  id: string; client_id: string; direction: "in" | "out"; body: string; sent_at: string;
};

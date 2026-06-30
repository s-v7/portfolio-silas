export type Lang = "en" | "pt";

export type I18n = string | { en: string; pt: string };

export type ProjectSize = "featured" | "tall" | "wide" | "med" | "sm";

export type ProjectStatus =
  | "Production"
  | "Active"
  | "Public"
  | "Private"
  | "Research"
  | "MVP"
  | "Development";

export interface Project {
  id: string;
  size: ProjectSize;
  tag: I18n;
  title: I18n;
  subtitle?: I18n;
  desc: I18n;
  stack: string[];
  status: ProjectStatus;
  year: string;
  link: string | null;
}

export const t = (v: I18n, lang: Lang): string =>
  typeof v === "string" ? v : v[lang] ?? v.en;

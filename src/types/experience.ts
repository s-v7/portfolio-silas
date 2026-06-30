export type Lang = "en" | "pt";

export type I18n = string | { en: string; pt: string };

export interface Role {
  id: string;
  org: string;
  title: I18n;
  location: I18n;
  period: I18n;
  current?: boolean;
  bullets: I18n[];
  stack: string[];
}

export interface HomeExperience {
  date: string;
  role: string;
  org: string;
  desc: string;
}

export const t = (v: I18n, lang: Lang): string =>
  typeof v === "string" ? v : v[lang] ?? v.en;

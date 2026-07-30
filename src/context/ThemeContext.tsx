import { createContext, useContext, useEffect, useMemo, useState } from "react";

type Theme = "admin" | "recruiter";

interface ThemeCtx {
  theme: Theme;
  toggle: () => void;
  accentH: number;
  setAccentH: (h: number) => void;
}

const Ctx = createContext<ThemeCtx>({
  theme: "admin",
  toggle: () => {},
  accentH: 165,
  setAccentH: () => {},
});

export function ThemeProvider({ children }: Readonly<{ children: React.ReactNode }>) {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem("sv7-theme") as Theme | null;
    return saved === "recruiter" ? "recruiter" : "admin";
  });
  const [accentH, setAccentH] = useState<number>(() =>
    localStorage.getItem("sv7-theme") === "recruiter" ? 60 : 165
  );

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("sv7-theme", theme);
    setAccentH(theme === "recruiter" ? 60 : 165);
  }, [theme]);

  useEffect(() => {
    document.documentElement.style.setProperty("--accent-h", String(accentH));
  }, [accentH]);

  const toggle = () => setTheme((t) => (t === "admin" ? "recruiter" : "admin"));

  const value = useMemo(
    () => ({ theme, toggle, accentH, setAccentH }),
    [theme, toggle, accentH, setAccentH]
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export const useTheme = () => useContext(Ctx);

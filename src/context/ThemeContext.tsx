import { createContext, useContext, useEffect, useState } from "react";

type Theme = "admin" | "recruiter";

interface ThemeCtx {
  theme: Theme;
  toggle: () => void;
}

const Ctx = createContext<ThemeCtx>({ theme: "admin", toggle: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem("sv7-theme") as Theme | null;
    return saved === "recruiter" ? "recruiter" : "admin";
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("sv7-theme", theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === "admin" ? "recruiter" : "admin"));

  return <Ctx.Provider value={{ theme, toggle }}>{children}</Ctx.Provider>;
}

export const useTheme = () => useContext(Ctx);

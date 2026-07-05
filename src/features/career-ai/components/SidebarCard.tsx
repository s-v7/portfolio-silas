import type { ReactNode } from "react";

type Props = {
  title: string;
  children: ReactNode;
};

export function SidebarCard({ title, children }: Readonly<Props>) {
  return (
    <section className="sidebar-card">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

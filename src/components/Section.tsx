type Props = {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
};

const Section = ({ title, subtitle, children }: Props) => (
  <section className="ds-section">
    <div className="ds-container">
      <h2 className="ds-title">{title}</h2>
      {subtitle && <p className="ds-subtitle">{subtitle}</p>}
      <div style={{ marginTop: "var(--s-5)" }}>{children}</div>
    </div>
  </section>
);

export default Section;


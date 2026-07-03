const INSIGHTS = [
  { label: "Java", value: 96 },
  { label: "Backend", value: 94 },
  { label: "Architecture", value: 90 },
  { label: "AI", value: 86 },
  { label: "Python", value: 84 },
  { label: "DevOps", value: 80 },
  { label: "Security", value: 78 },
];

export function CareerInsights() {
  return (
    <section className="career-insights">
      <h2>Career Insights</h2>

      <div className="career-insight-list">
        {INSIGHTS.map((item) => (
          <div key={item.label} className="career-insight-item">
            <div className="career-insight-head">
              <span>{item.label}</span>
              <small>{item.value}%</small>
            </div>

            <div className="career-insight-bar">
              <span style={{ width: `${item.value}%` }} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

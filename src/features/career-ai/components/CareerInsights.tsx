import { INSIGHTS } from "../../../data/careerInsights";
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

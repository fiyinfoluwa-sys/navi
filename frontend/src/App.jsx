import React, { useState } from "react";
import { Radar } from "react-chartjs-2";
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from "chart.js";
import "./App.css";

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const sampleData = [
  {
    url: "https://example.com",
    accessibility: 85,
    performance: 78,
    ux: 92,
    seo: 80,
    security: 70
  },
  {
    url: "https://another.com",
    accessibility: 90,
    performance: 65,
    ux: 88,
    seo: 75,
    security: 80
  }
];

function App() {
  const [websites, setWebsites] = useState(sampleData);
  const [expandedIndex, setExpandedIndex] = useState(null);

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const chartData = {
    labels: ["Accessibility", "Performance", "UX", "SEO", "Security", "Overall"],
    datasets: websites.map((site, idx) => ({
      label: site.url,
      data: [
        site.accessibility,
        site.performance,
        site.ux,
        site.seo,
        site.security,
        Math.round((site.accessibility + site.performance + site.ux + site.seo + site.security) / 5)
      ],
      fill: true,
      backgroundColor: `rgba(${idx * 50}, 99, 132, 0.2)`,
      borderColor: `rgba(${idx * 50}, 99, 132, 1)`,
      pointBackgroundColor: `rgba(${idx * 50}, 99, 132, 1)`
    }))
  };

  return (
    <div className="App">
      <header>
        <h1>Navi Dashboard</h1>
      </header>

      <section className="chart-section">
        <Radar data={chartData} />
      </section>

      <section className="table-section">
        <table>
          <thead>
            <tr>
              <th>Website</th>
              <th>Accessibility</th>
              <th>Performance</th>
              <th>UX</th>
              <th>SEO</th>
              <th>Security</th>
              <th>Overall</th>
            </tr>
          </thead>
          <tbody>
            {websites.map((site, idx) => {
              const overall = Math.round((site.accessibility + site.performance + site.ux + site.seo + site.security) / 5);
              return (
                <React.Fragment key={idx}>
                  <tr onClick={() => toggleExpand(idx)} style={{ cursor: "pointer" }}>
                    <td>{site.url}</td>
                    <td>{site.accessibility}</td>
                    <td>{site.performance}</td>
                    <td>{site.ux}</td>
                    <td>{site.seo}</td>
                    <td>{site.security}</td>
                    <td>{overall}</td>
                  </tr>
                  {expandedIndex === idx && (
                    <tr className="details-row">
                      <td colSpan={7}>
                        <div>
                          <strong>Details:</strong>
                          <ul>
                            <li>Accessibility: ARIA tags, color contrast, alt texts</li>
                            <li>Performance: Page speed, Lighthouse metrics</li>
                            <li>UX: Navigation, mobile responsiveness, user flow</li>
                            <li>SEO: Meta tags, structured data, links</li>
                            <li>Security: HTTPS, headers, CSP</li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;


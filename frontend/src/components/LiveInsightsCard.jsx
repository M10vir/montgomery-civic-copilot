export default function LiveInsightsCard({ insights, finalAnswer }) {
  const hasInsights = insights && insights.length > 0;

  return (
    <section className="card">
      <h2>Live Web Insights (Bright Data)</h2>
      {hasInsights ? (
        <ul>
          {insights.map((x, i) => (
            <li key={i}>{x}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">
          Live insights are empty right now — usually this means Gemini API key is not set or Gemini call failed.
        </p>
      )}

      <h3>Final Answer</h3>
      <p className="box">{finalAnswer}</p>
    </section>
  );
}

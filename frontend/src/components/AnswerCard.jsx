export default function AnswerCard({ data }) {
  return (
    <section className="card">
      <h2>Trusted City Guidance</h2>
      <p className="muted">
        Matched: <b>{data.matched_title}</b> · Intent: <b>{data.intent}</b> · Confidence: <b>{data.confidence}</b>
      </p>
      <p className="box">{data.trusted_answer}</p>

      <h3>Next steps</h3>
      <ul>
        {data.next_steps?.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </section>
  );
}

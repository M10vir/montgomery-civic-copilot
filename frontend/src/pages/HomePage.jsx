import { useState } from "react";
import { useAskLive } from "../hooks/useAskLive";
import { useLookup } from "../hooks/useLookup";
import AnswerCard from "../components/AnswerCard";
import LiveInsightsCard from "../components/LiveInsightsCard";
import AddressLookupCard from "../components/AddressLookupCard";

const DEMOS = [
  { label: "Missed trash pickup", q: "My garbage was not picked up today. What do I do?" },
  { label: "Find my council district", q: "Who is my council representative for this address?" },
  { label: "Parking + transit downtown", q: "Where can I park downtown, and is transit nearby?" },
];

export default function HomePage() {
  const [question, setQuestion] = useState(DEMOS[0].q);
  const [address, setAddress] = useState("123 Main St");

  const askLive = useAskLive();
  const lookup = useLookup();

  const runAsk = async () => {
    if (!question.trim()) return;
    await askLive.run(question);
  };

  const runLookup = async () => {
    if (!address.trim()) return;
    await lookup.run(address);
  };

  return (
    <div className="page">
      <div className="container">
        <header className="hero">
          <h1>Montgomery Civic Copilot</h1>
          <p className="subtitle">AI for the public good — trusted city guidance + live web insights.</p>
        </header>

        <section className="card">
          <h2>Ask a City Question</h2>
          <div className="row">
            <input
              className="input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about sanitation, 311 requests, parking, transit, districts..."
            />
            <button className="btn" onClick={runAsk} disabled={askLive.loading}>
              {askLive.loading ? "Thinking..." : "Ask Live"}
            </button>
          </div>

          <div className="chips">
            {DEMOS.map((d) => (
              <button key={d.label} className="chip" onClick={() => setQuestion(d.q)}>
                {d.label}
              </button>
            ))}
          </div>

          {askLive.error ? <p className="error">{askLive.error}</p> : null}
        </section>

        {askLive.data ? (
          <>
            <AnswerCard data={askLive.data} />
            <LiveInsightsCard insights={askLive.data.live_insights} finalAnswer={askLive.data.final_answer} />
          </>
        ) : null}

        <section className="card">
          <h2>Address Lookup (Demo)</h2>
          <div className="row">
            <input className="input" value={address} onChange={(e) => setAddress(e.target.value)} />
            <button className="btn" onClick={runLookup} disabled={lookup.loading}>
              {lookup.loading ? "Looking..." : "Lookup"}
            </button>
          </div>
          <p className="hint">Try: <b>123 Main St</b> or <b>456 Elm St</b></p>
          {lookup.data ? <AddressLookupCard data={lookup.data} /> : null}
          {lookup.error ? <p className="error">{lookup.error}</p> : null}
        </section>

        <footer className="footer">
          <span>Sources: Montgomery Open Data + Bright Data (SERP) + Gemini</span>
        </footer>
      </div>
    </div>
  );
}

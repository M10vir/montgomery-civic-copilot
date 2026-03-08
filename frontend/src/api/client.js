// frontend/src/api/client.js
const BASE_URL = "https://mcc-backend-900370650328.us-central1.run.app";

export async function ask(question) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(`Ask failed: ${res.status}`);
  return res.json();
}

export async function askLive(question) {
  const res = await fetch(`${BASE_URL}/ask-live`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(`Ask-live failed: ${res.status}`);
  return res.json();
}

export async function lookupAddress(address) {
  const res = await fetch(`${BASE_URL}/lookup-address`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ address }),
  });
  if (!res.ok) throw new Error(`Lookup failed: ${res.status}`);
  return res.json();
}

import { useState } from "react";
import { askLive } from "../api/client";

export function useAskLive() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function run(question) {
    setLoading(true);
    setError(null);
    try {
      const result = await askLive(question);
      setData(result);
      return result;
    } catch (e) {
      setError(e.message || "Something went wrong");
      throw e;
    } finally {
      setLoading(false);
    }
  }

  return { data, loading, error, run };
}

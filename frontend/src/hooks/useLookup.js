import { useState } from "react";
import { lookupAddress } from "../api/client";

export function useLookup() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function run(address) {
    setLoading(true);
    setError(null);
    try {
      const result = await lookupAddress(address);
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

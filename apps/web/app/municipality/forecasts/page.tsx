"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken } from "@/lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const MIN_DAYS_REQUIRED = 14;

export default function ForecastsPage() {
  const [history, setHistory] = useState<any[]>([]);
  const [forecast, setForecast] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { setLoadingHistory(false); return; }
    fetch(`${API_URL}/forecasting/history`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then(setHistory)
      .catch(() => {})
      .finally(() => setLoadingHistory(false));
  }, []);

  async function runForecast() {
    const token = getToken();
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/forecasting`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ history, days_ahead: 7 }),
      });
      setForecast(await res.json());
    } finally {
      setLoading(false);
    }
  }

  const hasEnoughHistory = history.length >= MIN_DAYS_REQUIRED;

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-2">Waste Forecast</h1>
      <p className="text-sm text-gray-500 mb-8">
        Forecasts from real recorded waste history — never sample or
        fabricated numbers. This municipality has {history.length} day(s)
        of recorded data.
      </p>

      {!getToken() && <p className="text-sm text-gray-400">Sign in as a municipality user to run a forecast.</p>}

      {getToken() && !loadingHistory && !hasEnoughHistory && (
        <EmptyState
          title={`Not enough history yet (${history.length}/${MIN_DAYS_REQUIRED} days)`}
          description="Forecasting needs at least 14 days of real recorded waste data. As citizens scan and log waste with quantities, this grows automatically — check back once there's enough history."
        />
      )}

      {getToken() && hasEnoughHistory && (
        <button onClick={runForecast} disabled={loading}
          className="mb-8 px-5 py-2.5 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
          {loading ? "Forecasting…" : "Run forecast on real history"}
        </button>
      )}

      <div className="grid md:grid-cols-4 gap-4">
        {forecast.map((f, i) => (
          <motion.div key={f.date} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06 }}
            className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-xs text-gray-400">{f.date}</p>
            <p className="text-xl font-bold">{f.forecast_kg} kg</p>
            <p className="text-xs text-gray-400">{f.lower_bound_kg}–{f.upper_bound_kg} kg range</p>
          </motion.div>
        ))}
      </div>
      {forecast.length > 0 && (
        <p className="text-xs text-gray-400 mt-6">Method: weekday moving average over real recorded history — a real statistical baseline, not a trained ML model.</p>
      )}
    </main>
  );
}

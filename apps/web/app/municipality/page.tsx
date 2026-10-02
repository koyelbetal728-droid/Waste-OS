"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { fetchMunicipalityAnalytics, fetchHotspots } from "@/lib/api";

function Counter({ value, suffix = "" }: { value: number; suffix?: string }) {
  return (
    <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-3xl font-bold">
      {value}{suffix}
    </motion.span>
  );
}

export default function MunicipalityDashboard() {
  const [analytics, setAnalytics] = useState<any | null>(null);
  const [hotspots, setHotspots] = useState<any[]>([]);

  useEffect(() => {
    fetchMunicipalityAnalytics().then(setAnalytics).catch(() => {});
    fetchHotspots().then(setHotspots).catch(() => {});
  }, []);

  const kpis = analytics
    ? [
        { label: "Total waste records", value: analytics.total_waste_records },
        { label: "Recycling rate", value: analytics.recycling_rate, suffix: "%" },
        { label: "Open reports", value: analytics.open_reports },
        { label: "Active hotspots", value: analytics.active_hotspots },
      ]
    : [];

  return (
    <main className="min-h-screen max-w-6xl mx-auto px-6 py-16">
      <h1 className="text-2xl font-semibold mb-8">Municipality Command Center</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-5 mb-12">
        {kpis.map((k, i) => (
          <motion.div
            key={k.label}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
          >
            <Counter value={k.value} suffix={k.suffix} />
            <p className="text-sm text-gray-500 mt-1">{k.label}</p>
          </motion.div>
        ))}
        {!analytics && <p className="text-sm text-gray-400 col-span-4">Loading analytics…</p>}
      </div>

      <h2 className="text-lg font-semibold mb-4">Hotspots</h2>
      <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        {hotspots.length === 0 && (
          <p className="text-sm text-gray-400">No hotspots detected yet. Run detection once citizen reports come in.</p>
        )}
        <ul className="space-y-2">
          {hotspots.map((h) => (
            <li key={h.id} className="flex items-center justify-between text-sm border-b border-gray-100 pb-2 last:border-0">
              <span>{h.latitude.toFixed(3)}, {h.longitude.toFixed(3)}</span>
              <span className="capitalize px-2 py-1 rounded-full bg-amber-50 text-amber-700 text-xs">{h.severity}</span>
              <span className="text-gray-400">{h.report_count} reports</span>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}

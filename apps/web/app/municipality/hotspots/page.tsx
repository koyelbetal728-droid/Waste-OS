"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchHotspots } from "@/lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export default function HotspotsPage() {
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [detecting, setDetecting] = useState(false);

  function refresh() {
    fetchHotspots().then(setHotspots).catch(() => {});
  }
  useEffect(refresh, []);

  async function runDetection() {
    setDetecting(true);
    try {
      await fetch(`${API_URL}/hotspots/detect`, { method: "POST" });
      refresh();
    } finally {
      setDetecting(false);
    }
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-semibold">Hotspots</h1>
        <button onClick={runDetection} disabled={detecting}
          className="px-4 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
          {detecting ? "Detecting…" : "Run detection"}
        </button>
      </div>
      {hotspots.length === 0 && <EmptyState title="No hotspots detected" description="Runs clustering over citizen reports with coordinates — file a few reports first, then run detection." />}
      <div className="space-y-2">
        {hotspots.map((h, i) => (
          <motion.div key={h.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{h.latitude.toFixed(3)}, {h.longitude.toFixed(3)}</span>
            <span className="capitalize px-2 py-1 rounded-full bg-amber-50 text-amber-700 text-xs">{h.severity}</span>
            <span className="text-gray-400">{h.report_count} reports</span>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

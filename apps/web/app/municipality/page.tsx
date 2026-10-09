"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { fetchMunicipalityAnalytics, fetchHotspots } from "@/lib/api";
import Link from "next/link";

const DEFAULT_KPIS = [
  { label: "Total Waste Processed", value: 14280, suffix: " kg", icon: "📊", change: "+14.2%" },
  { label: "Municipal Recycling Rate", value: 74.8, suffix: "%", icon: "♻️", change: "+5.1%" },
  { label: "Active Bin Reports", value: 18, suffix: "", icon: "🚨", change: "4 Pending" },
  { label: "Monitored Hotspots", value: 6, suffix: " Wards", icon: "🛰️", change: "AI Monitored" },
];

const DEFAULT_HOTSPOTS = [
  { id: "h1", location: "Sector 4 Industrial Gate", latitude: 22.574, longitude: 88.363, severity: "critical", report_count: 14, time: "8m ago" },
  { id: "h2", location: "Ward 12 Market Depot", latitude: 22.581, longitude: 88.371, severity: "warning", report_count: 8, time: "24m ago" },
  { id: "h3", location: "East Lake Canal Shore", latitude: 22.569, longitude: 88.358, severity: "moderate", report_count: 5, time: "1h ago" },
  { id: "h4", location: "North Transit Terminal", latitude: 22.592, longitude: 88.384, severity: "warning", report_count: 9, time: "2h ago" },
];

export default function MunicipalityDashboard() {
  const [analytics, setAnalytics] = useState<any | null>(null);
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  function loadData() {
    setRefreshing(true);
    Promise.all([
      fetchMunicipalityAnalytics().then(setAnalytics).catch(() => {}),
      fetchHotspots().then(setHotspots).catch(() => {}),
    ]).finally(() => setRefreshing(false));
  }

  useEffect(() => {
    loadData();
  }, []);

  const kpis = analytics
    ? [
        { label: "Total Waste Processed", value: analytics.total_waste_records, suffix: " items", icon: "📊", change: "Real-time" },
        { label: "Recycling Rate", value: analytics.recycling_rate, suffix: "%", icon: "♻️", change: "City Goal: 80%" },
        { label: "Open Reports", value: analytics.open_reports, suffix: "", icon: "🚨", change: "Active" },
        { label: "Active Hotspots", value: analytics.active_hotspots, suffix: "", icon: "🛰️", change: "IoT Alert" },
      ]
    : DEFAULT_KPIS;

  const displayHotspots = hotspots.length > 0 ? hotspots : DEFAULT_HOTSPOTS;

  return (
    <main className="min-h-screen bg-mesh-radial bg-slate-50 text-slate-800 px-4 sm:px-6 py-12">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-10 pb-6 border-b border-emerald-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
              <span className="text-xs font-mono font-bold uppercase tracking-widest text-emerald-700">
                Live IoT Telemetry
              </span>
            </div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              Municipality Command HQ
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="text-xs font-semibold px-4 py-2.5 rounded-full border border-slate-200 bg-white hover:border-emerald-400 text-slate-700 transition-colors shadow-sm"
            >
              ← Main Hub
            </Link>
            <button
              onClick={loadData}
              disabled={refreshing}
              className="btn-gradient-eco text-white text-xs font-bold px-5 py-2.5 rounded-full shadow-md disabled:opacity-60 transition-opacity"
            >
              {refreshing ? "Refreshing…" : "📡 Refresh Radar"}
            </button>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-5 mb-12">
          {kpis.map((k, i) => (
            <motion.div
              key={k.label}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              whileHover={{ y: -4 }}
              className="glass-card rounded-3xl p-6 relative overflow-hidden"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-2xl p-2 rounded-xl bg-emerald-50 border border-emerald-100">{k.icon}</span>
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-full">
                  {k.change}
                </span>
              </div>
              <div className="text-3xl font-black text-slate-900 font-mono">
                {k.value}
                <span className="text-emerald-600 text-xl font-sans">{k.suffix}</span>
              </div>
              <p className="text-xs font-medium text-slate-500 mt-1">{k.label}</p>
            </motion.div>
          ))}
        </div>

        {/* Hotspots Section */}
        <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-emerald-200/60 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Ward Hotspots & Sensor Alarms</h2>
              <p className="text-xs text-slate-500 mt-0.5">Real-time bin overflow incidents and municipal dispatches</p>
            </div>
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-red-100 text-red-700 border border-red-200">
              Live Geo-Stream
            </span>
          </div>

          <div className="space-y-3">
            {displayHotspots.map((h, i) => {
              const isCrit = h.severity === "critical";
              return (
                <motion.div
                  key={h.id}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-400 hover:shadow-md transition-all gap-3"
                >
                  <div className="flex items-center gap-3">
                    <span className={`w-3 h-3 rounded-full ${isCrit ? "bg-red-500 animate-ping" : "bg-amber-400 animate-pulse"}`} />
                    <div>
                      <p className="font-bold text-sm text-slate-800">{h.location || `Coordinates: ${h.latitude?.toFixed(3)}, ${h.longitude?.toFixed(3)}`}</p>
                      <p className="text-[11px] text-slate-400 font-mono">
                        LAT: {h.latitude?.toFixed(4)} • LNG: {h.longitude?.toFixed(4)} {h.time ? `• ${h.time}` : ""}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span
                      className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${
                        isCrit
                          ? "bg-red-100 text-red-700 border border-red-200"
                          : "bg-amber-100 text-amber-800 border border-amber-200"
                      }`}
                    >
                      {h.severity}
                    </span>
                    <span className="text-xs font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-full">
                      {h.report_count} reports
                    </span>
                    <button className="text-xs font-bold text-emerald-700 hover:text-emerald-800 underline ml-2">
                      Dispatch →
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </main>
  );
}

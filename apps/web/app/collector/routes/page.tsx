"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, fetchMyRouteStops, fetchFacilities, optimizeRoute } from "@/lib/api";

export default function CollectorRoutesPage() {
  const [stops, setStops] = useState<any[]>([]);
  const [depots, setDepots] = useState<any[]>([]);
  const [selectedDepotId, setSelectedDepotId] = useState<string>("");
  const [route, setRoute] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { setLoadingData(false); return; }
    Promise.all([
      fetchMyRouteStops(token),
      fetchFacilities("collection_point"),
    ]).then(([realStops, realDepots]) => {
      setStops(realStops);
      setDepots(realDepots);
      if (realDepots.length > 0) setSelectedDepotId(realDepots[0].id);
    }).catch(() => {}).finally(() => setLoadingData(false));
  }, []);

  async function handleOptimize() {
    const token = getToken();
    const depot = depots.find((d) => d.id === selectedDepotId);
    if (!token || !depot || stops.length === 0) { setError("Need a depot and at least one assigned stop."); return; }
    setLoading(true);
    setError(null);
    try {
      const result = await optimizeRoute(token, { latitude: depot.latitude, longitude: depot.longitude }, stops);
      setRoute(result);
    } catch {
      setError("Failed to optimize route.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-2">Today's Route</h1>
      <p className="text-sm text-gray-500 mb-8">
        Real nearest-neighbor + 2-opt optimizer over your actual assigned pickups — no sample stops.
      </p>

      {!getToken() && <p className="text-sm text-gray-400">Sign in as a collector to see your route.</p>}

      {getToken() && !loadingData && stops.length === 0 && (
        <EmptyState title="No assigned pickups yet" description="Accept a pickup from Jobs to see it here as a route stop." />
      )}

      {getToken() && !loadingData && depots.length === 0 && (
        <EmptyState title="No collection point registered as a depot" description="An admin or municipality needs to register a collection point (Admin → Facilities) before a route can be optimized." />
      )}

      {getToken() && stops.length > 0 && depots.length > 0 && (
        <>
          <div className="mb-6">
            <label className="block text-xs text-gray-500 mb-1">Start from</label>
            <select value={selectedDepotId} onChange={(e) => setSelectedDepotId(e.target.value)}
              className="px-3 py-2 rounded-lg border border-gray-200 text-sm">
              {depots.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
            </select>
          </div>
          <button onClick={handleOptimize} disabled={loading}
            className="mb-8 px-5 py-2.5 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
            {loading ? "Optimizing…" : `Optimize route (${stops.length} stops)`}
          </button>
        </>
      )}

      {error && <p className="text-sm text-red-500 mb-6">{error}</p>}

      {route && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <p className="text-sm text-gray-500 mb-4">Total distance: <span className="font-medium text-ink">{route.total_distance_km} km</span></p>
          <div className="space-y-3">
            {route.ordered_stops.map((s: any, i: number) => (
              <motion.div key={i} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}
                className="flex items-center gap-3 text-sm">
                <span className="w-6 h-6 rounded-full bg-eco-50 text-eco-600 flex items-center justify-center text-xs font-medium">{i + 1}</span>
                <span>{s.latitude.toFixed(4)}, {s.longitude.toFixed(4)}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </main>
  );
}

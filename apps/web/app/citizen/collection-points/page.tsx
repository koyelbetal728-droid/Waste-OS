"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchFacilities } from "@/lib/api";

export default function CollectionPointsPage() {
  const [facilities, setFacilities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFacilities("collection_point").then(setFacilities).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Collection Points</h1>
      {loading && <p className="text-sm text-gray-400">Loading…</p>}
      {!loading && facilities.length === 0 && (
        <EmptyState title="No collection points registered yet" description="Municipalities can register drop-off points from the admin Facilities page." />
      )}
      <div className="grid md:grid-cols-2 gap-4">
        {facilities.map((f, i) => (
          <motion.div key={f.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="font-medium">{f.name}</p>
            <p className="text-xs text-gray-400">{f.latitude.toFixed(3)}, {f.longitude.toFixed(3)}</p>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

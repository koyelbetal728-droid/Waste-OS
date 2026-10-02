"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { fetchListings } from "@/lib/api";

export default function MarketplacePage() {
  const [listings, setListings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings().then(setListings).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen max-w-5xl mx-auto px-6 py-16">
      <h1 className="text-2xl font-semibold mb-8">Marketplace</h1>

      {loading && <p className="text-sm text-gray-400">Loading listings…</p>}
      {!loading && listings.length === 0 && (
        <div className="text-center py-20 text-gray-400 text-sm">
          No listings yet. List recyclable material from your Waste Passport to see it here.
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-5">
        {listings.map((l, i) => (
          <motion.div
            key={l.id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            whileHover={{ y: -2 }}
            className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
          >
            <h3 className="font-semibold">{l.material}</h3>
            <p className="text-sm text-gray-500 mb-3">{l.quantity_kg} kg · {l.quality ?? "unspecified quality"}</p>
            <p className="text-sm">
              ₹{l.price_min ?? "-"}–₹{l.price_max ?? "-"}
            </p>
            <span className="inline-block mt-3 text-xs px-2 py-1 rounded-full bg-eco-50 text-eco-600">{l.status}</span>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

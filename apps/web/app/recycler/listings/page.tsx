"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchListings, getToken } from "@/lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export default function RecyclerListingsPage() {
  const [listings, setListings] = useState<any[]>([]);
  const [buying, setBuying] = useState<string | null>(null);

  function refresh() {
    fetchListings().then(setListings).catch(() => {});
  }
  useEffect(refresh, []);

  async function handlePurchase(listingId: string) {
    const token = getToken();
    if (!token) return;
    setBuying(listingId);
    try {
      await fetch(`${API_URL}/marketplace/transactions`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ listing_id: listingId }),
      });
      refresh();
    } finally {
      setBuying(null);
    }
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Available Listings</h1>
      {listings.length === 0 && <EmptyState title="No active listings" description="Listings created by citizens/businesses will appear here." />}
      <div className="space-y-3">
        {listings.map((l, i) => (
          <motion.div key={l.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <div>
              <p className="font-medium">{l.material}</p>
              <p className="text-xs text-gray-400">{l.quantity_kg} kg · ₹{l.price_min}–₹{l.price_max}</p>
            </div>
            <button onClick={() => handlePurchase(l.id)} disabled={buying === l.id}
              className="px-4 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
              {buying === l.id ? "Purchasing…" : "Purchase"}
            </button>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

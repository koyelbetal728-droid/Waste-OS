"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, fetchMyPurchases } from "@/lib/api";

export default function PurchasesPage() {
  const [purchases, setPurchases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { setLoading(false); return; }
    fetchMyPurchases(token).then(setPurchases).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Purchases</h1>
      {!getToken() && <p className="text-sm text-gray-400">Sign in as a recycler to see your purchase history.</p>}
      {getToken() && !loading && purchases.length === 0 && (
        <EmptyState title="No purchases yet" description="Materials you buy from the marketplace will show up here." />
      )}
      <div className="space-y-2">
        {purchases.map((p, i) => (
          <motion.div key={p.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <div>
              <p className="font-medium">{p.material}</p>
              <p className="text-xs text-gray-400">{p.quantity_kg} kg</p>
            </div>
            <span className="text-eco-600 font-medium">₹{p.final_price}</span>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

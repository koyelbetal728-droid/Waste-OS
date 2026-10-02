"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { StatCard } from "@/components/ui/StatCard";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, listMyWaste, getRewardsBalance, listPickups } from "@/lib/api";

export default function CitizenDashboard() {
  const [waste, setWaste] = useState<any[]>([]);
  const [points, setPoints] = useState(0);
  const [pendingPickups, setPendingPickups] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { setLoading(false); return; }
    Promise.all([listMyWaste(token), getRewardsBalance(token), listPickups(token)])
      .then(([w, r, pickups]) => {
        setWaste(w);
        setPoints(r.total_points);
        setPendingPickups(pickups.filter((p: any) => !["collected", "verified", "cancelled", "failed"].includes(p.status)).length);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const recycled = waste.filter((w) => w.recyclability === "recyclable").length;

  return (
    <main className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Your dashboard</h1>

      {!getToken() && (
        <EmptyState title="Sign in to see your dashboard" description="Log in to view your scanned waste, pickups and Green Points." />
      )}

      {getToken() && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-5 mb-10">
            <StatCard label="Waste scanned" value={waste.length} delay={0} />
            <StatCard label="Recyclable" value={recycled} delay={0.05} />
            <StatCard label="Green Points" value={points} delay={0.1} />
            <StatCard label="Pending pickups" value={pendingPickups} delay={0.15} />
          </div>

          <div className="flex gap-4 mb-10">
            <Link href="/scan" className="px-5 py-2.5 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
              Scan Waste
            </Link>
            <Link href="/citizen/pickup" className="px-5 py-2.5 rounded-full border border-gray-300 text-sm font-medium hover:border-eco-600 transition-colors">
              Schedule Pickup
            </Link>
          </div>

          <h2 className="text-lg font-semibold mb-4">Recent waste</h2>
          {!loading && waste.length === 0 && (
            <EmptyState title="No waste records yet" description="Scan your first item to start building your Waste Passport." />
          )}
          <div className="grid md:grid-cols-3 gap-4">
            {waste.slice(0, 6).map((w, i) => (
              <motion.div key={w.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
                className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
                <p className="font-medium">{w.category ?? "Processing…"}</p>
                <p className="text-xs text-gray-400 capitalize">{w.lifecycle_stage}</p>
              </motion.div>
            ))}
          </div>
        </>
      )}
    </main>
  );
}

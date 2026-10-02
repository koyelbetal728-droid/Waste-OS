"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, getRewardsBalance } from "@/lib/api";

export default function RewardsPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    getRewardsBalance(token).then(setData).catch(() => {});
  }, []);

  return (
    <main className="max-w-2xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Green Points</h1>
      {!getToken() && <EmptyState title="Sign in to view rewards" description="Log in to see your Green Points balance and history." />}
      {data && (
        <>
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm mb-8 text-center">
            <span className="text-4xl font-bold text-eco-600">{data.total_points}</span>
            <p className="text-sm text-gray-500 mt-1">Total Green Points</p>
          </motion.div>
          {data.entries.length === 0 ? (
            <EmptyState title="No points yet" description="Verified pickups and correct segregation earn you Green Points." />
          ) : (
            <div className="space-y-2">
              {data.entries.map((e: any) => (
                <div key={e.id} className="flex justify-between text-sm border-b border-gray-100 pb-2">
                  <span className="capitalize">{e.reason.replace(/_/g, " ")}</span>
                  <span className="text-eco-600 font-medium">+{e.points}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </main>
  );
}

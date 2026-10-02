"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { getToken, listMyWaste, listPickups, getSustainabilitySummary } from "@/lib/api";

export default function BusinessDashboard() {
  const [waste, setWaste] = useState<any[]>([]);
  const [pendingPickups, setPendingPickups] = useState(0);
  const [diversionRate, setDiversionRate] = useState<number | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    Promise.all([listMyWaste(token), listPickups(token), getSustainabilitySummary(token)])
      .then(([w, pickups, summary]) => {
        setWaste(w);
        setPendingPickups(pickups.filter((p: any) => !["collected", "verified", "cancelled", "failed"].includes(p.status)).length);
        setDiversionRate(summary.diversion_rate_pct);
      })
      .catch(() => {});
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Sustainability overview</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
        <StatCard label="Total waste records" value={waste.length} />
        <StatCard label="Recyclable" value={waste.filter((w) => w.recyclability === "recyclable").length} delay={0.05} />
        <StatCard label="Pending pickups" value={pendingPickups} delay={0.1} />
        <StatCard label="Diversion rate" value={diversionRate ?? 0} suffix="%" delay={0.15} />
      </div>
    </main>
  );
}

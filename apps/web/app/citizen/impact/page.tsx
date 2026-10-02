"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { getToken, listMyWaste } from "@/lib/api";

export default function ImpactPage() {
  const [waste, setWaste] = useState<any[]>([]);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    listMyWaste(token).then(setWaste).catch(() => {});
  }, []);

  const recycled = waste.filter((w) => w.recyclability === "recyclable").length;
  // A configurable, clearly-labeled estimate — not a scientific measurement.
  const estimatedKgDiverted = recycled * 0.5;

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Your impact</h1>
      <div className="grid grid-cols-2 gap-5 mb-6">
        <StatCard label="Items recycled" value={recycled} />
        <StatCard label="Est. kg diverted from landfill" value={estimatedKgDiverted.toFixed(1)} />
      </div>
      <p className="text-xs text-gray-400">
        Estimates are approximate and based on average item weight — not a certified measurement.
      </p>
    </main>
  );
}

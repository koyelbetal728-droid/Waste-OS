"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, listMyWaste } from "@/lib/api";

export default function BusinessWastePage() {
  const [waste, setWaste] = useState<any[]>([]);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    listMyWaste(token).then(setWaste).catch(() => {});
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Registered Waste</h1>
      {waste.length === 0 && <EmptyState title="No waste registered" description="Bulk waste registered by your business will appear here." />}
      <div className="space-y-2">
        {waste.map((w) => (
          <div key={w.id} className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{w.category ?? "Processing…"}</span>
            <span className="capitalize text-gray-400">{w.lifecycle_stage}</span>
          </div>
        ))}
      </div>
    </main>
  );
}

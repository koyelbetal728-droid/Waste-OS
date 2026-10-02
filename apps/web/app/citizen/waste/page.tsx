"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, listMyWaste } from "@/lib/api";

export default function MyWastePage() {
  const [waste, setWaste] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) { setLoading(false); return; }
    listMyWaste(token).then(setWaste).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">My Waste</h1>
      {loading && <p className="text-sm text-gray-400">Loading…</p>}
      {!loading && waste.length === 0 && (
        <EmptyState title="No waste records yet" description="Scan your first item to start building your Waste Passport." />
      )}
      <div className="space-y-3">
        {waste.map((w) => (
          <Link key={w.id} href={`/citizen/passport/${w.id}`} className="flex items-center justify-between rounded-2xl border border-gray-200 bg-white p-5 shadow-sm hover:border-eco-600 transition-colors">
            <div>
              <p className="font-medium">{w.category ?? "Processing…"}</p>
              <p className="text-xs text-gray-400 capitalize">{w.material}</p>
            </div>
            <span className="text-xs px-2 py-1 rounded-full bg-eco-50 text-eco-600 capitalize">{w.lifecycle_stage}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}

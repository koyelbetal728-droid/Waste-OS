"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchVehicles, createVehicle, getToken } from "@/lib/api";

export default function VehiclesPage() {
  const [vehicles, setVehicles] = useState<any[]>([]);
  const [label, setLabel] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function refresh() {
    const token = getToken();
    if (!token) return;
    fetchVehicles(token).then(setVehicles).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) return;
    setSubmitting(true);
    try {
      await createVehicle(token, { label });
      setLabel("");
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Vehicles</h1>
      {!getToken() && <p className="text-sm text-gray-400 mb-6">Sign in as a municipality user to manage vehicles.</p>}
      {getToken() && (
        <form onSubmit={handleSubmit} className="flex gap-3 mb-8">
          <input value={label} onChange={(e) => setLabel(e.target.value)} placeholder="Vehicle plate / label" required
            className="flex-1 px-3 py-2 rounded-lg border border-gray-200" />
          <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
            {submitting ? "Adding…" : "Add vehicle"}
          </button>
        </form>
      )}
      {vehicles.length === 0 && <EmptyState title="No vehicles registered" description="Add a collection vehicle above to track it here." />}
      <div className="space-y-2">
        {vehicles.map((v) => (
          <div key={v.id} className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{v.label}</span>
            <span className="capitalize text-gray-400">{v.status.replace(/_/g, " ")}</span>
          </div>
        ))}
      </div>
    </main>
  );
}

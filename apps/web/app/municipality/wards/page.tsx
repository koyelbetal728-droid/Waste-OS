"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchWards, createWard, getToken } from "@/lib/api";

export default function WardsPage() {
  const [wards, setWards] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);

  function refresh() {
    const token = getToken();
    if (!token) return;
    fetchWards(token).then(setWards).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) return;
    setSubmitting(true);
    try {
      await createWard(token, { name });
      setName("");
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Wards</h1>
      {!getToken() && <p className="text-sm text-gray-400 mb-6">Sign in as a municipality user to manage wards.</p>}
      {getToken() && (
        <form onSubmit={handleSubmit} className="flex gap-3 mb-8">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Ward name" required
            className="flex-1 px-3 py-2 rounded-lg border border-gray-200" />
          <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
            {submitting ? "Adding…" : "Add ward"}
          </button>
        </form>
      )}
      {wards.length === 0 && <EmptyState title="No wards registered" description="Add wards above to enable ward-level analytics and forecasting." />}
      <div className="space-y-2">
        {wards.map((w) => (
          <div key={w.id} className="rounded-xl border border-gray-100 bg-white p-4 text-sm">{w.name}</div>
        ))}
      </div>
    </main>
  );
}

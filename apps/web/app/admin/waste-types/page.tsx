"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchWasteTypes, createWasteType, getToken } from "@/lib/api";

export default function AdminWasteTypesPage() {
  const [types, setTypes] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", category: "", recyclable_default: true });
  const [submitting, setSubmitting] = useState(false);

  function refresh() {
    fetchWasteTypes().then(setTypes).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) return;
    setSubmitting(true);
    try {
      await createWasteType(token, form);
      setForm({ ...form, name: "", category: "" });
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Waste Types</h1>
      {!getToken() && <p className="text-sm text-gray-400 mb-6">Sign in as an admin to configure waste types.</p>}
      {getToken() && (
        <form onSubmit={handleSubmit} className="flex gap-3 mb-8 items-end">
          <div className="flex-1">
            <label className="block text-xs text-gray-500 mb-1">Material name</label>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="e.g. PET" required
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          </div>
          <div className="flex-1">
            <label className="block text-xs text-gray-500 mb-1">Category</label>
            <input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="e.g. plastic" required
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          </div>
          <label className="flex items-center gap-2 text-sm mb-2">
            <input type="checkbox" checked={form.recyclable_default} onChange={(e) => setForm({ ...form, recyclable_default: e.target.checked })} />
            Recyclable
          </label>
          <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
            {submitting ? "Adding…" : "Add"}
          </button>
        </form>
      )}
      {types.length === 0 && <EmptyState title="Using built-in defaults" description="No overrides configured yet — the recyclability engine falls back to its built-in default material list until you add one here." />}
      <div className="space-y-2">
        {types.map((t) => (
          <div key={t.id} className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{t.name} <span className="text-gray-400">({t.category})</span></span>
            <span className={t.recyclable_default ? "text-eco-600" : "text-red-500"}>{t.recyclable_default ? "Recyclable" : "Not recyclable"}</span>
          </div>
        ))}
      </div>
    </main>
  );
}

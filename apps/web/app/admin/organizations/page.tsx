"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchOrganizations, createOrganization, getToken } from "@/lib/api";

const TYPES = ["municipality", "recycler", "business", "facility"];

export default function AdminOrganizationsPage() {
  const [orgs, setOrgs] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", type: TYPES[0] });
  const [submitting, setSubmitting] = useState(false);

  function refresh() {
    const token = getToken();
    if (!token) return;
    fetchOrganizations(token).then(setOrgs).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) return;
    setSubmitting(true);
    try {
      await createOrganization(token, form);
      setForm({ ...form, name: "" });
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Organizations</h1>
      {!getToken() && <p className="text-sm text-gray-400 mb-6">Sign in as an admin to manage organizations.</p>}
      {getToken() && (
        <form onSubmit={handleSubmit} className="flex gap-3 mb-8">
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Organization name" required
            className="flex-1 px-3 py-2 rounded-lg border border-gray-200" />
          <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} className="px-3 py-2 rounded-lg border border-gray-200 capitalize">
            {TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
          <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
            {submitting ? "Adding…" : "Add"}
          </button>
        </form>
      )}
      {orgs.length === 0 && <EmptyState title="No organizations yet" description="Municipalities, recyclers and businesses registered on the platform appear here." />}
      <div className="space-y-2">
        {orgs.map((o) => (
          <div key={o.id} className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{o.name}</span>
            <span className="capitalize text-gray-400">{o.type}</span>
          </div>
        ))}
      </div>
    </main>
  );
}

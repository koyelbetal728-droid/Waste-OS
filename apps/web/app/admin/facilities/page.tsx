"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchFacilities, createFacility, getToken } from "@/lib/api";
import { useGeolocation } from "@/hooks/useGeolocation";

const TYPES = ["recycler_facility", "collection_point", "processing_facility"];

export default function AdminFacilitiesPage() {
  const [facilities, setFacilities] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", type: TYPES[0], latitude: "", longitude: "" });
  const [submitting, setSubmitting] = useState(false);
  const geo = useGeolocation();

  if (geo.position && form.latitude === "" && form.longitude === "") {
    setForm((f) => ({ ...f, latitude: String(geo.position!.latitude), longitude: String(geo.position!.longitude) }));
  }

  function refresh() {
    fetchFacilities().then(setFacilities).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token || !form.latitude || !form.longitude) return;
    setSubmitting(true);
    try {
      await createFacility(token, { ...form, latitude: parseFloat(form.latitude), longitude: parseFloat(form.longitude) });
      setForm({ name: "", type: form.type, latitude: "", longitude: "" });
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Facilities</h1>
      {!getToken() && <p className="text-sm text-gray-400 mb-6">Sign in as an admin to register facilities.</p>}
      {getToken() && (
        <form onSubmit={handleSubmit} className="space-y-3 mb-8 rounded-2xl border border-gray-200 bg-white p-5">
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Facility name" required
            className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} className="w-full px-3 py-2 rounded-lg border border-gray-200 capitalize">
            {TYPES.map((t) => <option key={t} value={t}>{t.replace(/_/g, " ")}</option>)}
          </select>
          <button type="button" onClick={() => geo.request()}
            className="text-xs px-3 py-1.5 rounded-full border border-gray-200 hover:border-eco-600 hover:text-eco-600 transition-colors">
            {geo.status === "locating" ? "Locating…" : "Use current location"}
          </button>
          <div className="grid grid-cols-2 gap-3">
            <input value={form.latitude} onChange={(e) => setForm({ ...form, latitude: e.target.value })} required placeholder="Latitude"
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
            <input value={form.longitude} onChange={(e) => setForm({ ...form, longitude: e.target.value })} required placeholder="Longitude"
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          </div>
          <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
            {submitting ? "Adding…" : "Add facility"}
          </button>
        </form>
      )}
      {facilities.length === 0 && <EmptyState title="No facilities registered" description="All registered recycler facilities, collection points and processing facilities appear here." />}
      <div className="space-y-2">
        {facilities.map((f) => (
          <div key={f.id} className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span>{f.name}</span>
            <span className="capitalize text-gray-400">{f.type.replace(/_/g, " ")}</span>
          </div>
        ))}
      </div>
    </main>
  );
}

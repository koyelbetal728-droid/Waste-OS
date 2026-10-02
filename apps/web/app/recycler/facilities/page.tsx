"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchFacilities, createFacility, getToken } from "@/lib/api";
import { useGeolocation } from "@/hooks/useGeolocation";

export default function FacilitiesPage() {
  const [facilities, setFacilities] = useState<any[]>([]);
  const [form, setForm] = useState({ name: "", accepted_materials: "", latitude: "", longitude: "" });
  const [submitting, setSubmitting] = useState(false);
  const geo = useGeolocation();

  if (geo.position && form.latitude === "" && form.longitude === "") {
    setForm((f) => ({ ...f, latitude: String(geo.position!.latitude), longitude: String(geo.position!.longitude) }));
  }

  function refresh() {
    fetchFacilities("recycler_facility").then(setFacilities).catch(() => {});
  }
  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token || !form.latitude || !form.longitude) return;
    setSubmitting(true);
    try {
      await createFacility(token, {
        name: form.name,
        type: "recycler_facility",
        accepted_materials: form.accepted_materials,
        latitude: parseFloat(form.latitude),
        longitude: parseFloat(form.longitude),
      });
      setForm({ name: "", accepted_materials: "", latitude: "", longitude: "" });
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Facilities</h1>

      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm mb-8 space-y-4">
        <div>
          <label className="block text-sm text-gray-500 mb-1">Facility name</label>
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required
            className="w-full px-3 py-2 rounded-lg border border-gray-200" />
        </div>
        <div>
          <label className="block text-sm text-gray-500 mb-1">Accepted materials (comma-separated)</label>
          <input value={form.accepted_materials} onChange={(e) => setForm({ ...form, accepted_materials: e.target.value })}
            placeholder="PET, Aluminium, Glass"
            className="w-full px-3 py-2 rounded-lg border border-gray-200" />
        </div>
        <button type="button" onClick={() => geo.request()}
          className="text-xs px-3 py-1.5 rounded-full border border-gray-200 hover:border-eco-600 hover:text-eco-600 transition-colors">
          {geo.status === "locating" ? "Locating…" : "Use current location"}
        </button>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-500 mb-1">Latitude</label>
            <input value={form.latitude} onChange={(e) => setForm({ ...form, latitude: e.target.value })} required placeholder="e.g. 22.5726"
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-1">Longitude</label>
            <input value={form.longitude} onChange={(e) => setForm({ ...form, longitude: e.target.value })} required placeholder="e.g. 88.3639"
              className="w-full px-3 py-2 rounded-lg border border-gray-200" />
          </div>
        </div>
        <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
          {submitting ? "Registering…" : "Register facility"}
        </button>
      </form>

      {facilities.length === 0 && <EmptyState title="No facilities registered" description="Register your facility above to appear in the citizen recycler directory and recycler-matching results." />}
      <div className="grid md:grid-cols-2 gap-4">
        {facilities.map((f, i) => (
          <motion.div key={f.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="font-medium">{f.name}</p>
            <p className="text-xs text-gray-400 mt-1">{f.accepted_materials || "—"}</p>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

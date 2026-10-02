"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, listMyReports, createReport } from "@/lib/api";

const CATEGORIES = ["illegal_dumping", "missed_pickup", "overflow", "hazardous", "other"];

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [submitting, setSubmitting] = useState(false);

  function refresh() {
    const token = getToken();
    if (!token) return;
    listMyReports(token).then(setReports).catch(() => {});
  }

  useEffect(refresh, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) return;
    setSubmitting(true);
    try {
      await createReport(token, category);
      refresh();
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="max-w-2xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Reports</h1>

      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm mb-8 flex gap-3 items-end">
        <div className="flex-1">
          <label className="block text-sm text-gray-500 mb-1">Category</label>
          <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full px-3 py-2 rounded-lg border border-gray-200 capitalize">
            {CATEGORIES.map((c) => <option key={c} value={c}>{c.replace(/_/g, " ")}</option>)}
          </select>
        </div>
        <button disabled={submitting} type="submit" className="px-5 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
          {submitting ? "Submitting…" : "Submit report"}
        </button>
      </form>

      {!getToken() && <EmptyState title="Sign in to file a report" description="Log in to report issues like missed pickups or illegal dumping." />}
      {getToken() && reports.length === 0 && <EmptyState title="No reports yet" description="Reports you file will appear here with their status." />}

      <div className="space-y-2">
        {reports.map((r, i) => (
          <motion.div key={r.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <span className="capitalize">{r.category.replace(/_/g, " ")}</span>
            <span className="text-gray-400 capitalize">{r.status.replace(/_/g, " ")}</span>
          </motion.div>
        ))}
      </div>
    </main>
  );
}

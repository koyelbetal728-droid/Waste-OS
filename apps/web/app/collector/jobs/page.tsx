"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/ui/EmptyState";
import { getToken, listPickups, updatePickupStatus } from "@/lib/api";

const NEXT_STATUS: Record<string, string> = {
  requested: "assigned",
  assigned: "accepted",
  accepted: "en_route",
  en_route: "arrived",
  arrived: "collected",
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [updating, setUpdating] = useState<string | null>(null);

  function refresh() {
    const token = getToken();
    if (!token) return;
    listPickups(token).then(setJobs).catch(() => {});
  }
  useEffect(refresh, []);

  async function advance(job: any) {
    const token = getToken();
    const next = NEXT_STATUS[job.status];
    if (!token || !next) return;
    setUpdating(job.id);
    try {
      await updatePickupStatus(token, job.id, next);
      refresh();
    } finally {
      setUpdating(null);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Jobs</h1>
      {!getToken() && <p className="text-sm text-gray-400">Sign in as a collector to see jobs.</p>}
      {getToken() && jobs.length === 0 && <EmptyState title="No jobs assigned" description="Requested pickups will appear here — accept one to start the job." />}
      <div className="space-y-3">
        {jobs.map((j, i) => (
          <motion.div key={j.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <div>
              <p className="font-medium">{j.latitude?.toFixed(3)}, {j.longitude?.toFixed(3)}</p>
              <p className="text-xs text-gray-400 capitalize">{j.status.replace(/_/g, " ")}</p>
            </div>
            {NEXT_STATUS[j.status] && (
              <button onClick={() => advance(j)} disabled={updating === j.id}
                className="px-4 py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
                {updating === j.id ? "Updating…" : `Mark ${NEXT_STATUS[j.status].replace(/_/g, " ")}`}
              </button>
            )}
          </motion.div>
        ))}
      </div>
    </main>
  );
}

"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { getToken, listPickups } from "@/lib/api";

const TODAY = () => new Date().toDateString();

export default function CollectorDashboard() {
  const [openJobs, setOpenJobs] = useState(0);
  const [completedToday, setCompletedToday] = useState(0);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    listPickups(token).then((pickups: any[]) => {
      setOpenJobs(pickups.filter((p) => !["collected", "verified", "cancelled", "failed"].includes(p.status)).length);
      setCompletedToday(
        pickups.filter((p) => ["collected", "verified"].includes(p.status) && new Date(p.updated_at || p.created_at).toDateString() === TODAY()).length
      );
    }).catch(() => {});
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Today</h1>
      <div className="grid grid-cols-2 gap-5 mb-4">
        <StatCard label="Open jobs" value={openJobs} />
        <StatCard label="Completed today" value={completedToday} delay={0.05} />
      </div>
      <p className="text-xs text-gray-400">
        Earnings aren't tracked yet — see the Earnings tab for what's still needed.
      </p>
    </main>
  );
}

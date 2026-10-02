"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { fetchMunicipalityAnalytics } from "@/lib/api";

export default function AdminDashboard() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { fetchMunicipalityAnalytics().then(setData).catch(() => {}); }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">System overview</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
        <StatCard label="Total waste records" value={data?.total_waste_records ?? 0} />
        <StatCard label="Open reports" value={data?.open_reports ?? 0} delay={0.05} />
        <StatCard label="Active hotspots" value={data?.active_hotspots ?? 0} delay={0.1} />
        <StatCard label="Recycling rate" value={data?.recycling_rate ?? 0} suffix="%" delay={0.15} />
      </div>
    </main>
  );
}

"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { getToken, getSustainabilitySummary } from "@/lib/api";

export default function SustainabilityPage() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    getSustainabilitySummary(token).then(setSummary).catch(() => {});
  }, []);

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Sustainability Report</h1>
      {!getToken() && <p className="text-sm text-gray-400">Sign in to view your sustainability report.</p>}
      {summary && (
        <>
          <div className="grid grid-cols-2 gap-5 mb-4">
            <StatCard label="Landfill diverted" value={summary.diverted_kg} suffix=" kg" />
            <StatCard label="Diversion rate" value={summary.diversion_rate_pct} suffix="%" delay={0.05} />
            <StatCard label="Carbon avoided (est.)" value={summary.estimated_carbon_avoided_kg_co2e} suffix=" kg CO2e" delay={0.1} />
            <StatCard label="Total waste tracked" value={summary.total_kg} suffix=" kg" delay={0.15} />
          </div>
          <p className="text-xs text-gray-400">{summary.note}</p>
        </>
      )}
    </main>
  );
}

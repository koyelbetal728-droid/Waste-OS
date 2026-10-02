"use client";
import { useEffect, useState } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { fetchListings, fetchFacilities, getToken, fetchMyPurchases } from "@/lib/api";

export default function RecyclerDashboard() {
  const [listings, setListings] = useState<any[]>([]);
  const [purchases, setPurchases] = useState<any[]>([]);
  const [facilities, setFacilities] = useState<any[]>([]);

  useEffect(() => {
    fetchListings().then(setListings).catch(() => {});
    fetchFacilities("recycler_facility").then(setFacilities).catch(() => {});
    const token = getToken();
    if (token) fetchMyPurchases(token).then(setPurchases).catch(() => {});
  }, []);

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Marketplace overview</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
        <StatCard label="Active listings" value={listings.length} />
        <StatCard label="Materials tracked" value={new Set(listings.map((l) => l.material)).size} delay={0.05} />
        <StatCard label="Your purchases" value={purchases.length} delay={0.1} />
        <StatCard label="Registered facilities" value={facilities.length} delay={0.15} />
      </div>
    </main>
  );
}

"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { fetchListings } from "@/lib/api";
import Link from "next/link";

const SAMPLE_LISTINGS = [
  {
    id: "sample-1",
    material: "PET Flakes (Clear A-Grade)",
    quantity_kg: 2400,
    quality: "Sorted & Washed (99.2% Purity)",
    price_min: 38,
    price_max: 44,
    status: "Verified Batch",
    tag: "High Demand",
    icon: "🍾",
  },
  {
    id: "sample-2",
    material: "HDPE Pellets (Recycled Blow-Moulding)",
    quantity_kg: 1850,
    quality: "Extruded & Degassed",
    price_min: 52,
    price_max: 60,
    status: "Passport #WP-882",
    tag: "EPR Compliant",
    icon: "🛢️",
  },
  {
    id: "sample-3",
    material: "Corrugated Cardboard (OCC 11)",
    quantity_kg: 5000,
    quality: "Baled & Moisture < 8%",
    price_min: 14,
    price_max: 18,
    status: "Ready For Haul",
    tag: "Direct Mill",
    icon: "📦",
  },
  {
    id: "sample-4",
    material: "Aluminium Can Bales (UBC Grade)",
    quantity_kg: 920,
    quality: "Briqueted 98% Aluminum",
    price_min: 110,
    price_max: 125,
    status: "Verified Batch",
    tag: "Instant Escrow",
    icon: "🥫",
  },
  {
    id: "sample-5",
    material: "Copper Scrap (Millberry Grade 1)",
    quantity_kg: 450,
    quality: "Stripped Clean Wire",
    price_min: 680,
    price_max: 720,
    status: "Certified Origin",
    tag: "Premium",
    icon: "⚡",
  },
  {
    id: "sample-6",
    material: "Bio-Waste Digestate Pellets",
    quantity_kg: 3200,
    quality: "Composted Organic Fertilizer",
    price_min: 8,
    price_max: 12,
    status: "Organic Certified",
    tag: "Agricultural",
    icon: "🌱",
  },
];

export default function MarketplacePage() {
  const [listings, setListings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState("All");

  useEffect(() => {
    fetchListings()
      .then((data) => {
        if (data && data.length > 0) {
          setListings(data);
        } else {
          setListings(SAMPLE_LISTINGS);
        }
      })
      .catch(() => {
        setListings(SAMPLE_LISTINGS);
      })
      .finally(() => setLoading(false));
  }, []);

  const baseListings = listings.length > 0 ? listings : SAMPLE_LISTINGS;
  const displayListings = baseListings.filter((l) => {
    if (activeCategory === "All") return true;
    const text = `${l.material || ""} ${l.quality || ""} ${l.tag || ""}`.toLowerCase();
    if (activeCategory === "Polymers") return text.includes("pet") || text.includes("hdpe") || text.includes("plastic") || text.includes("polymer");
    if (activeCategory === "Metals") return text.includes("aluminium") || text.includes("aluminum") || text.includes("copper") || text.includes("metal") || text.includes("steel");
    if (activeCategory === "Paper & Cardboard") return text.includes("cardboard") || text.includes("paper") || text.includes("occ");
    if (activeCategory === "Organics") return text.includes("bio") || text.includes("digestate") || text.includes("organic") || text.includes("compost") || text.includes("food");
    return true;
  });

  return (
    <main className="min-h-screen bg-mesh-radial bg-slate-50 text-slate-800 px-4 sm:px-6 py-12">
      <div className="max-w-6xl mx-auto">
        {/* Navigation & Header */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/" className="text-sm font-semibold text-emerald-600 hover:text-emerald-700 transition-colors">
            ← Back to Hub
          </Link>
          <Link
            href="/scan"
            className="btn-gradient-eco text-white text-xs font-bold px-4 py-2 rounded-full shadow-md"
          >
            + Create New Listing
          </Link>
        </div>

        <div className="text-center max-w-2xl mx-auto mb-10">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-100/70 px-3.5 py-1 rounded-full">
            B2B Secondary Materials Exchange
          </span>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 mt-3 mb-2 tracking-tight">
            Circular Marketplace
          </h1>
          <p className="text-sm text-slate-600">
            Discover verified, traceably audited recyclable material listings directly from waste processors and municipality recovery facilities.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap gap-2 justify-center mb-10">
          {["All", "Polymers", "Metals", "Paper & Cardboard", "Organics"].map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`text-xs font-bold px-4 py-2 rounded-full transition-all ${
                activeCategory === cat
                  ? "bg-slate-900 text-white shadow-md"
                  : "bg-white text-slate-600 border border-slate-200 hover:border-emerald-400"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Listings Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayListings.map((l, i) => (
            <motion.div
              key={l.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              whileHover={{ y: -6, scale: 1.01 }}
              className="glass-card rounded-3xl p-6 relative overflow-hidden flex flex-col justify-between group"
            >
              {/* Top Accent Gradient */}
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 to-teal-400 opacity-70 group-hover:opacity-100 transition-opacity" />

              <div>
                <div className="flex items-start justify-between mb-4">
                  <span className="text-3xl p-2 rounded-2xl bg-emerald-50 border border-emerald-100/80 group-hover:scale-110 transition-transform">
                    {l.icon || "♻️"}
                  </span>
                  <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-100/80 text-emerald-800 border border-emerald-200/60">
                    {l.tag || l.status}
                  </span>
                </div>

                <h3 className="font-extrabold text-lg text-slate-900 group-hover:text-emerald-700 transition-colors">
                  {l.material}
                </h3>
                <p className="text-xs text-slate-500 mt-1 mb-4">
                  {l.quality ?? "High Purity Grade"}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <div>
                  <span className="text-[11px] text-slate-400 block font-medium">Batch Weight</span>
                  <span className="text-sm font-bold text-slate-800 font-mono">
                    {l.quantity_kg?.toLocaleString()} kg
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-[11px] text-slate-400 block font-medium">Spot Price</span>
                  <span className="text-base font-extrabold text-emerald-600 font-mono">
                    ₹{l.price_min ?? "-"}–₹{l.price_max ?? "-"}
                    <span className="text-[10px] text-slate-400 font-sans">/kg</span>
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  );
}

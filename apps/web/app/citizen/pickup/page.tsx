"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { getToken, createPickup } from "@/lib/api";
import { useGeolocation } from "@/hooks/useGeolocation";

export default function PickupPage() {
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [status, setStatus] = useState<"idle" | "creating" | "done" | "error">("idle");
  const geo = useGeolocation();

  function useMyLocation() {
    geo.request();
  }

  // Once the browser actually reports a real position, fill the fields —
  // never before, and never with a guessed coordinate.
  if (geo.position && lat === "" && lon === "") {
    setLat(String(geo.position.latitude));
    setLon(String(geo.position.longitude));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token || !lat || !lon) { setStatus("error"); return; }
    setStatus("creating");
    try {
      await createPickup(token, parseFloat(lat), parseFloat(lon));
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  return (
    <main className="max-w-md mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Schedule a pickup</h1>
      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm space-y-4">
        <button type="button" onClick={useMyLocation}
          className="text-xs px-3 py-1.5 rounded-full border border-gray-200 hover:border-eco-600 hover:text-eco-600 transition-colors">
          {geo.status === "locating" ? "Locating…" : "Use my current location"}
        </button>
        {geo.status === "denied" && <p className="text-xs text-red-500">Location access denied — enter coordinates manually below.</p>}
        {geo.status === "unsupported" && <p className="text-xs text-gray-400">Geolocation isn't available in this browser — enter coordinates manually.</p>}

        <div>
          <label className="block text-sm text-gray-500 mb-1">Latitude</label>
          <input value={lat} onChange={(e) => setLat(e.target.value)} required placeholder="e.g. 22.5726"
            className="w-full px-3 py-2 rounded-lg border border-gray-200" />
        </div>
        <div>
          <label className="block text-sm text-gray-500 mb-1">Longitude</label>
          <input value={lon} onChange={(e) => setLon(e.target.value)} required placeholder="e.g. 88.3639"
            className="w-full px-3 py-2 rounded-lg border border-gray-200" />
        </div>
        <button type="submit" className="w-full py-2 rounded-full bg-eco-600 text-white font-medium hover:bg-eco-900 transition-colors">
          {status === "creating" ? "Requesting…" : "Request pickup"}
        </button>
        {status === "done" && (
          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-eco-600 text-sm text-center">
            Pickup requested — you'll be notified once assigned.
          </motion.p>
        )}
        {status === "error" && <p className="text-red-500 text-sm text-center">Enter a location and sign in to request a pickup.</p>}
      </form>
    </main>
  );
}

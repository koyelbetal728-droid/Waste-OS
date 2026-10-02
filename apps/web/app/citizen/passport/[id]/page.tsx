"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getPassport } from "@/lib/api";

const STAGES = ["created", "identified", "collected", "sorted", "transported", "processing", "recycled"];

export default function PassportPage({ params }: { params: { id: string } }) {
  const [passport, setPassport] = useState<any>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getPassport(params.id).then(setPassport).catch(() => setError(true));
  }, [params.id]);

  const completedStages = new Set((passport?.events ?? []).map((e: any) => e.stage));

  return (
    <main className="max-w-lg mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Waste Passport</h1>
      {error && <p className="text-sm text-gray-400">Passport not found — it's created once your scan finishes processing.</p>}
      {passport && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <p className="text-xs text-gray-400 mb-6">QR token: {passport.qr_token}</p>
          <div className="space-y-4">
            {STAGES.map((stage, i) => {
              const done = completedStages.has(stage);
              return (
                <motion.div key={stage} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.06 }}
                  className="flex items-center gap-3">
                  <span className={`w-2.5 h-2.5 rounded-full ${done ? "bg-eco-600" : "bg-gray-200"}`} />
                  <span className={`text-sm capitalize ${done ? "font-medium" : "text-gray-400"}`}>{stage}</span>
                </motion.div>
              );
            })}
          </div>
        </div>
      )}
    </main>
  );
}

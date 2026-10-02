"use client";
import { motion } from "framer-motion";

export function StatCard({ label, value, suffix = "", delay = 0 }: { label: string; value: number | string; suffix?: string; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <span className="text-3xl font-bold">{value}{suffix}</span>
      <p className="text-sm text-gray-500 mt-1">{label}</p>
    </motion.div>
  );
}

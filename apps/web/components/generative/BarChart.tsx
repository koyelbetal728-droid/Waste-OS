"use client";
import { motion } from "framer-motion";

export function BarChart({ labels, values, unit = "" }: { labels: string[]; values: number[]; unit?: string }) {
  const max = Math.max(...values, 1);
  return (
    <div className="space-y-2">
      {labels.map((label, i) => (
        <div key={label} className="flex items-center gap-3">
          <span className="text-xs text-gray-500 w-24 truncate">{label}</span>
          <div className="flex-1 h-6 bg-gray-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${(values[i] / max) * 100}%` }}
              transition={{ delay: i * 0.06, duration: 0.5 }}
              className="h-full bg-eco-600 rounded-full"
            />
          </div>
          <span className="text-xs text-gray-500 w-14 text-right">{values[i]}{unit}</span>
        </div>
      ))}
    </div>
  );
}

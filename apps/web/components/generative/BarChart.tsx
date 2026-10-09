"use client";
import { motion } from "framer-motion";

export function BarChart({ labels = [], values = [], unit = "" }: { labels: string[]; values: number[]; unit?: string }) {
  const safeValues = values ?? [];
  const max = Math.max(...safeValues, 1);
  return (
    <div className="space-y-3">
      {(labels ?? []).map((label, i) => {
        const val = safeValues[i] ?? 0;
        return (
          <div key={`${label}-${i}`} className="group flex items-center gap-3">
            <span className="text-xs font-medium text-slate-600 w-28 truncate group-hover:text-emerald-700 transition-colors">
              {label}
            </span>
            <div className="flex-1 h-7 bg-slate-100 rounded-xl overflow-hidden p-0.5 border border-slate-200/50">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(100, Math.max(0, (val / max) * 100))}%` }}
                transition={{ delay: i * 0.08, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
                className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 rounded-lg relative overflow-hidden group-hover:brightness-110 shadow-sm"
              >
                <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.div>
            </div>
            <span className="text-xs font-bold text-slate-700 w-16 text-right font-mono">
              {val}
              <span className="text-[10px] text-slate-400 ml-0.5 font-sans">{unit}</span>
            </span>
          </div>
        );
      })}
    </div>
  );
}

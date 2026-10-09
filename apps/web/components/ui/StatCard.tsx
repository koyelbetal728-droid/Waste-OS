"use client";
import { motion } from "framer-motion";

export function StatCard({
  label,
  value,
  suffix = "",
  delay = 0,
  icon,
}: {
  label: string;
  value: number | string;
  suffix?: string;
  delay?: number;
  icon?: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      whileHover={{ y: -5, scale: 1.02 }}
      transition={{ delay, duration: 0.4, type: "spring", stiffness: 300, damping: 20 }}
      className="relative overflow-hidden rounded-2xl border border-emerald-100/80 bg-white/90 backdrop-blur-md p-6 shadow-sm hover:shadow-glow-sm hover:border-emerald-300 transition-all duration-300 group"
    >
      {/* Top accent glowing gradient line */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 opacity-60 group-hover:opacity-100 transition-opacity" />

      {/* Ambient background light circle */}
      <div className="absolute -right-8 -bottom-8 w-24 h-24 rounded-full bg-emerald-100/40 blur-2xl group-hover:bg-emerald-200/50 transition-colors pointer-events-none" />

      <div className="flex items-start justify-between">
        <div>
          <span className="text-3xl font-extrabold tracking-tight text-slate-800 group-hover:text-emerald-700 transition-colors">
            {value}
            <span className="text-emerald-500 font-semibold text-2xl">{suffix}</span>
          </span>
          <p className="text-xs font-medium text-slate-500 mt-2 tracking-wide uppercase">{label}</p>
        </div>
        {icon && (
          <span className="text-2xl p-2.5 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100/60 shadow-sm group-hover:scale-110 group-hover:rotate-6 transition-transform">
            {icon}
          </span>
        )}
      </div>
    </motion.div>
  );
}

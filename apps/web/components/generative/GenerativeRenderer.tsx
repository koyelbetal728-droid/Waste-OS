"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { StatCard } from "@/components/ui/StatCard";
import { BarChart } from "@/components/generative/BarChart";
import { getToken } from "@/lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type GenerativeBlock = {
  type: string;
  title: string;
  data: any;
};

function StatGrid({ block }: { block: GenerativeBlock }) {
  return (
    <div>
      <p className="text-sm font-medium mb-3">{block.title}</p>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {block.data.stats.map((s: any, i: number) => (
          <StatCard key={s.label} label={s.label} value={s.value} suffix={s.suffix} delay={i * 0.05} />
        ))}
      </div>
      {block.data.follow_up && (
        <div className="mt-4">
          <GenerativeRenderer block={block.data.follow_up} />
        </div>
      )}
    </div>
  );
}

function ChartBar({ block }: { block: GenerativeBlock }) {
  return (
    <div>
      <p className="text-sm font-medium mb-3">{block.title}</p>
      <div className="rounded-2xl border border-gray-200 bg-white p-4">
        <BarChart labels={block.data.labels} values={block.data.values} unit={` ${block.data.unit || ""}`} />
      </div>
    </div>
  );
}

function ListBlock({ block }: { block: GenerativeBlock }) {
  return (
    <div>
      <p className="text-sm font-medium mb-3">{block.title}</p>
      <div className="space-y-2">
        {block.data.items.map((item: any, i: number) => (
          <motion.div key={i} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-3 text-sm">
            <div>
              <p className="font-medium">{item.title}</p>
              {item.subtitle && <p className="text-xs text-gray-400">{item.subtitle}</p>}
            </div>
            {item.badge && <span className="text-xs px-2 py-1 rounded-full bg-eco-50 text-eco-600 capitalize">{item.badge}</span>}
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function FormBlock({ block }: { block: GenerativeBlock }) {
  const [values, setValues] = useState<Record<string, any>>(
    Object.fromEntries(block.data.fields.map((f: any) => [f.name, f.default ?? ""]))
  );
  const [status, setStatus] = useState<"idle" | "submitting" | "done" | "error">("idle");
  const [locating, setLocating] = useState(false);

  const hasGeoFields = block.data.fields.some((f: any) => f.geolocation);

  function useMyLocation() {
    if (typeof navigator === "undefined" || !navigator.geolocation) return;
    setLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setValues((v) => ({ ...v, latitude: pos.coords.latitude, longitude: pos.coords.longitude }));
        setLocating(false);
      },
      () => setLocating(false),
      { timeout: 8000 }
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const token = getToken();
    if (!token) { setStatus("error"); return; }
    setStatus("submitting");
    try {
      const res = await fetch(`${API_URL}${block.data.submit_endpoint}`, {
        method: block.data.submit_method,
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(values),
      });
      setStatus(res.ok ? "done" : "error");
    } catch {
      setStatus("error");
    }
  }

  return (
    <div>
      <p className="text-sm font-medium mb-3">{block.title}</p>
      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-200 bg-white p-4 space-y-3">
        {hasGeoFields && (
          <button type="button" onClick={useMyLocation}
            className="text-xs px-3 py-1.5 rounded-full border border-gray-200 hover:border-eco-600 hover:text-eco-600 transition-colors">
            {locating ? "Locating…" : "Use my current location"}
          </button>
        )}
        {block.data.fields.map((f: any) => (
          <div key={f.name}>
            <label className="block text-xs text-gray-500 mb-1">{f.label}</label>
            <input
              type={f.type}
              value={values[f.name]}
              placeholder={f.geolocation ? "e.g. 22.5726" : undefined}
              onChange={(e) => setValues({ ...values, [f.name]: f.type === "number" ? parseFloat(e.target.value) : e.target.value })}
              className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm"
            />
          </div>
        ))}
        <button disabled={status === "submitting"} type="submit"
          className="w-full py-2 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
          {status === "submitting" ? "Submitting…" : block.data.submit_label || "Submit"}
        </button>
        {status === "done" && <p className="text-xs text-eco-600 text-center">Done.</p>}
        {status === "error" && <p className="text-xs text-red-500 text-center">Something went wrong — sign in and try again.</p>}
      </form>
    </div>
  );
}

function TextBlock({ block }: { block: GenerativeBlock }) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-4">
      {block.title && block.title !== "Assistant" && <p className="text-sm font-medium mb-1">{block.title}</p>}
      <p className="text-sm text-gray-600">{block.data.message}</p>
    </div>
  );
}

export function GenerativeRenderer({ block }: { block: GenerativeBlock }) {
  switch (block.type) {
    case "stat_grid": return <StatGrid block={block} />;
    case "chart_bar": return <ChartBar block={block} />;
    case "list": return <ListBlock block={block} />;
    case "form": return <FormBlock block={block} />;
    case "text":
    default:
      return <TextBlock block={block} />;
  }
}

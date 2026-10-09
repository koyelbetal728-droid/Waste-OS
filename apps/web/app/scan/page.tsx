"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { uploadScan, getScanResult, getToken, AuthError } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";

type Stage = "idle" | "uploading" | "processing" | "completed" | "failed";

export default function ScanPage() {
  const [stage, setStage] = useState<Stage>("idle");
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  useEffect(() => {
    if (!getToken()) router.replace("/login");
  }, [router]);

  async function handleFile(file: File) {
    const token = getToken() ?? undefined;
    if (!token) {
      router.replace("/login");
      return;
    }
    setPreview(URL.createObjectURL(file));
    setStage("uploading");
    setResult(null);
    setError(null);
    try {
      const job = await uploadScan(file, token);
      setStage("processing");
      for (let i = 0; i < 40; i++) {
        await new Promise((r) => setTimeout(r, 1000));
        const res = await getScanResult(job.waste_id, token);
        if (res.status === "completed") {
          setResult(res);
          setStage("completed");
          return;
        }
        if (res.status === "failed") {
          setError("The vision pipeline rejected this image. Try another photo.");
          setStage("failed");
          return;
        }
      }
      setError("Scan timed out. Make sure the API is running.");
      setStage("failed");
    } catch (e: any) {
      if (e instanceof AuthError) {
        router.replace("/login");
        return;
      }
      setError(e?.message || "Scan failed. Make sure the API is running.");
      setStage("failed");
    }
  }

  return (
    <main className="min-h-screen bg-mesh-radial bg-slate-900 text-slate-100 px-4 sm:px-6 py-12 relative overflow-hidden">
      {/* Background glow orbs */}
      <div className="absolute top-10 left-10 w-96 h-96 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />

      {/* Nav */}
      <div className="max-w-xl mx-auto flex items-center justify-between mb-8">
        <Link href="/" className="flex items-center gap-2 text-sm font-semibold text-emerald-400 hover:text-emerald-300 transition-colors">
          <span>← Back to Hub</span>
        </Link>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest">Neural Vision v11.4</span>
        </div>
      </div>

      <div className="max-w-xl mx-auto">
        <div className="text-center mb-8">
          <span className="text-xs font-bold uppercase tracking-widest text-emerald-400 bg-emerald-950/70 border border-emerald-500/30 px-3.5 py-1 rounded-full">
            Autonomous Material Inspector
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white mt-3 mb-2 tracking-tight">
            AI Waste Scanner
          </h1>
          <p className="text-slate-400 text-sm">
            Point your lens at any packaging, metal, or scrap. The deep neural network calculates purity, resale grade & recyclability in milliseconds.
          </p>
        </div>

        {/* Viewfinder Box */}
        <div
          onClick={() => inputRef.current?.click()}
          className="relative group border-2 border-dashed border-emerald-500/40 hover:border-emerald-400 rounded-3xl aspect-square flex flex-col items-center justify-center cursor-pointer overflow-hidden bg-slate-950/70 backdrop-blur-xl shadow-2xl transition-all duration-300"
        >
          {/* Cyber Corner Targeting Marks */}
          <div className="absolute top-3 left-3 w-5 h-5 border-t-2 border-l-2 border-emerald-400 group-hover:scale-110 transition-transform" />
          <div className="absolute top-3 right-3 w-5 h-5 border-t-2 border-r-2 border-emerald-400 group-hover:scale-110 transition-transform" />
          <div className="absolute bottom-3 left-3 w-5 h-5 border-b-2 border-l-2 border-emerald-400 group-hover:scale-110 transition-transform" />
          <div className="absolute bottom-3 right-3 w-5 h-5 border-b-2 border-r-2 border-emerald-400 group-hover:scale-110 transition-transform" />

          {/* Grid lines inside */}
          <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />

          {preview ? (
            <div className="w-full h-full relative">
              <img src={preview} alt="preview" className="object-cover w-full h-full" />
              {/* Laser Line Scanning Effect when active */}
              {(stage === "uploading" || stage === "processing") && (
                <div className="absolute left-0 right-0 h-1.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_20px_#06b6d4] animate-scan-line pointer-events-none" />
              )}
            </div>
          ) : (
            <div className="text-center p-6 space-y-3 z-10">
              <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-3xl mx-auto text-emerald-400 shadow-glow-sm group-hover:scale-110 group-hover:bg-emerald-500/20 transition-all">
                📷
              </div>
              <p className="text-base font-bold text-white">Click to Select or Drop Image</p>
              <p className="text-xs text-slate-400">JPEG, PNG, WEBP up to 25MB</p>
            </div>
          )}

          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />
         </div>

        {/* Status Transitions */}
        <AnimatePresence mode="wait">
          {stage === "uploading" && (
            <motion.div
              key="u"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-6 p-4 rounded-2xl bg-slate-800/80 border border-emerald-500/20 flex items-center gap-3 text-sm text-emerald-300"
            >
              <div className="w-5 h-5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
              <span>Uploading payload to vision inference pipeline…</span>
            </motion.div>
          )}

          {stage === "processing" && (
            <motion.div
              key="p"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-6 p-5 rounded-2xl bg-slate-800/80 border border-cyan-500/30 space-y-2 text-sm shadow-xl"
            >
              <div className="flex items-center justify-between text-xs text-cyan-300 font-mono">
                <span>INFERENCE ENGINE ACTIVE</span>
                <span className="animate-pulse">98.4% GPU LOAD</span>
              </div>
              <div className="h-1.5 w-full bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 animate-shimmer" style={{ width: "80%" }} />
              </div>
              <p className="text-slate-300 text-xs">Extracting polymer spectra & checking contaminants…</p>
            </motion.div>
          )}

          {stage === "failed" && (
            <motion.div
              key="f"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-6 p-5 rounded-2xl bg-red-950/60 border border-red-500/40 text-red-200 text-sm shadow-xl"
            >
              <p className="font-bold flex items-center gap-2">⚠️ Scan Pipeline Notice</p>
              <p className="text-xs text-red-300/80 mt-1">{error || "Make sure the backend API is online."}</p>
            </motion.div>
          )}

          {stage === "completed" && result && (
            <motion.div
              key="r"
              initial={{ opacity: 0, y: 15, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
              className="mt-6 rounded-3xl border border-emerald-500/40 bg-slate-950/90 backdrop-blur-2xl p-6 shadow-glow-md shadow-emerald-500/20 relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400" />

              <div className="flex items-start justify-between mb-4">
                <div>
                  <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-500/30">
                    {(result.confidence ?? 0) >= 0.5 ? "MATCH CONFIRMED" : "NO CONFIDENT MATCH"}
                  </span>
                  <h2 className="text-2xl font-black text-white mt-1">{result.category}</h2>
                  <p className="text-sm text-cyan-300 font-medium">{result.material}</p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-black text-emerald-400 font-mono">
                    {Math.round((result.confidence ?? 0) * 100)}%
                  </span>
                  <p className="text-[10px] text-slate-400 uppercase tracking-widest font-mono">CONFIDENCE</p>
                </div>
              </div>

              {/* Grid Metrics */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 my-4">
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-slate-400 text-[11px] block">Recyclability</span>
                  <p className="text-white font-bold text-sm capitalize mt-0.5 text-emerald-400">
                    {result.recyclability?.replace(/_/g, " ") ?? "Standard"}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-slate-400 text-[11px] block">Contamination</span>
                  <p className="text-white font-bold text-sm capitalize mt-0.5 text-teal-300">
                    {result.contamination_level ?? "Low"}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 col-span-2 sm:col-span-1">
                  <span className="text-slate-400 text-[11px] block">Estimated Value</span>
                  <p className="text-amber-400 font-extrabold text-sm mt-0.5 font-mono">
                    ₹{result.estimated_value_min != null ? result.estimated_value_min : "-"}–₹{result.estimated_value_max != null ? result.estimated_value_max : "-"}
                    <span className="text-[10px] text-slate-400 font-sans">/kg</span>
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 mt-6">
                <Link
                  href="/marketplace"
                  className="btn-gradient-eco flex-1 py-3 text-center text-white text-xs font-bold rounded-xl shadow-lg"
                >
                  List on Marketplace →
                </Link>
                <button
                  onClick={() => { setPreview(null); setStage("idle"); setResult(null); }}
                  className="px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 transition-colors"
                >
                  Scan Another
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}

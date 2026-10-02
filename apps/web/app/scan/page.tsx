"use client";
import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { uploadScan, getScanResult } from "@/lib/api";

type Stage = "idle" | "uploading" | "processing" | "completed" | "failed";

export default function ScanPage() {
  const [stage, setStage] = useState<Stage>("idle");
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File) {
    setPreview(URL.createObjectURL(file));
    setStage("uploading");
    setResult(null);
    try {
      const job = await uploadScan(file);
      setStage("processing");
      // Poll for the real backend result.
      for (let i = 0; i < 20; i++) {
        await new Promise((r) => setTimeout(r, 1000));
        const res = await getScanResult(job.waste_id);
        if (res.status === "completed") {
          setResult(res);
          setStage("completed");
          return;
        }
        if (res.status === "failed") {
          setStage("failed");
          return;
        }
      }
      setStage("failed");
    } catch (e) {
      setStage("failed");
    }
  }

  return (
    <main className="min-h-screen max-w-xl mx-auto px-6 py-16">
      <h1 className="text-2xl font-semibold mb-2">AI Waste Scanner</h1>
      <p className="text-gray-500 text-sm mb-8">
        Upload a photo — the API queues it to the worker, runs the vision
        pipeline, and returns a structured result below.
      </p>

      <div
        onClick={() => inputRef.current?.click()}
        className="border-2 border-dashed border-gray-300 rounded-2xl aspect-square flex items-center justify-center cursor-pointer overflow-hidden bg-white hover:border-eco-600 transition-colors"
      >
        {preview ? (
          <img src={preview} alt="preview" className="object-cover w-full h-full" />
        ) : (
          <span className="text-gray-400 text-sm">Click to select an image</span>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
      </div>

      <AnimatePresence mode="wait">
        {stage === "uploading" && (
          <motion.p key="u" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="mt-6 text-sm text-gray-500">
            Uploading…
          </motion.p>
        )}
        {stage === "processing" && (
          <motion.div key="p" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="mt-6 space-y-2 text-sm text-gray-500">
            <p>Analyzing image…</p>
            <p>Checking material and contamination…</p>
            <p>Evaluating recyclability…</p>
          </motion.div>
        )}
        {stage === "failed" && (
          <motion.p key="f" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-6 text-sm text-red-500">
            Scan failed. Make sure the API and worker containers are running.
          </motion.p>
        )}
        {stage === "completed" && result && (
          <motion.div
            key="r"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
          >
            <h2 className="font-semibold text-lg">{result.category}</h2>
            <p className="text-sm text-gray-500 mb-4">{result.material}</p>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div><span className="text-gray-400">Confidence</span><p>{Math.round((result.confidence ?? 0) * 100)}%</p></div>
              <div><span className="text-gray-400">Recyclability</span><p className="capitalize">{result.recyclability?.replace(/_/g, " ")}</p></div>
              <div><span className="text-gray-400">Contamination</span><p className="capitalize">{result.contamination_level}</p></div>
              <div><span className="text-gray-400">Est. value</span><p>₹{result.estimated_value_min ?? "-"}–₹{result.estimated_value_max ?? "-"}</p></div>
            </div>
            {result.is_mock_model && (
              <p className="mt-4 text-xs text-amber-600 bg-amber-50 rounded-lg px-3 py-2">
                Untrained placeholder model — this is not a real classification. Train a real model (see README) to get accurate results.
              </p>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

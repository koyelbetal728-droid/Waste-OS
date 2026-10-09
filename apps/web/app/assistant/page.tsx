"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { getToken, queryAssistant } from "@/lib/api";
import { GenerativeRenderer, GenerativeBlock } from "@/components/generative/GenerativeRenderer";

type Turn = { role: "user" | "assistant"; text?: string; block?: GenerativeBlock; id: number };

const SUGGESTIONS = [
  "How much waste do I have?",
  "What's my recycling rate?",
  "Schedule a pickup",
  "How many Green Points do I have?",
  "Show marketplace listings",
  "Show hotspots",
];

let idCounter = 0;

export default function AssistantPage() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns]);

  async function send(message: string) {
    if (!message.trim()) return;
    const token = getToken();
    setTurns((t) => [...t, { role: "user", text: message, id: idCounter++ }]);
    setInput("");
    if (!token) {
      setTurns((t) => [
        ...t,
        {
          role: "assistant",
          text: "Please sign in to view your real-time waste logs, rewards, and scheduled collection routes.",
          id: idCounter++,
        },
      ]);
      return;
    }
    setLoading(true);
    try {
      const result = await queryAssistant(token, message);
      setTurns((t) => [...t, { role: "assistant", block: result, id: idCounter++ }]);
    } catch {
      setTurns((t) => [
        ...t,
        {
          role: "assistant",
          text: "I couldn't reach the live backend API. Ensure your backend server is running on localhost:8000.",
          id: idCounter++,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex flex-col max-w-3xl mx-auto px-4 sm:px-6 bg-mesh-radial">
      {/* Header */}
      <nav className="py-6 flex items-center justify-between border-b border-emerald-100/60 sticky top-0 bg-white/80 backdrop-blur-md z-20">
        <div className="flex items-center gap-3">
          <Link href="/" className="font-extrabold text-xl text-slate-800 hover:text-emerald-600 transition-colors">
            Waste<span className="text-emerald-600">OS</span>
          </Link>
          <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-200">
            AI Copilot
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
          <span>Autonomous Assistant</span>
        </div>
      </nav>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-6 space-y-5">
        {turns.length === 0 && (
          <div className="py-12 text-center max-w-lg mx-auto">
            <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-cyan-400 text-white flex items-center justify-center text-3xl mx-auto mb-4 shadow-glow-sm shadow-emerald-500/40">
              🤖
            </div>
            <h2 className="text-2xl font-black text-slate-800 mb-2">How can I assist your circular operations?</h2>
            <p className="text-xs text-slate-500 mb-6">
              Ask about material passports, ward forecasts, waste pickups, or current circular spot prices.
            </p>

            <div className="flex flex-wrap gap-2 justify-center">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="text-xs px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:border-emerald-400 hover:bg-emerald-50/50 hover:text-emerald-700 transition-all font-medium text-slate-700 shadow-sm"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence initial={false}>
          {turns.map((turn) => (
            <motion.div
              key={turn.id}
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3 }}
              className={turn.role === "user" ? "flex justify-end" : "flex justify-start"}
            >
              {turn.role === "user" ? (
                <div className="max-w-[80%] rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-600 text-white px-5 py-3 text-sm shadow-md font-medium">
                  {turn.text}
                </div>
              ) : (
                <div className="max-w-full w-full">
                  {turn.block ? (
                    <GenerativeRenderer block={turn.block} />
                  ) : (
                    <div className="rounded-2xl border border-emerald-100 bg-white/90 backdrop-blur-md px-5 py-3.5 text-sm text-slate-700 shadow-sm max-w-lg">
                      {turn.text}
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-xs text-emerald-600 font-semibold px-2 py-1"
          >
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <span>Analyzing neural knowledge base…</span>
          </motion.div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Field */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
        className="py-4 flex gap-2 sticky bottom-0 bg-white/80 backdrop-blur-xl border-t border-slate-100"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about waste, pickups, or recycling..."
          className="flex-1 px-5 py-3.5 rounded-full border border-slate-200 bg-white text-sm focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 shadow-sm"
        />
        <button
          type="submit"
          className="btn-gradient-eco text-white text-sm font-bold px-6 py-3.5 rounded-full shadow-md flex items-center gap-1.5"
        >
          <span>Send</span>
          <span>🚀</span>
        </button>
      </form>
    </main>
  );
}

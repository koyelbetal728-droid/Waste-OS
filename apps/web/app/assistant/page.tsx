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
      setTurns((t) => [...t, { role: "assistant", text: "Sign in to use the assistant — it reads your real waste, rewards and pickup data.", id: idCounter++ }]);
      return;
    }
    setLoading(true);
    try {
      const result = await queryAssistant(token, message);
      setTurns((t) => [...t, { role: "assistant", block: result, id: idCounter++ }]);
    } catch {
      setTurns((t) => [...t, { role: "assistant", text: "Something went wrong reaching the assistant.", id: idCounter++ }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex flex-col max-w-2xl mx-auto px-6">
      <nav className="py-6 flex items-center justify-between">
        <Link href="/" className="font-bold text-lg">WasteOS</Link>
        <span className="text-xs text-gray-400">Assistant</span>
      </nav>

      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {turns.length === 0 && (
          <div className="py-10">
            <p className="text-sm text-gray-400 mb-4">Ask about your waste, recycling rate, pickups, rewards, or the marketplace — I'll pull up the real data.</p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((s) => (
                <button key={s} onClick={() => send(s)}
                  className="text-xs px-3 py-1.5 rounded-full border border-gray-200 hover:border-eco-600 hover:text-eco-600 transition-colors">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence initial={false}>
          {turns.map((turn) => (
            <motion.div key={turn.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              className={turn.role === "user" ? "flex justify-end" : "flex justify-start"}>
              {turn.role === "user" ? (
                <div className="max-w-[80%] rounded-2xl bg-eco-600 text-white px-4 py-2 text-sm">{turn.text}</div>
              ) : (
                <div className="max-w-full w-full">
                  {turn.block ? <GenerativeRenderer block={turn.block} /> : (
                    <div className="rounded-2xl border border-gray-200 bg-white px-4 py-2 text-sm text-gray-600">{turn.text}</div>
                  )}
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-gray-400">Thinking…</motion.div>
        )}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={(e) => { e.preventDefault(); send(input); }} className="py-4 flex gap-2 sticky bottom-0 bg-[#fbfaf8]">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something…"
          className="flex-1 px-4 py-3 rounded-full border border-gray-200 text-sm focus:outline-none focus:border-eco-600"
        />
        <button type="submit" className="px-5 py-3 rounded-full bg-eco-600 text-white text-sm font-medium hover:bg-eco-900 transition-colors">
          Send
        </button>
      </form>
    </main>
  );
}

"use client";
import { motion } from "framer-motion";
import Link from "next/link";

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12 } },
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const LIFECYCLE = ["Generate", "Identify", "Segregate", "Collect", "Route", "Process", "Recycle", "Recover"];

const FEATURES = [
  { title: "AI Waste Scanner", desc: "Point a camera at any item and get instant material identification, contamination and recyclability analysis." },
  { title: "Digital Waste Passport", desc: "Every batch is traced from creation to final recovery — verifiable with a QR code." },
  { title: "Municipality Command Center", desc: "Live hotspot detection, forecasting and route optimization across every ward." },
  { title: "Circular Marketplace", desc: "Recyclers discover and purchase verified, priced material listings directly." },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-6">
        <span className="font-bold text-lg tracking-tight">WasteOS</span>
        <div className="flex gap-5 text-sm items-center">
          <Link href="/assistant" className="text-gray-600 hover:text-eco-600 transition-colors">Assistant</Link>
          <Link href="/marketplace" className="text-gray-600 hover:text-eco-600 transition-colors">Marketplace</Link>
          <Link href="/municipality" className="text-gray-600 hover:text-eco-600 transition-colors">Municipality</Link>
          <Link href="/login" className="text-gray-600 hover:text-eco-600 transition-colors">Sign in</Link>
          <Link href="/scan" className="px-4 py-2 rounded-full bg-eco-600 text-white hover:bg-eco-900 transition-colors">
            Scan Waste
          </Link>
        </div>
      </nav>

      <motion.section
        initial="hidden"
        animate="show"
        variants={stagger}
        className="max-w-4xl mx-auto text-center px-6 pt-16 pb-24"
      >
        <motion.span variants={item} className="inline-block text-xs font-medium tracking-wide uppercase text-eco-600 bg-eco-50 px-3 py-1 rounded-full mb-6">
          AI-Powered Circular Economy OS
        </motion.span>
        <motion.h1 variants={item} className="text-5xl md:text-6xl font-bold tracking-tight leading-tight mb-6">
          Turning Waste<br />Into Value.
        </motion.h1>
        <motion.p variants={item} className="text-lg text-gray-600 max-w-xl mx-auto mb-10">
          AI-powered waste identification, collection, recycling, traceability and
          circular economy management — in one platform.
        </motion.p>
        <motion.div variants={item} className="flex gap-4 justify-center">
          <Link href="/scan" className="px-6 py-3 rounded-full bg-eco-600 text-white font-medium hover:bg-eco-900 transition-colors">
            Scan Waste
          </Link>
          <a href="#lifecycle" className="px-6 py-3 rounded-full border border-gray-300 font-medium hover:border-eco-600 transition-colors">
            Explore Platform
          </a>
        </motion.div>
      </motion.section>

      <section id="lifecycle" className="max-w-5xl mx-auto px-6 py-20">
        <h2 className="text-2xl font-semibold text-center mb-12">The Waste Lifecycle</h2>
        <motion.div
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          variants={stagger}
          className="flex flex-wrap justify-center gap-3"
        >
          {LIFECYCLE.map((stage, i) => (
            <motion.div key={stage} variants={item} className="flex items-center gap-3">
              <span className="px-5 py-2 rounded-full border border-gray-200 bg-white shadow-sm text-sm font-medium">
                {stage}
              </span>
              {i < LIFECYCLE.length - 1 && <span className="text-gray-300">→</span>}
            </motion.div>
          ))}
        </motion.div>
      </section>

      <section className="max-w-6xl mx-auto px-6 py-20">
        <motion.div
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.2 }}
          variants={stagger}
          className="grid md:grid-cols-2 gap-6"
        >
          {FEATURES.map((f) => (
            <motion.div
              key={f.title}
              variants={item}
              whileHover={{ y: -2 }}
              className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
            >
              <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      <footer className="border-t border-gray-100 py-10 text-center text-sm text-gray-400">
        WasteOS — Turning Waste Into Value.
      </footer>
    </main>
  );
}

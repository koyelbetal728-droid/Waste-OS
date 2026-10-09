"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } },
};

const LIFECYCLE = [
  { stage: "Generate", icon: "📦", desc: "Origin audit & barcode generation" },
  { stage: "Identify", icon: "👁️", desc: "Real-time AI neural material classifier" },
  { stage: "Segregate", icon: "🏷️", desc: "Automated purity & fraction separation" },
  { stage: "Collect", icon: "🚛", desc: "Dynamic route & load balancing pickup" },
  { stage: "Route", icon: "🛰️", desc: "Geo-tracked transport with zero detour" },
  { stage: "Process", icon: "⚙️", desc: "Sorting facility intake & contamination check" },
  { stage: "Recycle", icon: "♻️", desc: "Reprocessing into premium circular stock" },
  { stage: "Recover", icon: "💎", desc: "Carbon credit & tokenized value issuance" },
];

const FEATURES = [
  {
    title: "AI Computer Vision Scanner",
    desc: "Scan mixed waste under 1.2s using dual-layer YOLO11 neural models for instant material segregation, contamination analysis, and real-time resale pricing.",
    icon: "⚡",
    badge: "99.4% Precision",
    gradient: "from-emerald-500/10 to-teal-500/10",
    border: "border-emerald-200",
    iconBg: "bg-emerald-500 text-white",
  },
  {
    title: "Digital Waste Passport",
    desc: "Cryptographically traced lifecycle history for every scrap batch. Verifiable QR passports ensure end-to-end compliance with global EPR regulations.",
    icon: "🛡️",
    badge: "Tamper Proof",
    gradient: "from-cyan-500/10 to-blue-500/10",
    border: "border-cyan-200",
    iconBg: "bg-cyan-500 text-white",
  },
  {
    title: "Municipality Command HQ",
    desc: "Predictive municipal heatmaps, overflowing bin hotspot alarms, automated fleet dispatch, and ward-by-ward recycling performance leaderboards.",
    icon: "🗺️",
    badge: "Real-time IoT",
    gradient: "from-indigo-500/10 to-purple-500/10",
    border: "border-indigo-200",
    iconBg: "bg-indigo-500 text-white",
  },
  {
    title: "Circular Raw Materials Exchange",
    desc: "Direct B2B marketplace bridging verified scrap aggregators with industrial recyclers. Real-time spot pricing with escrow settlement.",
    icon: "💹",
    badge: "Zero Intermediary",
    gradient: "from-amber-500/10 to-orange-500/10",
    border: "border-amber-200",
    iconBg: "bg-amber-500 text-white",
  },
];

const METRICS = [
  { value: "48,290", suffix: " kg", label: "Recovered Today", change: "+18.4%" },
  { value: "99.4", suffix: "%", label: "Model Accuracy", change: "YOLOv11s" },
  { value: "1.2", suffix: "s", label: "Avg Scan Time", change: "Sub-second" },
  { value: "128", suffix: " Wards", label: "Active Coverage", change: "Live Fleet" },
];

export default function LandingPage() {
  const [activeStage, setActiveStage] = useState(1);
  const [demoScanned, setDemoScanned] = useState(false);

  return (
    <main className="min-h-screen relative overflow-hidden bg-mesh-radial bg-slate-50 selection:bg-emerald-500 selection:text-white">
      {/* Animated Ambient Light Blobs */}
      <div className="absolute top-12 left-1/4 w-96 h-96 bg-emerald-400/20 rounded-full blur-3xl pointer-events-none animate-float-slow -z-10" />
      <div className="absolute top-80 right-1/4 w-[30rem] h-[30rem] bg-cyan-400/15 rounded-full blur-3xl pointer-events-none animate-float-delayed -z-10" />
      <div className="absolute bottom-20 left-1/3 w-80 h-80 bg-teal-300/20 rounded-full blur-3xl pointer-events-none animate-pulse-glow -z-10" />

      {/* Floating Glass Navbar */}
      <header className="sticky top-4 z-50 max-w-6xl mx-auto px-4 sm:px-6">
        <nav className="glass-panel rounded-full px-6 py-3.5 flex items-center justify-between shadow-lg shadow-emerald-500/5 border border-emerald-200/50">
          <Link href="/" className="flex items-center gap-2.5 group">
            <span className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-cyan-400 flex items-center justify-center text-white text-base font-bold shadow-md shadow-emerald-500/30 group-hover:scale-105 group-hover:rotate-6 transition-transform">
              ♻
            </span>
            <span className="font-extrabold text-xl tracking-tight text-slate-900 group-hover:text-emerald-700 transition-colors">
              Waste<span className="text-emerald-600">OS</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-7 text-sm font-semibold text-slate-600">
            <Link href="/scan" className="hover:text-emerald-600 transition-colors">AI Scanner</Link>
            <Link href="/assistant" className="hover:text-emerald-600 transition-colors">AI Assistant</Link>
            <Link href="/marketplace" className="hover:text-emerald-600 transition-colors">Marketplace</Link>
            <Link href="/municipality" className="hover:text-emerald-600 transition-colors">Municipality</Link>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm font-semibold text-slate-700 hover:text-emerald-600 px-3 py-1.5 transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/scan"
              className="btn-gradient-eco text-white text-xs sm:text-sm font-bold px-5 py-2.5 rounded-full flex items-center gap-2"
            >
              <span className="animate-spin-slow">✨</span>
              <span>Scan Waste</span>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <motion.section
        initial="hidden"
        animate="show"
        variants={stagger}
        className="max-w-5xl mx-auto text-center px-6 pt-16 md:pt-24 pb-16 relative"
      >
        <motion.div variants={item} className="inline-flex items-center gap-2 glass-badge text-emerald-800 px-4 py-1.5 rounded-full text-xs font-bold tracking-wide uppercase shadow-sm mb-6">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
          <span>Next-Gen Circular Economy OS • v2.0</span>
        </motion.div>

        <motion.h1 variants={item} className="text-5xl sm:text-6xl md:text-7xl font-black tracking-tight leading-[1.08] text-slate-900 mb-6">
          Transforming Waste Into{" "}
          <span className="text-gradient-eco inline-block drop-shadow-sm">
            Infinite Value
          </span>
        </motion.h1>

        <motion.p variants={item} className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed mb-10 font-normal">
          Instant computer vision material analysis, automated municipality logistics, and tokenized circular commerce — built to close the loop on global waste.
        </motion.p>

        <motion.div variants={item} className="flex flex-wrap gap-4 justify-center items-center mb-16">
          <Link
            href="/scan"
            className="btn-gradient-eco text-white px-8 py-4 rounded-full font-bold text-base shadow-lg shadow-emerald-500/30 flex items-center gap-3 group"
          >
            <span>Launch Live Scanner</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
          <a
            href="#demo"
            className="px-7 py-4 rounded-full border border-slate-300/80 bg-white/70 backdrop-blur-md font-semibold text-slate-700 hover:border-emerald-500 hover:text-emerald-700 hover:bg-white shadow-sm transition-all"
          >
            View Live Simulation
          </a>
        </motion.div>

        {/* Live Metrics Strip */}
        <motion.div
          variants={item}
          className="grid grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto"
        >
          {METRICS.map((m, i) => (
            <div
              key={i}
              className="glass-card rounded-2xl p-5 text-left relative overflow-hidden"
            >
              <div className="flex items-center justify-between text-xs font-semibold text-emerald-600 mb-2">
                <span>{m.change}</span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {m.value}
                <span className="text-emerald-600 text-lg sm:text-xl font-bold">{m.suffix}</span>
              </div>
              <p className="text-xs text-slate-500 font-medium mt-1">{m.label}</p>
            </div>
          ))}
        </motion.div>
      </motion.section>

      {/* Interactive Live Demo Teaser Section */}
      <section id="demo" className="max-w-5xl mx-auto px-6 py-12">
        <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-emerald-200/60 shadow-xl relative overflow-hidden">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="max-w-md">
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-100/70 px-3 py-1 rounded-full mb-3">
                <span>⚡ Real-Time Demo</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mb-3">
                Try the Vision Classifier
              </h2>
              <p className="text-slate-600 text-sm leading-relaxed mb-6">
                Our lightweight deep neural model separates polymers, metals, organics, and hazardous fractions with real-time purity ratings.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setDemoScanned(!demoScanned)}
                  className="btn-gradient-eco text-white text-xs sm:text-sm font-bold px-5 py-2.5 rounded-full flex items-center gap-2"
                >
                  <span>{demoScanned ? "🔄 Reset Scan" : "▶ Run Sample Scan"}</span>
                </button>
                <Link
                  href="/scan"
                  className="px-5 py-2.5 rounded-full border border-slate-300 text-xs sm:text-sm font-semibold text-slate-700 hover:bg-white transition-colors"
                >
                  Upload Your Photo →
                </Link>
              </div>
            </div>

            {/* Simulated Scanner Window */}
            <div className="w-full md:w-80 h-72 rounded-2xl bg-slate-900 border border-emerald-500/30 relative overflow-hidden flex flex-col justify-between p-4 shadow-2xl text-emerald-400 font-mono text-xs">
              {/* Corner brackets */}
              <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-emerald-400" />
              <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-emerald-400" />
              <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-emerald-400" />
              <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-emerald-400" />

              {/* Scanning Laser Line */}
              <div className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-scan-line pointer-events-none" />

              <div className="flex justify-between items-center text-[10px] text-emerald-400/80 z-10">
                <span>FPS: 60.0</span>
                <span className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                  SENSOR_ONLINE
                </span>
              </div>

              {/* Center Subject Graphic */}
              <div className="my-auto text-center z-10">
                <div className="text-5xl mb-2 filter drop-shadow-[0_0_12px_rgba(16,185,129,0.5)]">
                  {demoScanned ? "🍾" : "📦"}
                </div>
                <div className="text-white text-xs font-bold font-sans">
                  {demoScanned ? "HDPE Bottle Container" : "Awaiting Frame Detection"}
                </div>
              </div>

              {/* Bottom HUD Output */}
              <div className="bg-slate-950/80 rounded-lg p-2.5 border border-emerald-500/20 z-10 space-y-1 text-[11px]">
                <div className="flex justify-between">
                  <span className="text-slate-400 font-sans">Target:</span>
                  <span className="text-emerald-300 font-bold">{demoScanned ? "Plastic (Grade 2)" : "Scanning..."}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 font-sans">Confidence:</span>
                  <span className="text-cyan-300 font-bold">{demoScanned ? "98.7%" : "--%"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 font-sans">Market Value:</span>
                  <span className="text-amber-400 font-bold">{demoScanned ? "₹14.20 / kg" : "--"}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Lifecycle Interactive Timeline */}
      <section id="lifecycle" className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 bg-emerald-100/60 px-3.5 py-1 rounded-full">
            Autonomous Pipeline
          </span>
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mt-3 mb-4">
            The Circular Waste Lifecycle
          </h2>
          <p className="text-slate-600 text-sm">
            Every step is cryptographically audited and optimized in real time from source to recovery.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          {LIFECYCLE.map((s, i) => {
            const isActive = activeStage === i;
            return (
              <motion.div
                key={s.stage}
                whileHover={{ y: -4, scale: 1.03 }}
                onClick={() => setActiveStage(i)}
                className={`cursor-pointer rounded-2xl p-4 text-center transition-all duration-300 flex flex-col items-center justify-between min-h-[140px] border ${
                  isActive
                    ? "bg-gradient-to-b from-emerald-500 to-teal-600 text-white border-emerald-400 shadow-glow-md"
                    : "glass-card text-slate-700 hover:border-emerald-300"
                }`}
              >
                <span className="text-2xl mb-1">{s.icon}</span>
                <span className={`text-xs font-extrabold tracking-tight ${isActive ? "text-white" : "text-slate-800"}`}>
                  {s.stage}
                </span>
                <span className={`text-[10px] leading-tight line-clamp-2 ${isActive ? "text-emerald-100" : "text-slate-500"}`}>
                  {s.desc}
                </span>
                <span className={`text-[9px] font-mono mt-1 px-1.5 py-0.5 rounded ${isActive ? "bg-white/20 text-white" : "bg-slate-100 text-slate-400"}`}>
                  0{i + 1}
                </span>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Feature Showcase Grid */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs font-bold uppercase tracking-wider text-teal-600 bg-teal-100/60 px-3.5 py-1 rounded-full">
            Enterprise Grade
          </span>
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mt-3 mb-4">
            Powering Modern Cities & Recyclers
          </h2>
          <p className="text-slate-600 text-sm">
            Tailored tools for citizens, waste collection operators, sorting hubs, and municipal planners.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              whileHover={{ y: -6 }}
              className={`rounded-3xl border ${f.border} bg-white/90 backdrop-blur-xl p-8 shadow-sm hover:shadow-xl transition-all relative overflow-hidden group`}
            >
              <div className={`absolute top-0 right-0 w-36 h-36 bg-gradient-to-bl ${f.gradient} rounded-bl-full pointer-events-none group-hover:scale-125 transition-transform duration-500`} />
              
              <div className="flex items-start justify-between mb-6">
                <div className={`w-12 h-12 rounded-2xl ${f.iconBg} flex items-center justify-center text-xl shadow-md group-hover:rotate-6 transition-transform`}>
                  {f.icon}
                </div>
                <span className="text-xs font-bold px-3 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                  {f.badge}
                </span>
              </div>

              <h3 className="font-extrabold text-xl text-slate-900 mb-3 group-hover:text-emerald-700 transition-colors">
                {f.title}
              </h3>
              <p className="text-slate-600 text-sm leading-relaxed mb-6">
                {f.desc}
              </p>

              <div className="flex items-center text-xs font-bold text-emerald-600 group-hover:text-emerald-800 gap-1.5">
                <span>Explore Module</span>
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Role Portal Quick Links */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="glass-panel rounded-3xl p-8 border border-emerald-200/50">
          <div className="text-center mb-8">
            <h3 className="text-xl font-bold text-slate-900">Direct Role Dashboards</h3>
            <p className="text-xs text-slate-500 mt-1">Jump straight into designated portal interfaces</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Citizen", href: "/citizen", icon: "🏡" },
              { label: "Collector", href: "/collector", icon: "🚛" },
              { label: "Recycler", href: "/recycler", icon: "🏭" },
              { label: "Municipality", href: "/municipality", icon: "🏛️" },
              { label: "Business", href: "/business", icon: "🏢" },
              { label: "Assistant", href: "/assistant", icon: "🤖" },
            ].map((portal) => (
              <Link
                key={portal.label}
                href={portal.href}
                className="flex flex-col items-center p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-emerald-400 hover:shadow-md hover:-translate-y-1 transition-all text-center group"
              >
                <span className="text-2xl mb-2 group-hover:scale-110 transition-transform">{portal.icon}</span>
                <span className="text-xs font-bold text-slate-800 group-hover:text-emerald-600">{portal.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200/70 bg-white/60 backdrop-blur-md py-12 text-center text-sm text-slate-500">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-lg">♻</span>
            <span className="font-extrabold text-slate-800">Waste<span className="text-emerald-600">OS</span></span>
            <span className="text-xs text-slate-400">© 2026 Circular Intelligence Inc.</span>
          </div>
          <div className="flex items-center gap-6 text-xs font-semibold text-slate-600">
            <Link href="/scan" className="hover:text-emerald-600">Scanner</Link>
            <Link href="/marketplace" className="hover:text-emerald-600">Marketplace</Link>
            <Link href="/assistant" className="hover:text-emerald-600">Copilot</Link>
            <Link href="/municipality" className="hover:text-emerald-600">Command Center</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}

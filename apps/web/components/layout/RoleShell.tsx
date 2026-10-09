"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";

export type NavItem = { label: string; href: string; icon?: string };

export function RoleShell({
  roleName,
  navItems,
  children,
}: {
  roleName: string;
  navItems: NavItem[];
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen flex bg-mesh-radial bg-slate-50/60">
      {/* Sidebar */}
      <aside className="w-64 shrink-0 border-r border-emerald-100/70 bg-white/85 backdrop-blur-xl px-5 py-6 hidden md:flex md:flex-col shadow-sm">
        <div className="flex items-center gap-3 px-2 mb-6">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-cyan-400 flex items-center justify-center text-white font-bold shadow-glow-sm shadow-emerald-500/30">
            ♻
          </div>
          <div>
            <Link href="/" className="font-extrabold text-xl tracking-tight text-slate-800 hover:text-emerald-600 transition-colors">
              Waste<span className="text-emerald-600">OS</span>
            </Link>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[11px] font-semibold text-emerald-800/70 uppercase tracking-wider">{roleName}</span>
            </div>
          </div>
        </div>

        <nav className="flex flex-col gap-1.5 flex-1">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`relative px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 flex items-center gap-3 ${
                  active ? "text-emerald-700 font-semibold" : "text-slate-600 hover:text-slate-900 hover:bg-emerald-50/50"
                }`}
              >
                {active && (
                  <motion.span
                    layoutId={`nav-active-${roleName}`}
                    className="absolute inset-0 bg-gradient-to-r from-emerald-100/80 to-teal-50/60 border border-emerald-200/60 rounded-xl shadow-sm"
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                  />
                )}
                {item.icon && <span className="relative z-10 text-base">{item.icon}</span>}
                <span className="relative z-10">{item.label}</span>
                {active && (
                  <span className="relative z-10 ml-auto w-1.5 h-1.5 rounded-full bg-emerald-600" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Bottom Quick Return */}
        <div className="pt-4 border-t border-slate-100 mt-auto">
          <Link
            href="/"
            className="flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-emerald-600 px-3 py-2 rounded-lg hover:bg-emerald-50/60 transition-colors"
          >
            ← Back to Main Hub
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="md:hidden border-b border-emerald-100 bg-white/90 backdrop-blur-md px-5 py-4 flex items-center justify-between sticky top-0 z-30">
          <div className="flex items-center gap-2">
            <span className="text-xl">♻</span>
            <Link href="/" className="font-extrabold text-lg text-slate-800">Waste<span className="text-emerald-600">OS</span></Link>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-semibold border border-emerald-100">
            {roleName}
          </span>
        </header>

        <div className="flex-1 p-6 md:p-8 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
}

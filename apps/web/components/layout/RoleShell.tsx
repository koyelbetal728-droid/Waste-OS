"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";

export type NavItem = { label: string; href: string };

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
    <div className="min-h-screen flex">
      <aside className="w-56 shrink-0 border-r border-gray-100 bg-white px-4 py-6 hidden md:flex md:flex-col">
        <Link href="/" className="font-bold text-lg tracking-tight px-2 mb-1">WasteOS</Link>
        <span className="text-xs text-gray-400 px-2 mb-6">{roleName}</span>
        <nav className="flex flex-col gap-1">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link key={item.href} href={item.href} className="relative px-3 py-2 rounded-lg text-sm text-gray-600 hover:text-eco-600">
                {active && (
                  <motion.span layoutId={`nav-active-${roleName}`} className="absolute inset-0 bg-eco-50 rounded-lg" transition={{ duration: 0.2 }} />
                )}
                <span className={`relative ${active ? "text-eco-600 font-medium" : ""}`}>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex-1 flex flex-col">
        <header className="md:hidden border-b border-gray-100 bg-white px-4 py-3 flex items-center justify-between">
          <Link href="/" className="font-bold">WasteOS</Link>
          <span className="text-xs text-gray-400">{roleName}</span>
        </header>
        <div className="flex-1">{children}</div>
      </div>
    </div>
  );
}

import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/collector" },
  { label: "Jobs", href: "/collector/jobs" },
  { label: "Routes", href: "/collector/routes" },
  { label: "Inventory", href: "/collector/inventory" },
  { label: "Earnings", href: "/collector/earnings" },
];

export default function CollectorLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Collector" navItems={NAV}>{children}</RoleShell>;
}

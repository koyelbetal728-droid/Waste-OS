import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/citizen" },
  { label: "Assistant", href: "/assistant" },
  { label: "Scan Waste", href: "/scan" },
  { label: "My Waste", href: "/citizen/waste" },
  { label: "Pickup", href: "/citizen/pickup" },
  { label: "Marketplace", href: "/marketplace" },
  { label: "Recyclers", href: "/citizen/recyclers" },
  { label: "Collection Points", href: "/citizen/collection-points" },
  { label: "Rewards", href: "/citizen/rewards" },
  { label: "Impact", href: "/citizen/impact" },
  { label: "Reports", href: "/citizen/reports" },
];

export default function CitizenLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Citizen" navItems={NAV}>{children}</RoleShell>;
}

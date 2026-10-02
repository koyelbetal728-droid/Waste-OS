import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/business" },
  { label: "Waste", href: "/business/waste" },
  { label: "Pickups", href: "/business/pickups" },
  { label: "Sustainability", href: "/business/sustainability" },
];

export default function BusinessLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Business" navItems={NAV}>{children}</RoleShell>;
}

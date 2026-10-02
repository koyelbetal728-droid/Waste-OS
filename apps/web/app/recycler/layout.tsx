import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/recycler" },
  { label: "Listings", href: "/recycler/listings" },
  { label: "Purchases", href: "/recycler/purchases" },
  { label: "Inventory", href: "/recycler/inventory" },
  { label: "Facilities", href: "/recycler/facilities" },
];

export default function RecyclerLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Recycler" navItems={NAV}>{children}</RoleShell>;
}

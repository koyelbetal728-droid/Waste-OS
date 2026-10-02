import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/admin" },
  { label: "Users", href: "/admin/users" },
  { label: "Organizations", href: "/admin/organizations" },
  { label: "Waste Types", href: "/admin/waste-types" },
  { label: "Facilities", href: "/admin/facilities" },
  { label: "System", href: "/admin/system" },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Admin" navItems={NAV}>{children}</RoleShell>;
}

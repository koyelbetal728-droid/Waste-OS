import { RoleShell } from "@/components/layout/RoleShell";

const NAV = [
  { label: "Dashboard", href: "/municipality" },
  { label: "Map", href: "/municipality/map" },
  { label: "Wards", href: "/municipality/wards" },
  { label: "Hotspots", href: "/municipality/hotspots" },
  { label: "Collection", href: "/municipality/collection" },
  { label: "Vehicles", href: "/municipality/vehicles" },
  { label: "Routes", href: "/municipality/routes" },
  { label: "Forecasts", href: "/municipality/forecasts" },
  { label: "Recycling", href: "/municipality/recycling" },
  { label: "Incidents", href: "/municipality/incidents" },
  { label: "Analytics", href: "/municipality/analytics" },
];

export default function MunicipalityLayout({ children }: { children: React.ReactNode }) {
  return <RoleShell roleName="Municipality" navItems={NAV}>{children}</RoleShell>;
}

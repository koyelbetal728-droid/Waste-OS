const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class AuthError extends Error {
  constructor(message = "Your session has expired. Please sign in again.") {
    super(message);
    this.name = "AuthError";
  }
}

async function handleResponse(res: Response) {
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Request failed");
  return res;
}

export async function uploadScan(file: File, token?: string) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/scanning`, {
    method: "POST",
    body: form,
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  });
  await handleResponse(res);
  return res.json();
}

export async function getScanResult(wasteId: string, token?: string) {
  const res = await fetch(`${API_URL}/scanning/${wasteId}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  });
  await handleResponse(res);
  return res.json();
}

export async function fetchListings() {
  const res = await fetch(`${API_URL}/marketplace/listings`);
  if (!res.ok) throw new Error("Failed to fetch listings");
  return res.json();
}

export async function fetchMunicipalityAnalytics() {
  const res = await fetch(`${API_URL}/municipality/analytics`);
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function fetchHotspots() {
  const res = await fetch(`${API_URL}/hotspots`);
  if (!res.ok) throw new Error("Failed to fetch hotspots");
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Invalid email or password");
  return res.json();
}

export async function register(email: string, password: string, full_name: string, role: string) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name, role }),
  });
  if (!res.ok) throw new Error("Registration failed");
  return res.json();
}

export async function getMe(token: string) {
  const res = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch profile");
  return res.json();
}

export async function listMyWaste(token: string) {
  const res = await fetch(`${API_URL}/waste`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch waste records");
  return res.json();
}

export async function createPickup(token: string, latitude: number, longitude: number, waste_id?: string) {
  const res = await fetch(`${API_URL}/pickups`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ latitude, longitude, waste_id }),
  });
  if (!res.ok) throw new Error("Failed to create pickup");
  return res.json();
}

export async function getRewardsBalance(token: string) {
  const res = await fetch(`${API_URL}/rewards/balance`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch rewards");
  return res.json();
}

export async function listMyReports(token: string) {
  const res = await fetch(`${API_URL}/reports`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch reports");
  return res.json();
}

export async function createReport(token: string, category: string, latitude?: number, longitude?: number) {
  const res = await fetch(`${API_URL}/reports`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ category, latitude, longitude }),
  });
  if (!res.ok) throw new Error("Failed to create report");
  return res.json();
}

export async function getPassport(wasteId: string) {
  const res = await fetch(`${API_URL}/passports/${wasteId}`);
  if (!res.ok) throw new Error("Passport not found");
  return res.json();
}

export async function optimizeRoute(token: string, depot: {latitude:number, longitude:number}, stops: {latitude:number, longitude:number}[]) {
  const res = await fetch(`${API_URL}/routes/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ depot, stops }),
  });
  if (!res.ok) throw new Error("Failed to optimize route");
  return res.json();
}

export function saveToken(token: string) {
  if (typeof window !== "undefined") localStorage.setItem("wasteos_token", token);
}
export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("wasteos_token");
}

// ---------- Facilities / vehicles / wards / waste types / admin ----------

export async function fetchFacilities(type?: string) {
  const url = type ? `${API_URL}/facilities?type=${type}` : `${API_URL}/facilities`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch facilities");
  return res.json();
}

export async function createFacility(token: string, payload: any) {
  const res = await fetch(`${API_URL}/facilities`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create facility");
  return res.json();
}

export async function fetchVehicles(token: string) {
  const res = await fetch(`${API_URL}/vehicles`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch vehicles");
  return res.json();
}

export async function createVehicle(token: string, payload: any) {
  const res = await fetch(`${API_URL}/vehicles`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create vehicle");
  return res.json();
}

export async function fetchWards(token: string) {
  const res = await fetch(`${API_URL}/wards`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch wards");
  return res.json();
}

export async function createWard(token: string, payload: any) {
  const res = await fetch(`${API_URL}/wards`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create ward");
  return res.json();
}

export async function fetchWasteTypes() {
  const res = await fetch(`${API_URL}/waste-types`);
  if (!res.ok) throw new Error("Failed to fetch waste types");
  return res.json();
}

export async function createWasteType(token: string, payload: any) {
  const res = await fetch(`${API_URL}/waste-types`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create waste type");
  return res.json();
}

export async function fetchAdminUsers(token: string) {
  const res = await fetch(`${API_URL}/admin/users`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function updateAdminUser(token: string, userId: string, payload: any) {
  const res = await fetch(`${API_URL}/admin/users/${userId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update user");
  return res.json();
}

export async function fetchOrganizations(token: string) {
  const res = await fetch(`${API_URL}/admin/organizations`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch organizations");
  return res.json();
}

export async function createOrganization(token: string, payload: any) {
  const res = await fetch(`${API_URL}/admin/organizations`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create organization");
  return res.json();
}

export async function getSustainabilitySummary(token: string) {
  const res = await fetch(`${API_URL}/waste/sustainability/summary`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch sustainability summary");
  return res.json();
}

export async function listPickups(token: string) {
  const res = await fetch(`${API_URL}/pickups`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch pickups");
  return res.json();
}

export async function updatePickupStatus(token: string, pickupId: string, status: string) {
  const res = await fetch(`${API_URL}/pickups/${pickupId}/status?status=${status}`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to update pickup status");
  return res.json();
}

export async function queryAssistant(token: string, message: string) {
  const res = await fetch(`${API_URL}/assistant/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Assistant request failed");
  return res.json();
}

export async function fetchMyRouteStops(token: string) {
  const res = await fetch(`${API_URL}/pickups/my-route-stops`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch route stops");
  return res.json();
}

export async function fetchMyPurchases(token: string) {
  const res = await fetch(`${API_URL}/purchases/mine`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error("Failed to fetch purchases");
  return res.json();
}

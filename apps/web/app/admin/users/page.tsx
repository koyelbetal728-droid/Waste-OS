"use client";
import { useEffect, useState } from "react";
import { EmptyState } from "@/components/ui/EmptyState";
import { fetchAdminUsers, updateAdminUser, getToken } from "@/lib/api";

export default function AdminUsersPage() {
  const [users, setUsers] = useState<any[]>([]);

  function refresh() {
    const token = getToken();
    if (!token) return;
    fetchAdminUsers(token).then(setUsers).catch(() => {});
  }
  useEffect(refresh, []);

  async function toggleActive(userId: string, current: boolean) {
    const token = getToken();
    if (!token) return;
    await updateAdminUser(token, userId, { is_active: !current });
    refresh();
  }

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Users</h1>
      {!getToken() && <p className="text-sm text-gray-400">Sign in as an admin to manage users.</p>}
      {getToken() && users.length === 0 && <EmptyState title="No users found" description="Registered users will appear here." />}
      <div className="space-y-2">
        {users.map((u) => (
          <div key={u.id} className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-4 text-sm">
            <div>
              <p className="font-medium">{u.full_name}</p>
              <p className="text-xs text-gray-400">{u.email} · <span className="capitalize">{u.role}</span></p>
            </div>
            <button onClick={() => toggleActive(u.id, u.is_active)}
              className={`text-xs px-3 py-1 rounded-full ${u.is_active ? "bg-eco-50 text-eco-600" : "bg-red-50 text-red-500"}`}>
              {u.is_active ? "Active" : "Deactivated"}
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}

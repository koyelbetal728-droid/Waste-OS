"use client";
import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export default function SystemPage() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_URL}/health`).then((r) => r.json()).then(setHealth).catch(() => setHealth({ status: "unreachable" }));
  }, []);

  return (
    <main className="max-w-2xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">System Health</h1>
      {health && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <span className={`w-2.5 h-2.5 rounded-full ${health.status === "healthy" ? "bg-eco-600" : "bg-red-500"}`} />
            <span className="font-medium capitalize">{health.status}</span>
          </div>
          {health.dependencies && Object.entries(health.dependencies).map(([k, v]: any) => (
            <div key={k} className="flex justify-between text-sm py-1 border-t border-gray-100 first:border-0">
              <span className="capitalize">{k}</span>
              <span className={v ? "text-eco-600" : "text-red-500"}>{v ? "OK" : "down"}</span>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}

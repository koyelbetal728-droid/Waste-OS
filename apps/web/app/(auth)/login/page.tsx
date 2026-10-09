"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import { login, saveToken, getMe } from "@/lib/api";

const DEMO_USERS = [
  { label: "Citizen", email: "citizen@wasteos.org", role: "citizen" },
  { label: "Collector", email: "collector@wasteos.org", role: "collector" },
  { label: "Recycler", email: "recycler@wasteos.org", role: "recycler" },
  { label: "Municipality", email: "municipality@wasteos.org", role: "municipality" },
  { label: "Admin", email: "admin@wasteos.org", role: "admin" },
];

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleLogin(targetEmail: string, targetPass: string) {
    setLoading(true);
    setError(null);
    try {
      const { access_token } = await login(targetEmail, targetPass);
      saveToken(access_token);
      try {
        const me = await getMe(access_token);
        if (me?.role) {
          router.push(`/${me.role}`);
          return;
        }
      } catch {}
      router.push("/citizen");
    } catch (e: any) {
      setError(e?.message || "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await handleLogin(email, password);
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-6 py-12">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-sm rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
      >
        <Link href="/" className="font-bold text-lg block mb-1">WasteOS</Link>
        <h1 className="text-xl font-semibold mb-6">Welcome back</h1>

        <form onSubmit={handleSubmit}>
          <label className="block text-sm text-gray-500 mb-1">Email</label>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
            className="w-full mb-4 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600"
          />

          <label className="block text-sm text-gray-500 mb-1">Password</label>
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
            className="w-full mb-2 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600"
          />

          {error && (
            <motion.p initial={{ opacity: 0, x: -4 }} animate={{ opacity: 1, x: 0 }} className="text-red-500 text-sm mb-2">{error}</motion.p>
          )}

          <button
            disabled={loading}
            type="submit"
            className="w-full mt-4 py-2 rounded-full bg-eco-600 text-white font-medium hover:bg-eco-900 transition-colors disabled:opacity-60"
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <div className="mt-6 pt-6 border-t border-gray-100">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2.5">
            Quick Demo Logins
          </p>
          <div className="flex flex-wrap gap-1.5">
            {DEMO_USERS.map((u) => (
              <button
                key={u.role}
                type="button"
                onClick={() => {
                  setEmail(u.email);
                  setPassword("changeme123");
                  handleLogin(u.email, "changeme123");
                }}
                disabled={loading}
                className="text-xs px-2.5 py-1 rounded-md bg-gray-50 hover:bg-eco-50 hover:text-eco-700 text-gray-600 border border-gray-200 transition-colors"
              >
                {u.label}
              </button>
            ))}
          </div>
        </div>

        <p className="text-sm text-gray-400 mt-6 text-center">
          No account? <Link href="/register" className="text-eco-600 font-medium">Register</Link>
        </p>
      </motion.div>
    </main>
  );
}

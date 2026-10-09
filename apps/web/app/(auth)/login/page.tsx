"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import { login, saveToken } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const { access_token } = await login(email, password);
      saveToken(access_token);
      router.push("/citizen");
    } catch (e: any) {
      setError(e?.message || "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <motion.form
        onSubmit={handleSubmit}
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-sm rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
      >
        <Link href="/" className="font-bold text-lg block mb-1">WasteOS</Link>
        <h1 className="text-xl font-semibold mb-6">Welcome back</h1>

        <label className="block text-sm text-gray-500 mb-1">Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required
          className="w-full mb-4 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600" />

        <label className="block text-sm text-gray-500 mb-1">Password</label>
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required
          className="w-full mb-2 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600" />

        {error && (
          <motion.p initial={{ opacity: 0, x: -4 }} animate={{ opacity: 1, x: 0 }} className="text-red-500 text-sm mb-2">{error}</motion.p>
        )}

        <button disabled={loading} type="submit" className="w-full mt-4 py-2 rounded-full bg-eco-600 text-white font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
          {loading ? "Signing in…" : "Sign in"}
        </button>

        <p className="text-sm text-gray-400 mt-4 text-center">
          No account? <Link href="/register" className="text-eco-600">Register</Link>
        </p>
      </motion.form>
    </main>
  );
}

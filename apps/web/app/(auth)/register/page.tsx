"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import { register, login, saveToken } from "@/lib/api";

const ROLES = ["citizen", "collector", "recycler", "business", "municipality"];

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", password: "", full_name: "", role: "citizen" });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register(form.email, form.password, form.full_name, form.role);
      const { access_token } = await login(form.email, form.password);
      saveToken(access_token);
      router.push(`/${form.role}`);
    } catch (e: any) {
      // If registration failed because the email is already taken, the user
      // may well already have an account — try signing in directly instead of
      // blocking them with a generic "registration failed" message.
      try {
        const { access_token } = await login(form.email, form.password);
        saveToken(access_token);
        router.push(`/${form.role}`);
        return;
      } catch {
        const msg = e?.message || "Registration failed — email may already be taken.";
        setError(msg);
      }
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
        <h1 className="text-xl font-semibold mb-6">Create your account</h1>

        <label className="block text-sm text-gray-500 mb-1">Full name</label>
        <input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required
          className="w-full mb-4 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600" />

        <label className="block text-sm text-gray-500 mb-1">Email</label>
        <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} type="email" required
          className="w-full mb-4 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600" />

        <label className="block text-sm text-gray-500 mb-1">Password</label>
        <input value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} type="password" required
          className="w-full mb-4 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600" />

        <label className="block text-sm text-gray-500 mb-1">I am a</label>
        <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}
          className="w-full mb-2 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-eco-600">
          {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>

        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}

        <button disabled={loading} type="submit" className="w-full mt-4 py-2 rounded-full bg-eco-600 text-white font-medium hover:bg-eco-900 transition-colors disabled:opacity-60">
          {loading ? "Creating account…" : "Create account"}
        </button>

        <p className="text-sm text-gray-400 mt-4 text-center">
          Already have an account? <Link href="/login" className="text-eco-600">Sign in</Link>
        </p>
      </motion.form>
    </main>
  );
}

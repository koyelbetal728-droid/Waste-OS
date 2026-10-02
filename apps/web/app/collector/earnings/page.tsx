import { EmptyState } from "@/components/ui/EmptyState";

export default function EarningsPage() {
  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Earnings</h1>
      <EmptyState
        title="Earnings aren't tracked yet"
        description="No earnings ledger exists in the backend yet — this needs a per-collector payout model before it can show real numbers. See packages/collection."
      />
    </main>
  );
}

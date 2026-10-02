import { EmptyState } from "@/components/ui/EmptyState";

export default function BusinessPickupsPage() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Bulk Pickups</h1>
      <EmptyState title="No pickups scheduled" description="Bulk pickup requests for your business will appear here." />
    </main>
  );
}

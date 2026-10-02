import { EmptyState } from "@/components/ui/EmptyState";

export default function CollectorInventoryPage() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Inventory</h1>
      <EmptyState title="No inventory yet" description="Materials you collect and haven't yet dropped off will appear here." />
    </main>
  );
}

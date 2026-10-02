import { EmptyState } from "@/components/ui/EmptyState";

export default function RoutesPage() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold mb-8">Routes</h1>
      <EmptyState title="Not wired to live data yet" description="This view follows the locked WasteOS layout and will populate once the corresponding backend endpoint/dataset is connected." />
    </main>
  );
}

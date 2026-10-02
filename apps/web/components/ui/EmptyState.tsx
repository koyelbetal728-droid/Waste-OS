export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="text-center py-20 rounded-2xl border border-dashed border-gray-200 bg-white">
      <p className="font-medium mb-1">{title}</p>
      <p className="text-sm text-gray-400 max-w-sm mx-auto">{description}</p>
    </div>
  );
}

export function AdSlot({ label }: { label: string }) {
  return <div className="ad-slot" aria-label={label}>{label}</div>;
}

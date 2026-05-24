import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { platformRegistry } from "@/lib/platforms";

export const metadata: Metadata = {
  title: "Supported Platforms",
  description: "See which username checks are active, API-backed, or still being researched.",
};

export default function PlatformsPage() {
  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 20 }}>
      <Link href="/" style={{ color: "var(--accent)" }}>Back to checker</Link>
      <div>
        <h1 style={{ margin: 0, fontSize: "2.5rem" }}>Platform coverage</h1>
        <p style={{ color: "var(--muted)", maxWidth: 700 }}>
          Username Scan favors reliable checks over brittle scraping. Active checks run through official APIs or stable public endpoints.
        </p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))", gap: 12 }}>
        {platformRegistry.map((platform) => (
          <Link key={platform.slug} className="panel" href={`/platforms/${platform.slug}`} style={{ padding: 16, textDecoration: "none", display: "grid", gap: 10 }}>
            <Image src={platform.icon} alt="" width={30} height={30} />
            <strong>{platform.name}</strong>
            <span style={{ color: platform.active ? "var(--success)" : "var(--muted)" }}>{platform.active ? "Active" : "Research"}</span>
            <span style={{ color: "var(--muted)", fontSize: 14 }}>{platform.validation}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}

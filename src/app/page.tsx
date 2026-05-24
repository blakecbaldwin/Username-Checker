import { Suspense } from "react";
import Image from "next/image";
import Link from "next/link";
import { SearchInterface } from "@/components/search-interface";
import { AdSlot } from "@/components/ad-slot";
import { getActivePlatforms, platformRegistry } from "@/lib/platforms";

export default async function Home({ searchParams }: { searchParams: Promise<{ username?: string }> }) {
  const params = await searchParams;
  const activePlatforms = getActivePlatforms();

  return (
    <main className="page-shell">
      <header className="container" style={{ padding: "28px 0 18px" }}>
        <nav style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 }}>
          <Link href="/" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none" }}>
            <Image src="/img/usernamescan.svg" alt="" width={28} height={28} />
            <strong>Username Scan</strong>
          </Link>
          <div style={{ display: "flex", gap: 16, color: "var(--muted)", fontSize: 14 }}>
            <Link href="/platforms">Platforms</Link>
            <Link href="/contact">Contact</Link>
          </div>
        </nav>
      </header>

      <section className="container" style={{ display: "grid", gap: 18, padding: "10px 0 32px" }}>
        <div style={{ display: "grid", gap: 12 }}>
          <p style={{ color: "var(--accent)", fontWeight: 700, margin: 0 }}>Reliable username availability checks</p>
          <h1 style={{ fontSize: "clamp(2rem, 6vw, 4.5rem)", lineHeight: 1, margin: 0, letterSpacing: 0 }}>
            Find a username that travels well.
          </h1>
          <p style={{ color: "var(--muted)", fontSize: "1.075rem", maxWidth: 680, margin: 0 }}>
            Check active API-backed platforms first, see reliability labels, and avoid false confidence from brittle scraping.
          </p>
        </div>

        <AdSlot label="Ad placement reserved for AdSense" />

        <Suspense>
          <SearchInterface initialUsername={params.username ?? ""} platforms={activePlatforms} />
        </Suspense>

        <section className="panel" style={{ padding: 18 }}>
          <h2 style={{ margin: "0 0 12px", fontSize: "1.1rem" }}>Platform coverage</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 10 }}>
            {platformRegistry.map((platform) => (
              <Link
                key={platform.slug}
                href={`/platforms/${platform.slug}`}
                className="panel"
                style={{ padding: 12, textDecoration: "none", display: "flex", alignItems: "center", gap: 10 }}
              >
                <Image src={platform.icon} alt="" width={22} height={22} />
                <span style={{ flex: 1 }}>{platform.name}</span>
                <span style={{ color: platform.active ? "var(--success)" : "var(--muted)", fontSize: 12 }}>
                  {platform.active ? "Active" : "Research"}
                </span>
              </Link>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

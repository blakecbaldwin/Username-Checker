import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About",
  description: "About Username Scan and its reliability-first username availability checks.",
};

export default function AboutPage() {
  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 18 }}>
      <Link href="/" style={{ color: "var(--accent)" }}>Back to checker</Link>
      <h1>About Username Scan</h1>
      <p>Username Scan helps creators, gamers, founders, and teams check username availability across reliable social and gaming platforms.</p>
      <p>The checker prioritizes official APIs and safer public endpoints. Scraper-heavy checks are disabled until they can be supported without creating misleading results or resource spikes.</p>
    </main>
  );
}

import { Suspense } from "react";
import Link from "next/link";
import { BadgeCheck, CheckCircle2, Code2, Edit3, Globe2, ShieldCheck, Telescope } from "lucide-react";
import { SearchInterface } from "@/components/search-interface";
import { getActivePlatforms, platformRegistry } from "@/lib/platforms";

export default async function Home({ searchParams }: { searchParams: Promise<{ username?: string }> }) {
  const params = await searchParams;
  const activePlatforms = getActivePlatforms();
  const researchCount = platformRegistry.length - activePlatforms.length;

  return (
    <main className="page-shell">
      <div className="cosmic-background" aria-hidden="true" />
      <div className="ambient-glow" aria-hidden="true" />

      <header className="container">
        <nav className="site-nav">
          <div className="nav-links">
            <Link href="/about">About</Link>
          </div>
        </nav>
      </header>

      <div className="container home-stack">
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-logo">
              <BadgeCheck size={54} strokeWidth={1.8} />
            </div>
            <div>
              <h1 className="hero-title">UsernameScan</h1>
              <p className="hero-subtitle">
                Search across <strong>{activePlatforms.length} active reliability-first checks</strong>, with{" "}
                {researchCount} more platforms under review.
              </p>
            </div>
          </div>

          <Suspense>
            <SearchInterface initialUsername={params.username ?? ""} platforms={activePlatforms} />
          </Suspense>

          <div className="how-grid">
            <div className="how-card">
              <div className="how-icon">
                <Edit3 size={22} />
              </div>
              <strong>1. Enter Name</strong>
              <p>Type your desired handle.</p>
            </div>
            <div className="how-card">
              <div className="how-icon" style={{ color: "var(--success)" }}>
                <Telescope size={22} />
              </div>
              <strong>2. Scan Platforms</strong>
              <p>Check reliable APIs first.</p>
            </div>
            <div className="how-card">
              <div className="how-icon" style={{ color: "#c0c1ff" }}>
                <CheckCircle2 size={22} />
              </div>
              <strong>3. Review Results</strong>
              <p>See availability and profile links.</p>
            </div>
          </div>
        </section>

        <section className="platform-strip" aria-label="Platform summary">
          <span className="platform-strip-label">
            Checking active platforms, researching requested additions
          </span>
          <div className="platform-strip-items">
            <span className="platform-strip-item">
              <Globe2 size={22} /> Global
            </span>
            <span className="platform-strip-item">
              <Code2 size={22} /> GitHub
            </span>
            <span className="platform-strip-item">
              <ShieldCheck size={22} /> API-backed
            </span>
          </div>
        </section>

        <footer className="site-footer">
          <div className="site-footer-inner">
            <div>
              <strong style={{ color: "var(--accent)" }}>UsernameScan</strong>
              <p>&copy; 2026 UsernameScan. Built for safer username availability checks.</p>
            </div>
            <div className="footer-links">
              <Link href="/privacy">Privacy Policy</Link>
              <Link href="/terms">Terms of Service</Link>
              <Link href="/contact">Contact</Link>
            </div>
          </div>
        </footer>
      </div>
    </main>
  );
}

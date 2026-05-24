import type { Metadata } from "next";
import Link from "next/link";
import {
  Activity,
  BadgeCheck,
  BarChart3,
  Bolt,
  CheckCircle2,
  DatabaseZap,
  Globe2,
  Network,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { getActivePlatforms, platformRegistry } from "@/lib/platforms";

export const metadata: Metadata = {
  title: "About",
  description: "Learn how UsernameScan checks username availability with reliability-first platform coverage.",
};

export default function AboutPage() {
  const activePlatforms = getActivePlatforms();
  const researchCount = platformRegistry.length - activePlatforms.length;

  return (
    <main className="page-shell about-page">
      <div className="cosmic-background" aria-hidden="true" />
      <div className="ambient-glow" aria-hidden="true" />

      <header className="about-nav-shell">
        <nav className="about-nav">
          <Link href="/" className="about-brand">UsernameScan</Link>
          <div className="about-nav-links">
            <Link href="/">Search</Link>
            <Link href="/platforms">Platforms</Link>
          </div>
        </nav>
      </header>

      <section className="about-hero">
        <div className="hero-logo about-hero-logo">
          <BadgeCheck size={50} strokeWidth={1.8} />
        </div>
        <h1>Finding Your Name Everywhere</h1>
        <p>
          The simplest way to check your username across reliable social, creator, and gaming platforms. Whether you are
          building a brand or looking for a fresh start, UsernameScan helps you see where your handle can travel.
        </p>
      </section>

      <section className="about-grid about-steps" aria-label="How UsernameScan works">
        <article className="glass-panel about-card">
          <div className="about-card-icon">
            <Search size={30} />
          </div>
          <h2>1. Search</h2>
          <p>Enter your desired handle or brand name to start a focused availability check.</p>
        </article>
        <article className="glass-panel about-card">
          <div className="about-card-icon">
            <DatabaseZap size={30} />
          </div>
          <h2>2. Scan</h2>
          <p>
            We query {activePlatforms.length} active reliability-first checks and keep scraper-heavy sources out of the
            default path.
          </p>
        </article>
        <article className="glass-panel about-card">
          <div className="about-card-icon">
            <Globe2 size={30} />
          </div>
          <h2>3. Discover</h2>
          <p>Get a clear breakdown of available, taken, invalid, unknown, or credential-limited results.</p>
        </article>
      </section>

      <section className="about-split">
        <div className="about-copy">
          <span className="about-eyebrow">Reliability before reach</span>
          <h2>Check active platforms safely, then expand with confidence.</h2>
          <p>
            Building a consistent digital identity starts with a handle you can actually claim. UsernameScan prioritizes
            official APIs and stable public endpoints so results are useful instead of noisy.
          </p>
          <ul className="about-feature-list">
            <li>
              <Bolt size={22} />
              <span>Fast checks with conservative timeout and rate-limit behavior</span>
            </li>
            <li>
              <Network size={22} />
              <span>{researchCount} requested platforms are tracked for safer future support</span>
            </li>
            <li>
              <BarChart3 size={22} />
              <span>Every result includes a reliability label and status reason when needed</span>
            </li>
          </ul>
        </div>
        <div className="about-visual" aria-label="UsernameScan reliability dashboard preview">
          <div className="about-visual-glow" />
          <div className="about-terminal glass-panel">
            <div className="about-terminal-top">
              <span />
              <span />
              <span />
            </div>
            <div className="about-terminal-row">
              <ShieldCheck size={18} />
              <strong>official_api</strong>
              <em>preferred</em>
            </div>
            <div className="about-terminal-row">
              <Activity size={18} />
              <strong>public_endpoint</strong>
              <em>monitored</em>
            </div>
            <div className="about-terminal-row muted">
              <Sparkles size={18} />
              <strong>scraper-heavy</strong>
              <em>research</em>
            </div>
          </div>
        </div>
      </section>

      <section className="about-faq">
        <h2>Frequently Asked Questions</h2>
        <div className="about-faq-list">
          <details className="glass-panel about-detail">
            <summary>
              How many platforms do you check?
              <CheckCircle2 size={18} />
            </summary>
            <p>
              UsernameScan currently runs {activePlatforms.length} active checks. Additional requested platforms are
              documented as research until they have a safer lookup path.
            </p>
          </details>
          <details className="glass-panel about-detail">
            <summary>
              Why not scrape every site?
              <CheckCircle2 size={18} />
            </summary>
            <p>
              Scraping can create false results, resource spikes, and upstream blocking. The default checker favors
              APIs and stable endpoints first.
            </p>
          </details>
          <details className="glass-panel about-detail">
            <summary>
              Is it free to use?
              <CheckCircle2 size={18} />
            </summary>
            <p>Yes. The core username availability search is free for individual users.</p>
          </details>
        </div>
      </section>

      <section className="about-cta glass-panel">
        <h2>Ready to find your perfect name?</h2>
        <Link href="/" className="about-cta-button">Start Searching Now</Link>
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
    </main>
  );
}

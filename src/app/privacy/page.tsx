import type { Metadata } from "next";
import Link from "next/link";
import { CheckCircle2, Cookie, Database, ExternalLink, ShieldCheck } from "lucide-react";
import { CosmicBackground } from "@/components/cosmic-background";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Privacy information for UsernameScan.",
};

export default function PrivacyPage() {
  return (
    <main className="page-shell legal-page">
      <CosmicBackground />

      <header className="legal-nav-shell">
        <nav className="legal-nav">
          <Link href="/" className="about-brand">UsernameScan</Link>
          <div className="about-nav-links">
            <Link href="/about">About</Link>
          </div>
        </nav>
      </header>

      <section className="legal-shell">
        <div className="legal-heading">
          <h1>Privacy Policy</h1>
          <p>Last updated: May 24, 2026</p>
          <span />
        </div>

        <div className="legal-grid">
          <article className="glass-panel legal-card legal-card-wide">
            <div className="legal-card-title">
              <ShieldCheck size={28} />
              <h2>Our Commitment</h2>
            </div>
            <p>
              UsernameScan is built as a lightweight username availability utility. We try to collect only what is
              necessary to operate the checker, protect it from abuse, and respond to contact form submissions.
            </p>
          </article>

          <article className="glass-panel legal-card legal-card-large">
            <div className="legal-card-title success">
              <Database size={28} />
              <h2>Data Collection</h2>
            </div>
            <span className="legal-kicker">Minimal collection</span>
            <p>We may process the following information when you use the service:</p>
            <ul className="legal-list">
              <li>
                <CheckCircle2 size={18} />
                <strong>Search queries:</strong>
                <span>Usernames you submit so platform checks can run.</span>
              </li>
              <li>
                <CheckCircle2 size={18} />
                <strong>Technical logs:</strong>
                <span>IP address, request metadata, and rate-limit data used for reliability and abuse prevention.</span>
              </li>
              <li>
                <CheckCircle2 size={18} />
                <strong>Contact details:</strong>
                <span>Name, email, inquiry type, and message content when you submit the contact form.</span>
              </li>
            </ul>
          </article>

          <article className="glass-panel legal-card legal-card-small">
            <div className="legal-card-title secondary">
              <Cookie size={28} />
              <h2>Cookies</h2>
            </div>
            <p>
              The current app does not require user accounts. Essential technical storage may be used by hosting,
              security, analytics, or ad services if those integrations are enabled.
            </p>
            <div className="legal-note">No resale of search data. No profile building from username searches.</div>
          </article>

          <article className="glass-panel legal-card legal-card-wide">
            <div className="legal-card-title">
              <ExternalLink size={28} />
              <h2>Third-Party Platforms</h2>
            </div>
            <p>
              UsernameScan checks public availability signals through third-party platforms, APIs, or stable public
              endpoints. External links and profile pages are controlled by those providers and are subject to their own
              policies.
            </p>
            <div className="legal-platform-grid">
              <span>Social Networks</span>
              <span>Developer Platforms</span>
              <span>Gaming Services</span>
              <span>Creator Platforms</span>
            </div>
            <p className="legal-fineprint">
              Advertising, analytics, Vercel hosting, and email delivery providers may process limited technical data if
              enabled for production.
            </p>
          </article>
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
    </main>
  );
}

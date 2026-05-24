import type { Metadata } from "next";
import Link from "next/link";
import { Ban, Edit3, Gavel, ShieldCheck, TriangleAlert } from "lucide-react";
import { CosmicBackground } from "@/components/cosmic-background";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: "Terms for using UsernameScan.",
};

export default function TermsPage() {
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

      <section className="terms-shell">
        <div className="legal-heading">
          <h1>Terms of Service</h1>
          <p>Last updated: May 24, 2026</p>
          <span />
        </div>

        <div className="terms-stack">
          <section className="glass-panel terms-card">
            <div className="terms-title">
              <div>
                <Gavel size={24} />
              </div>
              <h2>1. Acceptance of Terms</h2>
            </div>
            <div className="terms-copy">
              <p>
                By accessing or using UsernameScan, you agree to these Terms of Service. If you do not agree, do not use
                the service.
              </p>
              <p>
                UsernameScan provides unofficial username availability checks. We may modify, pause, or discontinue
                features at any time to protect reliability, security, or platform compliance.
              </p>
            </div>
          </section>

          <section className="glass-panel terms-card">
            <div className="terms-title success">
              <div>
                <ShieldCheck size={24} />
              </div>
              <h2>2. User Responsibilities</h2>
            </div>
            <div className="terms-copy">
              <p>You agree not to use UsernameScan for unlawful, abusive, high-volume, or misleading activity.</p>
              <ul className="terms-list">
                <li>
                  <Ban size={20} />
                  <span>
                    <strong>No automated abuse:</strong> Do not use bots, spiders, scrapers, or other automated systems
                    to bypass rate limits or overload the service.
                  </span>
                </li>
                <li>
                  <Ban size={20} />
                  <span>
                    <strong>No resale or redistribution:</strong> Do not scrape, resell, or repackage UsernameScan
                    results or internal API responses.
                  </span>
                </li>
                <li>
                  <Ban size={20} />
                  <span>
                    <strong>Respect platforms:</strong> Each third-party platform controls its own username rules,
                    availability, and account data.
                  </span>
                </li>
              </ul>
            </div>
          </section>

          <section className="glass-panel terms-card">
            <div className="terms-title warning">
              <div>
                <TriangleAlert size={24} />
              </div>
              <h2>3. Limitation of Liability</h2>
            </div>
            <div className="terms-mono">
              <p>
                USERNAMESCAN IS PROVIDED &quot;AS IS&quot; AND &quot;AS AVAILABLE&quot; WITHOUT WARRANTIES OF ANY KIND. WE
                DO NOT GUARANTEE THAT RESULTS ARE COMPLETE, CURRENT, ERROR-FREE, OR AVAILABLE AT ALL TIMES.
              </p>
              <p>
                TO THE MAXIMUM EXTENT PERMITTED BY LAW, USERNAMESCAN WILL NOT BE LIABLE FOR INDIRECT, INCIDENTAL,
                SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM YOUR USE OF THE SERVICE.
              </p>
            </div>
          </section>

          <section className="glass-panel terms-card">
            <div className="terms-title">
              <div>
                <Edit3 size={24} />
              </div>
              <h2>4. Changes to Terms</h2>
            </div>
            <p className="terms-copy single">
              We may update these Terms from time to time. The latest version will be posted on this page. Continued use
              of UsernameScan after changes become effective means you accept the revised Terms.
            </p>
          </section>
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

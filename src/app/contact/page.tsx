import type { Metadata } from "next";
import Link from "next/link";
import { CosmicBackground } from "@/components/cosmic-background";
import { ContactForm } from "@/components/contact-form";

export const metadata: Metadata = {
  title: "Contact",
  description: "Report a UsernameScan bug, send feedback, or request a new platform.",
};

export default function ContactPage() {
  return (
    <main className="page-shell contact-page">
      <CosmicBackground />

      <header className="contact-nav-shell">
        <nav className="contact-nav">
          <Link href="/" className="about-brand">UsernameScan</Link>
          <div className="about-nav-links">
            <Link href="/about">About</Link>
          </div>
        </nav>
      </header>

      <section className="contact-main">
        <div className="contact-shell">
          <div className="contact-heading">
            <h1>Contact Support</h1>
            <p>We value your input. Use the form below to report bugs, suggest platforms, or share feedback.</p>
          </div>
          <ContactForm />
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

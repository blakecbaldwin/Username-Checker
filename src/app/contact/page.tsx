import type { Metadata } from "next";
import Link from "next/link";
import { ContactForm } from "@/components/contact-form";

export const metadata: Metadata = {
  title: "Contact",
  description: "Report a Username Scan bug, send feedback, or request a new platform.",
};

export default function ContactPage() {
  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 20 }}>
      <Link href="/" style={{ color: "var(--accent)" }}>Back to checker</Link>
      <div>
        <h1 style={{ margin: 0, fontSize: "2.5rem" }}>Contact Username Scan</h1>
        <p style={{ color: "var(--muted)", maxWidth: 720 }}>
          Report an inaccurate result, suggest a platform, or share feedback about the checker.
        </p>
      </div>
      <ContactForm />
    </main>
  );
}

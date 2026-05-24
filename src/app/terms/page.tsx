import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: "Terms for using Username Scan.",
};

export default function TermsPage() {
  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 18 }}>
      <Link href="/" style={{ color: "var(--accent)" }}>Back to checker</Link>
      <h1>Terms of Service</h1>
      <p>Username Scan is provided as an unofficial tool with no guarantee of accuracy, availability, or platform affiliation.</p>
      <p>Results can change at any time because each platform owns its own username policies and account data.</p>
      <p>Do not use this tool for sensitive, abusive, automated, or high-volume activity.</p>
    </main>
  );
}

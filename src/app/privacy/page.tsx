import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Privacy information for Username Scan.",
};

export default function PrivacyPage() {
  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 18 }}>
      <Link href="/" style={{ color: "var(--accent)" }}>Back to checker</Link>
      <h1>Privacy Policy</h1>
      <p>Username Scan checks usernames in real time and does not create user accounts.</p>
      <p>Searches may be processed by third-party platform APIs to determine availability. Server logs, analytics, ads, and anti-abuse systems may process limited technical data such as IP address, browser, and request metadata.</p>
      <p>AdSense, Google Analytics, Vercel Analytics, and Speed Insights may be added as part of the Vercel launch. Update this page with final production identifiers before launch.</p>
    </main>
  );
}

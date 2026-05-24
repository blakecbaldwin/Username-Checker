import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getPlatform, platformRegistry } from "@/lib/platforms";

type Props = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return platformRegistry.map((platform) => ({ slug: platform.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const platform = getPlatform(slug);
  if (!platform) return {};

  return {
    title: `${platform.name} Username Checker`,
    description: `Check ${platform.name} username availability status, validation rules, and reliability notes.`,
  };
}

export default async function PlatformPage({ params }: Props) {
  const { slug } = await params;
  const platform = getPlatform(slug);
  if (!platform) notFound();

  return (
    <main className="container" style={{ padding: "36px 0", display: "grid", gap: 20 }}>
      <Link href="/platforms" style={{ color: "var(--accent)" }}>Back to platforms</Link>
      <section className="panel" style={{ padding: 24, display: "grid", gap: 14 }}>
        <Image src={platform.icon} alt="" width={42} height={42} />
        <div>
          <h1 style={{ margin: 0, fontSize: "2.5rem" }}>{platform.name} username checker</h1>
          <p style={{ color: "var(--muted)", maxWidth: 760 }}>{platform.description}</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 10 }}>
          <div className="panel" style={{ padding: 14 }}>
            <strong>Status</strong>
            <p style={{ margin: "6px 0 0", color: platform.active ? "var(--success)" : "var(--muted)" }}>
              {platform.active ? "Active check" : "Requested / in research"}
            </p>
          </div>
          <div className="panel" style={{ padding: 14 }}>
            <strong>Reliability</strong>
            <p style={{ margin: "6px 0 0", color: "var(--muted)" }}>{platform.reliability.replace("_", " ")}</p>
          </div>
          <div className="panel" style={{ padding: 14 }}>
            <strong>Validation</strong>
            <p style={{ margin: "6px 0 0", color: "var(--muted)" }}>{platform.validation}</p>
          </div>
        </div>
        <Link href="/" style={{ color: "var(--accent)", fontWeight: 700 }}>Check a username</Link>
      </section>
    </main>
  );
}

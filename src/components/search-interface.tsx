"use client";

import { Search, ShieldCheck } from "lucide-react";
import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import type { CheckResult, PlatformDefinition } from "@/lib/platforms";

type Props = {
  initialUsername: string;
  platforms: PlatformDefinition[];
};

function statusColor(status: CheckResult["status"]) {
  if (status === "available") return "var(--success)";
  if (status === "taken") return "var(--danger)";
  if (status === "invalid" || status === "auth_failed") return "var(--warning)";
  return "var(--muted)";
}

function statusLabel(status: CheckResult["status"]) {
  return status.replace("_", " ");
}

export function SearchInterface({ initialUsername, platforms }: Props) {
  const [username, setUsername] = useState(initialUsername);
  const [results, setResults] = useState<CheckResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const platformMap = useMemo(() => new Map(platforms.map((platform) => [platform.slug, platform])), [platforms]);

  async function runSearch(nextUsername = username) {
    const trimmed = nextUsername.trim();
    if (!trimmed) return;

    setLoading(true);
    setError("");
    try {
      const response = await fetch(`/api/check?username=${encodeURIComponent(trimmed)}`);
      const data = (await response.json()) as { results?: CheckResult[]; error?: string };
      if (!response.ok) {
        throw new Error(data.error || "Search failed");
      }

      setResults(data.results ?? []);
      const url = new URL(window.location.href);
      url.searchParams.set("username", trimmed);
      window.history.replaceState(null, "", url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (initialUsername) {
      const timeout = window.setTimeout(() => {
        void runSearch(initialUsername);
      }, 0);
      return () => window.clearTimeout(timeout);
    }
    // Run only for the initial query URL.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <section className="panel" style={{ padding: 18, display: "grid", gap: 18 }}>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void runSearch();
        }}
        style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 10 }}
      >
        <input
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          maxLength={50}
          placeholder="Enter a username..."
          aria-label="Username"
          style={{
            minWidth: 0,
            border: "1px solid var(--border)",
            borderRadius: 8,
            padding: "13px 14px",
            background: "var(--panel-strong)",
            color: "var(--foreground)",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            border: 0,
            borderRadius: 8,
            padding: "0 16px",
            background: "var(--accent)",
            color: "white",
            cursor: "pointer",
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            minHeight: 48,
          }}
        >
          <Search size={18} />
          {loading ? "Checking" : "Check"}
        </button>
      </form>

      <div style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--muted)", fontSize: 14 }}>
        <ShieldCheck size={16} />
        <span>{platforms.length} active reliability-first checks. Scraper-heavy platforms are held for research.</span>
      </div>

      {error ? <div style={{ color: "var(--danger)" }}>{error}</div> : null}

      {results.length ? (
        <div style={{ display: "grid", gap: 10 }}>
          {results.map((item) => {
            const platform = platformMap.get(item.platform);
            return (
              <article
                key={item.platform}
                className="panel"
                style={{ padding: 14, display: "grid", gridTemplateColumns: "auto 1fr auto", alignItems: "center", gap: 12 }}
              >
                {platform ? <Image src={platform.icon} alt="" width={28} height={28} /> : null}
                <div style={{ display: "grid", gap: 2 }}>
                  <strong>{platform?.name ?? item.platform}</strong>
                  <span style={{ color: "var(--muted)", fontSize: 13 }}>{item.reason || item.reliability.replace("_", " ")}</span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  {item.profileUrl ? (
                    <a href={item.profileUrl} target="_blank" rel="noreferrer" style={{ color: "var(--accent)" }}>
                      View
                    </a>
                  ) : null}
                  <strong style={{ color: statusColor(item.status), textTransform: "capitalize" }}>{statusLabel(item.status)}</strong>
                </div>
              </article>
            );
          })}
        </div>
      ) : null}
    </section>
  );
}

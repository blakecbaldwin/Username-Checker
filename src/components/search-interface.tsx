"use client";

import { AtSign, LoaderCircle, Search, ShieldCheck } from "lucide-react";
import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import type { CheckResult, PlatformDefinition } from "@/lib/platforms";

type Props = {
  initialUsername: string;
  platforms: PlatformDefinition[];
};

function statusColor(status: CheckResult["status"]) {
  if (status === "available") return "available";
  if (status === "taken") return "taken";
  return "other";
}

function statusLabel(status: CheckResult["status"]) {
  return status.replace("_", " ");
}

function resultDetail(item: CheckResult) {
  if (item.reason) return item.reason;
  if (item.status === "available") return "No matching profile found from the active check.";
  if (item.status === "taken") return "Matching profile found.";
  return item.reliability.replace("_", " ");
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
    <section className="search-panel">
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void runSearch();
        }}
        className="glass-panel search-form"
      >
        <div className="search-input-icon">
          <AtSign size={24} />
        </div>
        <input
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          maxLength={50}
          placeholder="Enter a username..."
          aria-label="Username"
          spellCheck={false}
          className="search-input"
        />
        <button
          type="submit"
          disabled={loading}
          className="scan-button scan-gradient"
        >
          <span>{loading ? "Scanning" : "Scan"}</span>
          {loading ? <LoaderCircle className="spin" size={18} /> : <Search size={18} />}
        </button>
      </form>

      <div className="search-note">
        <ShieldCheck size={16} />
        <span>Clear availability checks with reliability labels.</span>
      </div>

      {error ? <div className="search-error">{error}</div> : null}

      {results.length ? (
        <div className="results-grid">
          {results.map((item, index) => {
            const platform = platformMap.get(item.platform);
            const statusClass = statusColor(item.status);
            return (
              <article
                key={item.platform}
                className={`glass-panel result-card ${statusClass}`}
                style={{ animationDelay: `${index * 70}ms` }}
              >
                <div className="result-card-header">
                  <div className="result-platform">
                    {platform ? <Image src={platform.icon} alt="" width={24} height={24} /> : null}
                    <span>{platform?.name ?? item.platform}</span>
                  </div>
                  <span className={`result-badge ${statusClass}`}>{statusLabel(item.status)}</span>
                </div>
                <div className="result-detail">{resultDetail(item)}</div>
                {item.profileUrl ? (
                  <a href={item.profileUrl} target="_blank" rel="noreferrer" className="result-action view">
                    View Profile
                  </a>
                ) : item.status === "available" ? (
                  <span className="result-action">Available</span>
                ) : (
                  <span className="result-action view">No Link</span>
                )}
              </article>
            );
          })}
        </div>
      ) : null}
    </section>
  );
}

import type { CheckResult } from "@/lib/platforms";

type CacheEntry = {
  expiresAt: number;
  result: CheckResult;
};

const CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const CACHE_MAX_ENTRIES = 1000;
const cache = new Map<string, CacheEntry>();

const CACHEABLE_STATUSES: ReadonlySet<CheckResult["status"]> = new Set(["available", "taken"]);

// Only definitive availability answers may be cached. Transient outcomes such
// as "unknown" (timeouts, upstream errors) or "auth_failed" (missing or
// rejected credentials) must be re-checked on the next request instead of
// sticking for the whole cache TTL.
export function isCacheableResult(resultToCheck: CheckResult) {
  return CACHEABLE_STATUSES.has(resultToCheck.status);
}

export function getCachedResult(key: string) {
  const cached = cache.get(key);
  if (!cached) {
    return null;
  }

  if (cached.expiresAt <= Date.now()) {
    cache.delete(key);
    return null;
  }

  cache.delete(key);
  cache.set(key, cached);
  return cached.result;
}

export function setCachedResult(key: string, result: CheckResult) {
  cache.set(key, { expiresAt: Date.now() + CACHE_TTL_MS, result });

  while (cache.size > CACHE_MAX_ENTRIES) {
    const oldest = cache.keys().next().value;
    if (!oldest) {
      break;
    }
    cache.delete(oldest);
  }
}

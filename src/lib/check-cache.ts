import type { CheckResult } from "@/lib/platforms";

type CacheEntry = {
  expiresAt: number;
  result: CheckResult;
};

const CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const CACHE_MAX_ENTRIES = 1000;
const cache = new Map<string, CacheEntry>();

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

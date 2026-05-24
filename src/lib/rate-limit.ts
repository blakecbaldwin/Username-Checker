type RateRecord = {
  count: number;
  resetAt: number;
};

const buckets = new Map<string, RateRecord>();

export function rateLimit(key: string, limit: number, windowMs: number) {
  const now = Date.now();
  const record = buckets.get(key);

  if (!record || record.resetAt <= now) {
    buckets.set(key, { count: 1, resetAt: now + windowMs });
    return { limited: false, remaining: limit - 1, resetAt: now + windowMs };
  }

  if (record.count >= limit) {
    return { limited: true, remaining: 0, resetAt: record.resetAt };
  }

  record.count += 1;
  return { limited: false, remaining: limit - record.count, resetAt: record.resetAt };
}

import assert from "node:assert/strict";
import test from "node:test";
import { validators } from "../src/lib/checkers";
import { isCacheableResult } from "../src/lib/check-cache";
import { getActivePlatforms, getPlatform, platformRegistry, type CheckResult } from "../src/lib/platforms";
import { rateLimit } from "../src/lib/rate-limit";

test("platform registry keeps reliability-first active set", () => {
  const active = getActivePlatforms().map((platform) => platform.slug).sort();
  assert.deepEqual(active, [
    "bluesky",
    "github",
    "kick",
    "minecraft",
    "reddit",
    "roblox",
    "soundcloud",
    "steam",
    "tumblr",
    "twitch",
    "youtube",
  ]);
  assert.equal(getPlatform("instagram")?.active, false);
  assert.equal(getPlatform("tiktok")?.active, false);
  assert.equal(getPlatform("github")?.reliability, "official_api");
  assert.equal(getPlatform("kick")?.reliability, "public_endpoint");
});

test("every active platform has a validator", () => {
  for (const platform of getActivePlatforms()) {
    assert.equal(typeof validators[platform.slug], "function", `missing validator for ${platform.slug}`);
  }
});

test("new platform validators accept and reject the right shapes", () => {
  assert.equal(validators.kick("xqc"), true);
  assert.equal(validators.kick("ab"), false);
  assert.equal(validators.kick("has space"), false);
  assert.equal(validators.kick("a".repeat(26)), false);

  assert.equal(validators.youtube("google"), true);
  assert.equal(validators.youtube("mr.beast-1_2"), true);
  assert.equal(validators.youtube("ab"), false);
  assert.equal(validators.youtube("-leadingdash"), false);
  assert.equal(validators.youtube("trailing."), false);
  assert.equal(validators.youtube("a".repeat(31)), false);

  assert.equal(validators.soundcloud("soundcloud"), true);
  assert.equal(validators.soundcloud("ab"), false);
  assert.equal(validators.soundcloud("has space"), false);
  assert.equal(validators.soundcloud("a".repeat(26)), false);
});

test("only definitive results are cacheable", () => {
  const base: CheckResult = {
    platform: "github",
    status: "available",
    reliability: "official_api",
    checkedAt: new Date().toISOString(),
  };
  assert.equal(isCacheableResult(base), true);
  assert.equal(isCacheableResult({ ...base, status: "taken" }), true);
  assert.equal(isCacheableResult({ ...base, status: "unknown" }), false);
  assert.equal(isCacheableResult({ ...base, status: "auth_failed" }), false);
  assert.equal(isCacheableResult({ ...base, status: "invalid" }), false);
  assert.equal(isCacheableResult({ ...base, status: "disabled" }), false);
});

test("every platform has a public icon path and description", () => {
  for (const platform of platformRegistry) {
    assert.match(platform.icon, /^\/img\/.+\.svg$/);
    assert.ok(platform.description.length > 20);
    assert.ok(platform.validation.length > 10);
  }
});

test("rate limiter blocks after configured limit", () => {
  const key = `test:${Date.now()}:${Math.random()}`;
  assert.equal(rateLimit(key, 2, 60_000).limited, false);
  assert.equal(rateLimit(key, 2, 60_000).limited, false);
  assert.equal(rateLimit(key, 2, 60_000).limited, true);
});

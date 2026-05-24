import assert from "node:assert/strict";
import test from "node:test";
import { getActivePlatforms, getPlatform, platformRegistry } from "../src/lib/platforms";
import { rateLimit } from "../src/lib/rate-limit";

test("platform registry keeps reliability-first active set", () => {
  const active = getActivePlatforms().map((platform) => platform.slug).sort();
  assert.deepEqual(active, ["bluesky", "github", "minecraft", "reddit", "roblox", "steam", "tumblr", "twitch"]);
  assert.equal(getPlatform("instagram")?.active, false);
  assert.equal(getPlatform("github")?.reliability, "official_api");
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

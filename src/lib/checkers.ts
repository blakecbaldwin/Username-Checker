import { getActivePlatforms, type CheckResult, type PlatformDefinition, type PlatformStatus } from "@/lib/platforms";
import { getCachedResult, setCachedResult } from "@/lib/check-cache";

const REQUEST_TIMEOUT_MS = 4000;
const MAX_CONCURRENT_CHECKS = 4;

type Checker = (username: string, platform: PlatformDefinition) => Promise<CheckResult>;

function now() {
  return new Date().toISOString();
}

function result(platform: PlatformDefinition, status: PlatformStatus, reason?: string, profileUrl?: string): CheckResult {
  return {
    platform: platform.slug,
    status,
    reason,
    profileUrl,
    reliability: platform.reliability,
    checkedAt: now(),
  };
}

function withTimeout(url: string, init?: RequestInit) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  return fetch(url, {
    ...init,
    signal: controller.signal,
    headers: {
      "User-Agent": "username-scan/2.0",
      ...init?.headers,
    },
  }).finally(() => clearTimeout(timeout));
}

function isMissingEnv(names: string[] | undefined) {
  return Boolean(names?.some((name) => !process.env[name]));
}

function validateGitHub(username: string) {
  return /^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$/.test(username);
}

function validateMinecraft(username: string) {
  return /^[a-zA-Z0-9_]{3,16}$/.test(username);
}

function validateReddit(username: string) {
  return /^[A-Za-z0-9_-]{3,20}$/.test(username);
}

function validateRoblox(username: string) {
  return /^[a-zA-Z0-9_]{3,20}$/.test(username);
}

function validateSteam(username: string) {
  return username.length >= 2 && username.length <= 32;
}

function validateTwitch(username: string) {
  return /^[a-zA-Z0-9_]{4,25}$/.test(username);
}

function validateBluesky(username: string) {
  return /^[a-zA-Z0-9](?:[a-zA-Z0-9-]{1,61}[a-zA-Z0-9])?$/.test(username);
}

function validateTumblr(username: string) {
  return /^[a-zA-Z0-9](?:[a-zA-Z0-9-]{1,30}[a-zA-Z0-9])?$/.test(username);
}

const validators: Record<string, (username: string) => boolean> = {
  github: validateGitHub,
  minecraft: validateMinecraft,
  reddit: validateReddit,
  roblox: validateRoblox,
  steam: validateSteam,
  twitch: validateTwitch,
  bluesky: validateBluesky,
  tumblr: validateTumblr,
};

const tokenCache = new Map<string, { token: string; expiresAt: number }>();

async function getRedditToken() {
  const cached = tokenCache.get("reddit");
  if (cached && cached.expiresAt > Date.now()) {
    return cached.token;
  }

  const clientId = process.env.REDDIT_CLIENT_ID;
  const clientSecret = process.env.REDDIT_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    return null;
  }

  const credentials = Buffer.from(`${clientId}:${clientSecret}`).toString("base64");
  const response = await withTimeout("https://www.reddit.com/api/v1/access_token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${credentials}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });

  if (!response.ok) {
    return null;
  }

  const data = (await response.json()) as { access_token?: string; expires_in?: number };
  if (!data.access_token) {
    return null;
  }

  tokenCache.set("reddit", {
    token: data.access_token,
    expiresAt: Date.now() + Math.max((data.expires_in ?? 3600) - 60, 60) * 1000,
  });
  return data.access_token;
}

async function getTwitchToken() {
  const cached = tokenCache.get("twitch");
  if (cached && cached.expiresAt > Date.now()) {
    return cached.token;
  }

  const clientId = process.env.TWITCH_CLIENT_ID;
  const clientSecret = process.env.TWITCH_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    return null;
  }

  const params = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    grant_type: "client_credentials",
  });
  const response = await withTimeout(`https://id.twitch.tv/oauth2/token?${params.toString()}`, { method: "POST" });

  if (!response.ok) {
    return null;
  }

  const data = (await response.json()) as { access_token?: string; expires_in?: number };
  if (!data.access_token) {
    return null;
  }

  tokenCache.set("twitch", {
    token: data.access_token,
    expiresAt: Date.now() + Math.max((data.expires_in ?? 3600) - 60, 60) * 1000,
  });
  return data.access_token;
}

const checkers: Record<string, Checker> = {
  async github(username, platform) {
    const headers: Record<string, string> = {};
    if (process.env.GITHUB_TOKEN) {
      headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
    }

    const response = await withTimeout(`https://api.github.com/users/${username}`, { headers });
    if (response.status === 200) return result(platform, "taken", undefined, `https://github.com/${username}`);
    if (response.status === 404) return result(platform, "available");
    return result(platform, "unknown", `GitHub returned ${response.status}`);
  },

  async minecraft(username, platform) {
    const response = await withTimeout(`https://api.mojang.com/users/profiles/minecraft/${username}`);
    if (response.status === 200) return result(platform, "taken", undefined, `https://namemc.com/profile/${username}`);
    if (response.status === 404 || response.status === 204) return result(platform, "available");
    return result(platform, "unknown", `Mojang returned ${response.status}`);
  },

  async reddit(username, platform) {
    const token = await getRedditToken();
    if (!token) return result(platform, "auth_failed", "Missing or invalid Reddit credentials");

    const response = await withTimeout(`https://oauth.reddit.com/user/${username}/about`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 200) return result(platform, "taken", undefined, `https://www.reddit.com/user/${username}/`);
    if (response.status === 404) return result(platform, "available");
    return result(platform, "unknown", `Reddit returned ${response.status}`);
  },

  async roblox(username, platform) {
    const response = await withTimeout("https://users.roblox.com/v1/usernames/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usernames: [username], excludeBannedUsers: false }),
    });
    if (!response.ok) return result(platform, "unknown", `Roblox returned ${response.status}`);

    const data = (await response.json()) as { data?: unknown[] };
    if (data.data?.length) return result(platform, "taken", undefined, `https://www.roblox.com/users/profile?username=${username}`);
    return result(platform, "available");
  },

  async steam(username, platform) {
    const key = process.env.STEAM_API_KEY;
    if (!key) return result(platform, "auth_failed", "Missing Steam API key");

    const params = new URLSearchParams({ key, vanityurl: username });
    const response = await withTimeout(`https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?${params.toString()}`);
    if (!response.ok) return result(platform, "unknown", `Steam returned ${response.status}`);

    const data = (await response.json()) as { response?: { success?: number } };
    if (data.response?.success === 1) return result(platform, "taken", undefined, `https://steamcommunity.com/id/${username}`);
    return result(platform, "available");
  },

  async twitch(username, platform) {
    const token = await getTwitchToken();
    const clientId = process.env.TWITCH_CLIENT_ID;
    if (!token || !clientId) return result(platform, "auth_failed", "Missing or invalid Twitch credentials");

    const params = new URLSearchParams({ login: username });
    const response = await withTimeout(`https://api.twitch.tv/helix/users?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Client-ID": clientId,
      },
    });
    if (!response.ok) return result(platform, "unknown", `Twitch returned ${response.status}`);

    const data = (await response.json()) as { data?: unknown[] };
    if (data.data?.length) return result(platform, "taken", undefined, `https://www.twitch.tv/${username}`);
    return result(platform, "available");
  },

  async bluesky(username, platform) {
    const handle = `${username}.bsky.social`;
    const params = new URLSearchParams({ handle });
    const response = await withTimeout(`https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?${params.toString()}`);
    if (response.status === 200) return result(platform, "taken", undefined, `https://bsky.app/profile/${handle}`);
    if (response.status === 400 || response.status === 404) return result(platform, "available");
    return result(platform, "unknown", `Bluesky returned ${response.status}`);
  },

  async tumblr(username, platform) {
    const key = process.env.TUMBLR_CONSUMER_KEY;
    if (!key) return result(platform, "auth_failed", "Missing Tumblr consumer key");

    const params = new URLSearchParams({ api_key: key });
    const response = await withTimeout(`https://api.tumblr.com/v2/blog/${username}.tumblr.com/info?${params.toString()}`);
    if (response.status === 200) return result(platform, "taken", undefined, `https://${username}.tumblr.com/`);
    if (response.status === 404) return result(platform, "available");
    return result(platform, "unknown", `Tumblr returned ${response.status}`);
  },
};

export async function checkUsername(username: string) {
  const normalizedUsername = username.trim().toLowerCase();
  const platforms = getActivePlatforms();

  async function run(platform: PlatformDefinition) {
    const validate = validators[platform.slug];
    if (!validate?.(normalizedUsername)) {
      return result(platform, "invalid", platform.validation);
    }

    if (isMissingEnv(platform.env) && platform.env?.some((name) => name !== "GITHUB_TOKEN")) {
      return result(platform, "auth_failed", `Missing required environment: ${platform.env.join(", ")}`);
    }

    const cacheKey = `${platform.slug}:${normalizedUsername}`;
    const cached = getCachedResult(cacheKey);
    if (cached) {
      return cached;
    }

    try {
      const checker = checkers[platform.slug];
      const checked = checker ? await checker(normalizedUsername, platform) : result(platform, "disabled");
      setCachedResult(cacheKey, checked);
      return checked;
    } catch (error) {
      const reason = error instanceof Error && error.name === "AbortError" ? "Request timed out" : "Request failed";
      return result(platform, "unknown", reason);
    }
  }

  const results: CheckResult[] = [];
  for (let index = 0; index < platforms.length; index += MAX_CONCURRENT_CHECKS) {
    const chunk = platforms.slice(index, index + MAX_CONCURRENT_CHECKS);
    results.push(...(await Promise.all(chunk.map(run))));
  }

  return results;
}

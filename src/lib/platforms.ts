export type PlatformStatus = "available" | "taken" | "invalid" | "unknown" | "auth_failed" | "disabled";

export type PlatformReliability = "official_api" | "public_endpoint" | "disabled";

export type CheckResult = {
  platform: string;
  status: PlatformStatus;
  profileUrl?: string;
  reason?: string;
  reliability: PlatformReliability;
  checkedAt: string;
};

export type PlatformDefinition = {
  slug: string;
  name: string;
  icon: string;
  active: boolean;
  reliability: PlatformReliability;
  validation: string;
  env?: string[];
  description: string;
};

export const ACTIVE_PLATFORM_SLUGS = [
  "github",
  "minecraft",
  "reddit",
  "roblox",
  "steam",
  "twitch",
  "bluesky",
  "tumblr",
] as const;

export const platformRegistry: PlatformDefinition[] = [
  {
    slug: "github",
    name: "GitHub",
    icon: "/img/github.svg",
    active: true,
    reliability: "official_api",
    validation: "1-39 characters. Letters, numbers, and internal hyphens.",
    env: ["GITHUB_TOKEN"],
    description: "Checks the GitHub users API. A token is optional but helps avoid anonymous rate limits.",
  },
  {
    slug: "minecraft",
    name: "Minecraft",
    icon: "/img/minecraft.svg",
    active: true,
    reliability: "official_api",
    validation: "3-16 characters. Letters, numbers, and underscores.",
    description: "Checks the Mojang profile endpoint for existing Minecraft usernames.",
  },
  {
    slug: "reddit",
    name: "Reddit",
    icon: "/img/reddit.svg",
    active: true,
    reliability: "official_api",
    validation: "3-20 characters. Letters, numbers, hyphens, and underscores.",
    env: ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
    description: "Uses Reddit OAuth client credentials and the user about endpoint.",
  },
  {
    slug: "roblox",
    name: "Roblox",
    icon: "/img/roblox.svg",
    active: true,
    reliability: "public_endpoint",
    validation: "3-20 characters. Letters, numbers, and underscores.",
    description: "Uses Roblox's username lookup endpoint.",
  },
  {
    slug: "steam",
    name: "Steam",
    icon: "/img/steam.svg",
    active: true,
    reliability: "official_api",
    validation: "2-32 characters.",
    env: ["STEAM_API_KEY"],
    description: "Checks Steam vanity URLs through the Steam Web API.",
  },
  {
    slug: "twitch",
    name: "Twitch",
    icon: "/img/twitch.svg",
    active: true,
    reliability: "official_api",
    validation: "4-25 characters. Letters, numbers, and underscores.",
    env: ["TWITCH_CLIENT_ID", "TWITCH_CLIENT_SECRET"],
    description: "Uses Twitch OAuth client credentials and the Helix users endpoint.",
  },
  {
    slug: "bluesky",
    name: "Bluesky",
    icon: "/img/bluesky.svg",
    active: true,
    reliability: "official_api",
    validation: "3-63 characters for the bsky.social handle prefix. Letters, numbers, and hyphens.",
    description: "Resolves the username as a bsky.social handle through the public AT Protocol identity endpoint.",
  },
  {
    slug: "tumblr",
    name: "Tumblr",
    icon: "/img/tumblr.svg",
    active: true,
    reliability: "official_api",
    validation: "3-32 characters. Letters, numbers, and hyphens.",
    env: ["TUMBLR_CONSUMER_KEY"],
    description: "Checks Tumblr blog info through Tumblr's API when a consumer key is configured.",
  },
  {
    slug: "kick",
    name: "Kick",
    icon: "/img/kick.svg",
    active: false,
    reliability: "disabled",
    validation: "Requested platform. Validation and official lookup path still need confirmation.",
    description: "Held as requested/in research until a reliable lookup path is confirmed.",
  },
  {
    slug: "xbox",
    name: "Xbox",
    icon: "/img/xbox.svg",
    active: false,
    reliability: "disabled",
    validation: "Requested platform. Official availability lookup still needs confirmation.",
    description: "Held as requested/in research because consumer-grade Xbox lookup APIs are not established here yet.",
  },
  {
    slug: "playstation",
    name: "PlayStation",
    icon: "/img/playstation.svg",
    active: false,
    reliability: "disabled",
    validation: "Requested platform. Official availability lookup still needs confirmation.",
    description: "Held as requested/in research until a reliable official lookup route is confirmed.",
  },
  {
    slug: "facebook",
    name: "Facebook",
    icon: "/img/facebook.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "instagram",
    name: "Instagram",
    icon: "/img/instagram.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "pinterest",
    name: "Pinterest",
    icon: "/img/pinterest.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "snapchat",
    name: "Snapchat",
    icon: "/img/snapchat.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "soundcloud",
    name: "SoundCloud",
    icon: "/img/soundcloud.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "tiktok",
    name: "TikTok",
    icon: "/img/tiktok.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
  {
    slug: "youtube",
    name: "YouTube",
    icon: "/img/youtube.svg",
    active: false,
    reliability: "disabled",
    validation: "Disabled because the old checker depended on page scraping.",
    description: "Disabled from the default checker because scraping was resource-heavy and unreliable.",
  },
];

export function getActivePlatforms() {
  return platformRegistry.filter((platform) => platform.active);
}

export function getPlatform(slug: string) {
  return platformRegistry.find((platform) => platform.slug === slug);
}

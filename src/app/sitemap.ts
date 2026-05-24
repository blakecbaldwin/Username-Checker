import type { MetadataRoute } from "next";
import { platformRegistry } from "@/lib/platforms";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://usernamescan.com";
  return [
    { url: baseUrl },
    { url: `${baseUrl}/contact` },
    { url: `${baseUrl}/platforms` },
    ...platformRegistry.map((platform) => ({ url: `${baseUrl}/platforms/${platform.slug}` })),
  ];
}

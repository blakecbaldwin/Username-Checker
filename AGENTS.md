# Username Scan Agent Guide

This repository is a Flask app for checking username availability across a controlled set of platforms. This guide is the working map for future agents and includes the security remediation tracker for the current hardening effort.

## Current Repository State

- Local branch: `main`.
- Remote: `origin` points to `https://github.com/blakecbaldwin/Username-Checker`.
- After fetching on 2026-05-23, local `main` was behind `origin/main` by one README-only commit: `9266c09 Add online view link to README`.
- Always run `git status --short --branch` before edits. This repo has had local uncommitted work.

## Product Summary

The app is branded as **Username Scan**. The home page accepts one username, checks active platforms, and renders statuses:

- `Available`
- `Taken`
- `Invalid`
- `Unknown/Error`
- `Auth Failed`

The contact form remains available for bug reports, but it is protected with CSRF, reCAPTCHA, server-side length limits, and conservative rate limits.

## Stack

- Python Flask app in `app.py`.
- Jinja templates in `templates/`.
- Platform checker modules in `platforms/`.
- Static SVG platform icons in `static/img/`.
- Rate limiting via `Flask-Limiter`.
- CSRF protection via `Flask-WTF`.
- HTTP calls via `requests`.
- Environment variables via `python-dotenv`.

## Security Remediation Tracker

- [x] Removed birthday/anniversary/celebrations feature, including `/banner`, `/celebrations-data`, `templates/birthday-anniversary-banner.html`, and `static/celebrations.json`.
- [x] Added conservative inbound rate limits with in-memory storage.
- [x] Disabled scraper-heavy platform checks from the active public search path.
- [x] Kept only API-backed active platforms: GitHub, Minecraft/Mojang, Reddit, Roblox, Steam, Twitch.
- [x] Lowered username check concurrency to 4 workers.
- [x] Added a 6-hour in-memory username result cache with a 1000-entry cap.
- [x] Added outbound request timeouts for all platform modules.
- [x] Changed upstream `403` and `429` handling to `Unknown`, not `Available`.
- [x] Added fail-closed handling for missing API credentials.
- [x] Added CSRF protection and hidden CSRF fields for POST forms.
- [x] Added request and field length limits.
- [x] Required `SECRET_KEY` outside debug mode.
- [x] Added basic security headers and CSP.
- [x] Hardened contact form reCAPTCHA and SMTP failure handling.
- [x] Normalized pinned dependencies and added security packages.
- [x] Added unittest coverage for key security behavior.

## Saved Plans

### Security Audit And Remediation Plan

Status: implemented in the current working tree, pending commit.

Original goals:

- Harden the Flask app against abuse-driven restarts.
- Remove the internship celebration/banner feature completely.
- Add conservative rate limiting and safer outbound request behavior.
- Disable scraper-heavy checks from the active public search path.
- Add CSRF protection, request size limits, safer app config, and security headers.
- Keep the contact form but harden reCAPTCHA and SMTP failure handling.
- Normalize dependencies and add tests.
- Record remediation progress in this guide.

Implementation decisions:

- Use `Flask-Limiter` with `memory://` storage for now.
- Use `Flask-WTF` / `CSRFProtect` for forms.
- Keep API-backed active platforms only: GitHub, Minecraft/Mojang, Reddit, Roblox, Steam, Twitch.
- Keep disabled checker files for future review, but do not show disabled platforms in active results.
- Use a 6-hour in-memory username cache with a 1000-entry cap.
- Use max 4 active checker workers.
- Treat upstream `403` and `429` as unknown/error states, never available.
- Require `SECRET_KEY` outside debug mode.

### Vercel Rebuild And Growth Plan

Status: planned, not implemented.

Summary:

Rebuild Username Scan as a Vercel-native Next.js app, replacing Flask after feature parity. The new version should keep the hardened security posture, redesign the checker as a polished utility dashboard, add clean AdSense monetization, improve SEO with platform pages, and expand platform support reliability-first.

Locked decisions from planning:

- Migration strategy: Next.js rebuild, replacing Flask.
- Platform expansion style: reliability first.
- First new platform batch: existing icon backlog.
- Ads strategy: clean AdSense.
- Storage/rate-limit budget: free/low-cost first; use Vercel-native defenses and in-memory/function cache initially, with Upstash Redis as a later upgrade if traffic requires it.
- Visual direction: utility dashboard.
- Contact support: keep a simple form.
- Analytics/monitoring: use both Vercel Analytics/Speed Insights and Google tools.
- Result model: share by query URL, such as `/?username=example`; no persisted result snapshots in v1.
- SEO content: platform pages.
- User platform requests: add a platform request option to the contact form.

Planned implementation:

- Scaffold a Next.js App Router app with TypeScript, Tailwind, shadcn/ui, and Geist.
- Replace Flask/Jinja with a tool-first homepage: username input, platform filters, reliability labels, fast result cards, reserved ad slots, and mobile-first layout.
- Add `/api/check?username=...` returning:

```ts
type CheckResult = {
  platform: string
  status: "available" | "taken" | "invalid" | "unknown" | "auth_failed" | "disabled"
  profileUrl?: string
  reason?: string
  reliability: "official_api" | "public_endpoint" | "disabled"
  checkedAt: string
}
```

- Port active checks from Python to TypeScript.
- Keep v1 active platforms as GitHub, Minecraft, Reddit, Roblox, Steam, Twitch, Bluesky, and Tumblr when reliable implementations are confirmed.
- Keep Kick, Xbox, PlayStation, and scraper-heavy platforms visible as requested/in-research platform pages, not active checks until a reliable source exists.
- Add a platform registry that owns display name, icon, validation, reliability tier, active/disabled state, and checker function.
- Add `/platforms/[slug]` pages for active and requested platforms with useful validation rules, known limitations, and a checker entry point.
- Add clean AdSense support: `NEXT_PUBLIC_ADSENSE_CLIENT`, `ads.txt`, one top reserved slot, one results/sidebar slot, Auto Ads script, and privacy-policy updates.
- Add Vercel Web Analytics and Speed Insights plus Google Search Console/Analytics-ready metadata.
- Keep contact support with reCAPTCHA, existing SMTP-compatible env vars or a Vercel-friendly email provider, and a platform request option.
- Update this guide with the final Next.js architecture, platform policy, env vars, ad setup, and Vercel deployment notes.

Planned test coverage:

- Unit test validators and checker status mapping with all outbound network calls mocked.
- API tests for `/api/check`: invalid username, rate limit behavior, timeout behavior, disabled platforms, missing credentials, and cache hits.
- Page tests for homepage, contact page, platform pages, sitemap, robots, metadata, and ad placeholder rendering.
- Run Next.js build, lint, typecheck, and browser verification at desktop/mobile sizes.
- Verify no live API calls happen in tests and no scraper-heavy platforms are active by default.

### Suggested Future Updates

- Reliability labels per platform so users understand why some results are stronger than others.
- User-selectable platform groups so normal searches remain cheap and fast.
- Platform-specific SEO pages for search growth and clearer limitations.
- A lightweight platform request workflow through the contact form.
- Vercel-friendly shared rate limiting/cache storage, likely Upstash Redis, if traffic grows.
- Replace or repair mojibake copy during the redesign.
- Review legal/privacy copy after adding ads, analytics, and platform pages.

## Routes

- `GET /`: Render username search form.
- `POST /`: CSRF-protected username search. Rate limited to `5 per minute` and `30 per day` per IP.
- `GET /about`: About page.
- `GET /privacy`: Privacy policy page.
- `GET /terms`: Terms page.
- `GET /contact`: Contact form.
- `POST /contact`: CSRF-protected contact submission. Rate limited to `3 per hour` and `10 per day` per IP.
- `GET /sitemap.xml`: Serves root `sitemap.xml`.

Removed routes:

- `/banner`
- `/celebrations-data`

Those routes must stay removed unless the owner explicitly asks to reintroduce a non-private, production-safe version.

## Active Platform Policy

Only API-backed or comparatively structured checks are active in the public fan-out path:

| Platform | Check method | Required env |
| --- | --- | --- |
| GitHub | GitHub REST users endpoint | `GITHUB_TOKEN` optional |
| Minecraft | Mojang profile lookup | None |
| Reddit | OAuth client credentials, then user about endpoint | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` |
| Roblox | Username lookup API | None |
| Steam | Steam vanity URL API | `STEAM_API_KEY` |
| Twitch | OAuth client credentials, then Helix users API | `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET` |

Scraper-heavy checks are intentionally disabled from active search:

- Facebook
- Instagram
- Pinterest
- Snapchat
- SoundCloud
- TikTok
- YouTube

The disabled checker files remain in `platforms/` for future review, but `app.py` only imports modules listed in `ACTIVE_PLATFORM_MODULES`.

## Runtime Security Behavior

- Global request rate limit: `60 per minute` per IP.
- Username search rate limit: `5 per minute` and `30 per day` per IP.
- Contact form rate limit: `3 per hour` and `10 per day` per IP.
- Rate limit storage defaults to `memory://`; set `RATELIMIT_STORAGE_URI` for shared storage later.
- Username cache key is normalized platform + lowercased username.
- Cache TTL is 6 hours; max size is 1000 entries.
- Active platform checks run with max 4 worker threads.
- Outbound HTTP timeout is `(2, 4)` unless a future module has a documented reason otherwise.
- `403` and `429` upstream responses must not be shown as available usernames.
- Missing required credentials should return `Auth Failed` or fail closed before making outbound calls.

## Required Environment Variables

Required outside debug mode:

```text
SECRET_KEY
```

Required for specific features:

```text
STEAM_API_KEY
TWITCH_CLIENT_ID
TWITCH_CLIENT_SECRET
REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET
SMTP_SERVER
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
SMTP_FROM_EMAIL
SMTP_TO_EMAIL
RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY
```

Optional:

```text
GITHUB_TOKEN
RATELIMIT_STORAGE_URI
PORT
FLASK_DEBUG
```

Do not commit `.env` or print secret values.

## Local Development

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python app.py
```

Default local URL:

```text
http://localhost:5000
```

Run tests:

```powershell
python -m unittest discover
```

In this Codex desktop environment, the bundled Python may be at `C:\Users\blake\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.

## Agent Working Rules

- Keep celebration/birthday/anniversary code removed.
- Keep scraper-heavy platforms disabled unless the owner explicitly asks for a production-safe rework.
- Keep platform checker return values compatible with `templates/index.html`.
- When changing validation rules, update checker tooltips and tests.
- When adding a platform, add a checker and icon or make missing icons harmless.
- When changing public routes, update `sitemap.xml`, `robots.txt`, tests, and this guide.
- For the Vercel migration, revisit rate-limit/cache storage because in-memory state is only an immediate Render/resource fix.

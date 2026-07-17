# Username Scan

Username Scan checks whether a username appears available across reliable social, creator, and gaming platforms.

Production site: https://usernamescan.com

## Features

- Search one username across multiple platforms.
- Shows clear statuses: `available`, `taken`, `invalid`, `unknown`, `auth_failed`, or `disabled`.
- Uses official APIs or stable public endpoints for active checks.
- Avoids scraper-heavy platforms in the active public checker.
- Includes platform coverage pages for SEO and transparency.
- Includes a contact form for feedback, bug reports, and platform requests.
- Designed for Vercel deployment with Next.js App Router.

## Supported Platforms

Active checks:

- GitHub
- Minecraft
- Reddit
- Roblox
- Steam
- Twitch
- Bluesky
- Tumblr

Requested or disabled checks:

- Kick
- Xbox
- PlayStation
- Facebook
- Instagram
- Pinterest
- Snapchat
- SoundCloud
- TikTok
- YouTube

## Tech Stack

- Next.js `16.2.6`
- React `19.2.6`
- TypeScript
- Tailwind CSS v4
- Nodemailer for the contact form
- Vercel-compatible App Router API routes

## Getting Started

Use Node.js 20 or newer.

Install dependencies:

```powershell
npm.cmd install
```

Create a local environment file:

```powershell
Copy-Item .env.example .env.local
```

Fill in the values in `.env.local`, then start the dev server:

```powershell
npm.cmd run dev
```

Open http://localhost:3000.

## Environment Variables

See `.env.example` for the full list of supported variables.

Required for all active platform checks and contact form delivery:

- `STEAM_API_KEY`
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `TUMBLR_CONSUMER_KEY`
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SMTP_TO_EMAIL`

Optional:

- `GITHUB_TOKEN`
- `NEXT_PUBLIC_ADSENSE_CLIENT`

The app can run locally without every credential, but missing platform credentials return `auth_failed`, and missing SMTP configuration makes the contact API return `503`.

## Scripts

```powershell
npm.cmd run dev
npm.cmd run build
npm.cmd start
npm.cmd run lint
npm.cmd test
```

## Deployment

Deploy as a standard Next.js app on Vercel:

1. Import the repository into Vercel.
2. Set the project root to the directory containing `package.json`.
3. Keep the default Next.js build settings:
   - Install: `npm install`
   - Build: `npm run build`
4. Add the environment variables from `.env.example`.
5. Deploy and smoke test `/`, `/platforms`, `/api/check?username=example`, and `/contact`.

More detailed deployment and operational notes are in `AGENTS.md`.

## Security Note

This project currently has a known HIGH-severity Nodemailer dependency alert involving SSRF or arbitrary file read through Nodemailer's `raw` option. The current contact route is publicly reachable in production, but the code does not currently pass `raw` to Nodemailer. See `AGENTS.md` for the full known-issue note before changing the contact form or email code.

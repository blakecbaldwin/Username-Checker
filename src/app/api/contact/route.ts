import nodemailer from "nodemailer";
import { NextRequest, NextResponse } from "next/server";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

function clientIp(request: NextRequest) {
  return request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
}

function missingSmtpConfig() {
  return [
    "SMTP_SERVER",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_FROM_EMAIL",
    "SMTP_TO_EMAIL",
  ].some((key) => !process.env[key]);
}

export async function POST(request: NextRequest) {
  const limit = rateLimit(`contact:${clientIp(request)}`, 3, 60 * 60 * 1000);
  if (limit.limited) {
    return NextResponse.json({ error: "Too many contact attempts. Please wait before trying again." }, { status: 429 });
  }

  const body = (await request.json()) as {
    name?: string;
    email?: string;
    subject?: string;
    message?: string;
    platformRequest?: string;
  };

  const name = body.name?.trim() ?? "";
  const email = body.email?.trim() ?? "";
  const subject = body.subject?.trim() ?? "";
  const message = body.message?.trim() ?? "";
  const platformRequest = body.platformRequest?.trim() ?? "";

  if (!name || !subject || !message) {
    return NextResponse.json({ error: "Name, subject, and message are required." }, { status: 400 });
  }
  if (name.length > 100 || email.length > 254 || subject.length > 150 || message.length > 4000 || platformRequest.length > 100) {
    return NextResponse.json({ error: "One or more fields is too long." }, { status: 400 });
  }
  if (missingSmtpConfig()) {
    console.warn("Contact form blocked: missing SMTP configuration");
    return NextResponse.json({ error: "Contact form is not configured yet." }, { status: 503 });
  }

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_SERVER,
    port: Number(process.env.SMTP_PORT),
    secure: false,
    auth: {
      user: process.env.SMTP_USERNAME,
      pass: process.env.SMTP_PASSWORD,
    },
  });

  await transporter.sendMail({
    from: process.env.SMTP_FROM_EMAIL,
    to: process.env.SMTP_TO_EMAIL,
    subject: `Username Scan Contact: ${subject}`,
    text: [
      "New Username Scan contact form submission:",
      "",
      `Name: ${name}`,
      `Email: ${email || "Not provided"}`,
      `Platform request: ${platformRequest || "Not provided"}`,
      `Subject: ${subject}`,
      "",
      message,
    ].join("\n"),
  });

  return NextResponse.json({ ok: true });
}

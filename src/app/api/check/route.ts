import { NextRequest, NextResponse } from "next/server";
import { checkUsername } from "@/lib/checkers";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

function clientIp(request: NextRequest) {
  return request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
}

export async function GET(request: NextRequest) {
  const limit = rateLimit(`check:${clientIp(request)}`, 5, 60 * 1000);
  if (limit.limited) {
    return NextResponse.json({ error: "Too many searches. Please wait a bit before trying again." }, { status: 429 });
  }

  const username = request.nextUrl.searchParams.get("username")?.trim() ?? "";
  if (!username) {
    return NextResponse.json({ error: "Username is required." }, { status: 400 });
  }
  if (username.length > 50) {
    return NextResponse.json({ error: "Usernames must be 50 characters or fewer." }, { status: 400 });
  }

  const results = await checkUsername(username);
  return NextResponse.json({ username: username.toLowerCase(), results });
}

"use client";

import { useState } from "react";

export function ContactForm() {
  const [status, setStatus] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setStatus("");

    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") ?? ""),
      email: String(form.get("email") ?? ""),
      platformRequest: String(form.get("platformRequest") ?? ""),
      subject: String(form.get("subject") ?? ""),
      message: String(form.get("message") ?? ""),
    };

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = (await response.json()) as { error?: string };
      if (!response.ok) throw new Error(data.error || "Message failed");
      setStatus("Message sent.");
      event.currentTarget.reset();
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Message failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={submit} className="panel" style={{ padding: 18, display: "grid", gap: 12 }}>
      <input name="name" required maxLength={100} placeholder="Your name" style={fieldStyle} />
      <input name="email" type="email" maxLength={254} placeholder="Email (optional)" style={fieldStyle} />
      <input name="platformRequest" maxLength={100} placeholder="Platform request (optional)" style={fieldStyle} />
      <input name="subject" required maxLength={150} placeholder="Subject" style={fieldStyle} />
      <textarea name="message" required maxLength={4000} rows={7} placeholder="Message" style={fieldStyle} />
      <button
        disabled={submitting}
        style={{
          border: 0,
          borderRadius: 8,
          padding: "12px 16px",
          background: "var(--accent)",
          color: "white",
          cursor: "pointer",
          width: "fit-content",
        }}
      >
        {submitting ? "Sending" : "Send"}
      </button>
      {status ? <p style={{ color: "var(--muted)", margin: 0 }}>{status}</p> : null}
    </form>
  );
}

const fieldStyle: React.CSSProperties = {
  border: "1px solid var(--border)",
  borderRadius: 8,
  padding: "12px 13px",
  background: "var(--panel-strong)",
  color: "var(--foreground)",
};

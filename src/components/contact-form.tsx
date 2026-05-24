"use client";

import { Bolt, ChevronDown, LoaderCircle, Lock, Send } from "lucide-react";
import { useState } from "react";

export function ContactForm() {
  const [status, setStatus] = useState("");
  const [statusTone, setStatusTone] = useState<"muted" | "success" | "error">("muted");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setStatus("");
    setStatusTone("muted");

    const form = new FormData(event.currentTarget);
    const inquiryType = String(form.get("inquiryType") ?? "");
    const payload = {
      name: String(form.get("name") ?? ""),
      email: String(form.get("email") ?? ""),
      platformRequest: inquiryType === "Platform Request" ? "Requested from contact form" : "",
      subject: inquiryType,
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
      setStatus("Sent successfully.");
      setStatusTone("success");
      event.currentTarget.reset();
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Message failed");
      setStatusTone("error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <div className="glass-panel contact-form-panel">
        <form onSubmit={submit} className="contact-form">
          <label>
            <span>Full Name</span>
            <input name="name" required maxLength={100} placeholder="Enter your name" className="contact-field" />
          </label>

          <label>
            <span>Email Address</span>
            <input
              name="email"
              required
              type="email"
              maxLength={254}
              placeholder="name@example.com"
              className="contact-field"
            />
          </label>

          <label>
            <span>Type of Inquiry</span>
            <div className="contact-select-wrap">
              <select name="inquiryType" required defaultValue="" className="contact-field contact-select">
                <option disabled value="">
                  Select inquiry type
                </option>
                <option value="Feedback">Feedback</option>
                <option value="Bug Report">Bug Report</option>
                <option value="Platform Request">Platform Request</option>
                <option value="Other">Other</option>
              </select>
              <ChevronDown size={20} />
            </div>
          </label>

          <label>
            <span>Message</span>
            <textarea
              name="message"
              required
              maxLength={4000}
              rows={5}
              placeholder="Describe your feedback or bug in detail..."
              className="contact-field contact-textarea"
            />
          </label>

          <button className="contact-submit" type="submit" disabled={submitting}>
            {submitting ? <LoaderCircle className="spin" size={20} /> : <Send size={20} />}
            {submitting ? "Processing..." : "Submit Inquiry"}
          </button>

          {status ? <p className={`contact-status ${statusTone}`}>{status}</p> : null}
        </form>
      </div>

      <div className="contact-meta">
        <span>
          <Bolt size={14} />
          Response time: &lt; 24h
        </span>
        <i />
        <span>
          <Lock size={14} />
          Secure transmission
        </span>
      </div>
    </>
  );
}

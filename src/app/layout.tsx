import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://usernamescan.com"),
  title: {
    default: "Username Scan - Check Username Availability",
    template: "%s | Username Scan",
  },
  description: "Check username availability across reliable social, creator, and gaming platforms.",
  icons: {
    icon: "/img/usernamescan.svg",
  },
  openGraph: {
    title: "Username Scan",
    description: "Check username availability across reliable social, creator, and gaming platforms.",
    url: "https://usernamescan.com",
    siteName: "Username Scan",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Username Scan",
    description: "Check username availability across reliable social, creator, and gaming platforms.",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const adsenseClient = process.env.NEXT_PUBLIC_ADSENSE_CLIENT;

  return (
    <html lang="en">
      <body>
        {adsenseClient ? (
          <Script
            async
            strategy="afterInteractive"
            src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsenseClient}`}
            crossOrigin="anonymous"
          />
        ) : null}
        {children}
      </body>
    </html>
  );
}

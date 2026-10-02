import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WasteOS — Turning Waste Into Value",
  description: "AI-powered waste management and circular economy platform.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}

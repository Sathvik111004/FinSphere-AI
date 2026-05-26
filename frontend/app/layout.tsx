import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinSphere AI — Autonomous Financial Intelligence",
  description: "Enterprise-grade financial intelligence copilot, vector RAG database, and machine learning risk prediction dashboards.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background">
        {children}
      </body>
    </html>
  );
}

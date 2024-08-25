import { SessionProvider } from "next-auth/react";
import { auth } from "@/auth";

import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Connect Four",
  description: "",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  return (
    <SessionProvider session={session}>
      <html data-theme="light" lang="en">
        <body className={inter.className}>{children}</body>
      </html>
    </SessionProvider>
  );
}

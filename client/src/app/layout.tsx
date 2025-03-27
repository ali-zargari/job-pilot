import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Toaster } from 'react-hot-toast';
import { NextUIProvider } from '@nextui-org/react';
import { ThemeProvider } from 'next-themes';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ResumePilot - AI Resume Optimization",
  description: "Transform your resume with AI-powered optimization for more interviews and better job opportunities",
  keywords: "resume optimizer, AI resume, job application, career tools, ATS-friendly",
  other: {
    "darkreader-lock": "true"
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="light">
      <body className={inter.className}>
        <NextUIProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem
            disableTransitionOnChange
          >
            <div className="flex flex-col min-h-screen">
              <Navbar />
              <main className="flex-grow">
                {children}
              </main>
              <Footer />
            </div>
            <Toaster position="bottom-right" />
          </ThemeProvider>
        </NextUIProvider>
      </body>
    </html>
  );
}

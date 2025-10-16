import type { Metadata } from "next";
import localFont from 'next/font/local';
import "./globals.css";

const bitcountFont = localFont({
  src: './bitcount-font.ttf',
  display: 'swap',
  variable: '--font-bitcount',
});

const monacoFont = localFont({
  src: './fonts/Monaco.ttf',
  display: 'swap',
  variable: '--font-monaco',
});

export const metadata: Metadata = {
  title: "Humanity's Diary",
  description: "A collective diary of human experiences",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${bitcountFont.variable} ${monacoFont.variable}`}>
        <div className="min-h-screen p-4 sm:p-6 lg:p-8">
          <div className="min-h-[calc(100vh-2rem)] sm:min-h-[calc(100vh-3rem)] lg:min-h-[calc(100vh-4rem)] bg-white dark:bg-gray-900 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}

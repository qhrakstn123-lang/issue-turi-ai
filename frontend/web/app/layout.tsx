import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ShortsFlow | AI 쇼츠 기획 스튜디오",
  description: "ShortsFlow AI 쇼츠 기획 스튜디오 미리보기 작업 화면.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}

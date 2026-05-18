import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="icon" type="image/jpeg" href="/branding/matta_logo_icon.jpg" />
        <link rel="shortcut icon" type="image/jpeg" href="/branding/matta_logo_icon.jpg" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <meta name="theme-color" content="#1F242C" />
        <meta name="description" content="Matta Lead Refinery — Theater Console" />
        <title>Matta · Lead Refinery</title>
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

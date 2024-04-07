import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        <div className="bg-gray-100">
          <img src="/2.png" alt="Notesframe" className="w-40 ml-9" />
        </div>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

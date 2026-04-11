import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="zh-CN">
      <Head>
        <meta charSet="utf-8" />
        <meta name="theme-color" content="#0ea5e9" />
        <meta property="og:image" content="/og-image.png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:image:alt" content="黄瓜病害识别系统" />
        <meta property="og:title" content="黄瓜病害识别系统---智能农业解决方案" />
        <meta property="og:description" content="基于深度学习的黄瓜病害智能识别系统，帮助农户快速诊断作物问题，提供科学防治建议" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="黄瓜病害识别系统" />
        <meta property="og:url" content="https://plant-pest-ai.example.com" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="黄瓜病害识别系统---智能农业解决方案" />
        <meta name="twitter:description" content="基于深度学习的黄瓜病害智能识别系统，帮助农户快速诊断作物问题，提供科学防治建议" />
        <meta name="twitter:image" content="/og-image.png" />
        <link rel="canonical" href="https://plant-pest-ai.example.com" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
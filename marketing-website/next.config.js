/** @type {import('next').NextConfig} */
const nextConfig = {
  // 保留你原来的图片配置
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'qingmu.cloud',
      },
    ],
    unoptimized: true,
  },
  env: {},
  
  // 可选：开发环境代理（前端已优先直连 localhost:8080，见 src/api/baseUrl.ts）
  async rewrites() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8080/api/:path*'
        }
      ]
    }
    return []
  },

  // 保留你原来的TS忽略配置
  typescript: {
    ignoreBuildErrors: true,
  }
}

module.exports = nextConfig
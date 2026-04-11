/**
 * 后端根地址（不含路径）。Spring Boot 使用 server.servlet.context-path=/api，
 * 请求路径仍写 /api/analysis/... 即可拼成 http://localhost:8080/api/analysis/...
 *
 * 优先级：NEXT_PUBLIC_API_BASE_URL > 浏览器访问 localhost 时直连 8080 > 后端服务URL
 */
export function getApiBaseUrl(): string {
  // 优先使用环境变量
  const envUrl = process.env.NEXT_PUBLIC_API_BASE_URL
  if (envUrl && envUrl.trim() !== '') {
    let url = envUrl.replace(/\/$/, '')
    // 确保URL包含/api路径
    if (!url.endsWith('/api')) {
      url += '/api'
    }
    return url
  }
  // 本地开发环境
  if (typeof window !== 'undefined') {
    const { hostname } = window.location
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return `http://${hostname}:8080/api`
    }
  }
  // 默认返回后端服务URL
  return 'https://cucumber-disease-detection.onrender.com/api'
}

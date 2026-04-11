import axios from 'axios'
import { getApiBaseUrl } from './baseUrl'

// 创建axios实例
const request = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 60000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    
    // 检查响应结构
    if (res.code === 200) {
      return res.data
    } else if (res.success) {
      // 直接返回成功响应
      return res
    } else {
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  error => {
    const ax = error as { response?: { data?: { message?: string } } }
    const msg = ax.response?.data?.message
    if (msg) {
      return Promise.reject(new Error(msg))
    }
    return Promise.reject(error)
  }
)

/**
 * 上传图片并分析
 */
export function uploadAndAnalyze(file: File, modelType: string = 'YOLOv8') {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('modelType', modelType)
  
  return request({
    url: '/analysis/upload',
    method: 'POST',
    data: formData
  })
}

/**
 * 使用Base64分析
 */
export function analyzeBase64(imageData: string, modelType: string = 'qwen3') {
  return request({
    url: '/analysis/analyze',
    method: 'POST',
    data: {
      imageData,
      modelType
    }
  })
}

/**
 * 获取支持的模型列表
 */
export function getModels() {
  return request({
    url: '/analysis/models',
    method: 'GET'
  })
}
import axios, { AxiosError, AxiosResponse } from 'axios';
import { getApiBaseUrl } from './baseUrl';

// 定义返回值类型（整合新代码的TS规范 + 原有业务逻辑）
interface AIChatResponse {
  success: boolean;
  content: string | null;
  error?: string; // 替换原message，更贴合AI聊天的错误语义
}

// 2. 重构Axios实例：保留原有拦截器 + 新代码的配置规范
const aiApi = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 60000, // 保留原有超时时间（AI请求耗时更长，10s太短）
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
aiApi.interceptors.request.use(
  config => {
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
aiApi.interceptors.response.use(
  (response: AxiosResponse) => {
    return response; // 注意：这里不再直接返回data，交给业务函数处理（避免拦截器层丢失上下文）
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * 3. 核心聊天方法：保留原有messages逻辑 + 新代码的TS/错误处理
 * @param messages 消息列表（原有业务逻辑）
 * @returns 标准化响应
 */
export async function sendAIChatMessage(
  messages: Array<{ role: string; content: string }>
): Promise<AIChatResponse> {
  try {
    // 保留原有“取最新用户消息”的业务逻辑
    const latestUserMessage = [...messages].reverse().find(item => item.role === 'user')?.content || '';
    
    // 新代码的Axios请求写法（规范TS类型 + 修复原response.response错误）
    const response: AxiosResponse = await aiApi.post('/chat', {
      query: latestUserMessage, // 适配后端API参数名
    });

    // 修复核心错误：用response.data替代原response.response
    return {
      success: true,
      content: response.data.answer || '', // 适配后端API返回结构
    };
  } catch (error) {
    // 整合新代码的精细化错误处理
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      // 服务器返回错误（4xx/5xx）
      return {
        success: false,
        content: null,
        error: (axiosError.response.data as any)?.error?.message || '服务器返回错误',
      };
    } else if (axiosError.request) {
      // 网络错误（无响应）
      return {
        success: false,
        content: null,
        error: '网络请求失败，请检查网络连接',
      };
    } else {
      // 其他错误（参数/配置错误）
      return {
        success: false,
        content: null,
        error: `请求失败：${axiosError.message}`,
      };
    }
  }
}

/**
 * 4. 流式聊天方法：保留原有逻辑 + 补充TS类型 + 优化错误处理
 * @param messages 消息列表
 * @param onMessage 接收消息回调
 * @param onError 错误回调
 * @param onComplete 完成回调
 */
export async function sendAIChatMessageStream(
  messages: Array<{ role: string; content: string }>,
  onMessage: (content: string) => void,
  onError: (error: string) => void,
  onComplete: () => void
): Promise<void> {
  try {
    const latestUserMessage = [...messages].reverse().find(item => item.role === 'user')?.content || '';
    const response = await fetch(`${getApiBaseUrl()}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: latestUserMessage }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '请求失败');
    }

    const data = await response.json();
    onMessage(data.answer || '');
    onComplete();
  } catch (error) {
    console.error('流式AI咨询请求失败:', error);
    // 复用新代码的错误提示逻辑
    const errorMsg = (error as Error).message || '请求失败，请稍后重试';
    onError(errorMsg);
  }
}

// 兼容原有默认导出（如果其他文件用了默认导入）
export default sendAIChatMessage;
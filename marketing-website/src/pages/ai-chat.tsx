import Head from 'next/head'
import { useState, useRef, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { getApiBaseUrl } from '../api/baseUrl'

interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
}

const QUICK_QUESTIONS = [
  '黄瓜叶子发黄怎么办？',
  '如何防治黄瓜霜霉病？',
  '黄瓜枯萎病的症状是什么？',
  '黄瓜最佳种植时间是什么时候？',
  '如何提高黄瓜产量？'
]

export default function AIChatPage() {
  const apiBaseUrl = getApiBaseUrl()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: '您好!我是您的AI农业顾问,专门为您解答黄瓜种植和病害防治方面的问题。请问有什么可以帮助您的吗?',
      role: 'assistant'
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [inputHeight, setInputHeight] = useState('56px')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      const newHeight = Math.min(inputRef.current.scrollHeight, 140)
      setInputHeight(`${Math.max(newHeight, 56)}px`)
    }
  }

  const sendMessage = async (rawMessage?: string) => {
    const message = (rawMessage ?? input).trim()
    if (!message) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: message,
      role: 'user'
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setInputHeight('56px')
    setIsLoading(true)

    try {
      const response = await fetch(`${apiBaseUrl}/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
      })

      if (!response.ok) {
        throw new Error('Failed to get AI response')
      }

      const data = await response.json()
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response ?? '抱歉，我暂时无法回答您的问题。请稍后再试。',
        role: 'assistant'
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: '抱歉，我暂时无法回答您的问题。请稍后再试。',
        role: 'assistant'
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <>
      <Head>
        <title>AI农业顾问 - 黄瓜病害识别系统</title>
        <meta
          name="description"
          content="AI农业顾问为您提供黄瓜种植和病害防治问答服务，帮助您快速获得科学建议。"
        />
      </Head>

      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <Navbar />

        <section className="pt-28 pb-10">
          <div className="container">
            <div className="text-center mb-10">
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
                <span className="text-gradient">AI农业顾问</span>
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                您好!我是您的AI农业顾问,专门为您解答黄瓜种植和病害防治方面的问题。请问有什么可以帮助您的吗?
              </p>
            </div>

            <div className="max-w-5xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-4 md:p-6">
              <div className="border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">智能农业顾问</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">实时解答您的农业问题</p>
              </div>

              <div className="h-[52vh] overflow-y-auto space-y-4 pr-1">
                {messages.map((message) => (
                  <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div
                      className={`max-w-[85%] px-4 py-3 rounded-2xl ${
                        message.role === 'user'
                          ? 'text-white rounded-tr-md'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-tl-md'
                      }`}
                      style={message.role === 'user' ? { backgroundColor: 'rgb(2 132 199 / var(--tw-bg-opacity, 1))' } : undefined}
                    >
                      <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[85%] px-4 py-3 rounded-2xl rounded-tl-md bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                      正在思考...
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
                <div className="flex flex-col sm:flex-row gap-3">
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyPress}
                    placeholder="输入您的问题..."
                    className="flex-1 px-5 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-primary-200 dark:border-gray-600 rounded-xl shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none transition-all duration-300"
                    style={{ height: inputHeight }}
                  />
                  <button
                    onClick={() => sendMessage()}
                    disabled={!input.trim() || isLoading}
                    className="px-8 py-4 text-white text-lg font-semibold rounded-xl shadow-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    style={{ backgroundColor: 'rgb(2 132 199 / var(--tw-bg-opacity, 1))' }}
                  >
                    发送
                  </button>
                </div>
              </div>
            </div>

            <div className="max-w-5xl mx-auto mt-8">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">常见问题</h3>
              <div className="flex flex-wrap gap-3">
                {QUICK_QUESTIONS.map((question) => (
                  <button
                    key={question}
                    onClick={() => sendMessage(question)}
                    className="px-5 py-3 bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 text-sm font-medium rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-primary-200 dark:border-gray-700"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}

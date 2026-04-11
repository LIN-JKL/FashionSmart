'use client'

import { useState, useEffect } from 'react'
import { Disclosure } from '@headlessui/react'
import { Bars3Icon, XMarkIcon, SparklesIcon, PlayIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import ThemeToggle from './ThemeToggle'

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const router = useRouter()

  const navigation = [
    { name: '首页', href: '/' },
    { name: 'AI咨询', href: '/ai-chat' },
    { name: '功能特性', href: '#features' },
    { name: '技术介绍', href: '#ai-tech' },
    { name: '关于我们', href: '#about' },
  ]

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true)
      } else {
        setIsScrolled(false)
      }
    }

    window.addEventListener('scroll', handleScroll)
    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  const scrollToSection = (sectionId: string) => {
    if (sectionId.startsWith('/')) {
      // 处理以'/'开头的路径，直接导航
      router.push(sectionId)
    } else if (router.pathname === '/') {
      if (sectionId === '/') {
        // 如果是首页链接，滚动到页面顶部
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        // 其他锚点链接
        const element = document.querySelector(sectionId)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
      }
    } else {
      // 非首页且不是以'/'开头的链接，先导航到首页再滚动
      router.push('/')
      setTimeout(() => {
        const element = document.querySelector(sectionId)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
      }, 100)
    }
  }

  return (
    <Disclosure as="nav" className={`fixed w-full z-50 transition-all duration-300 ${isScrolled ? 'bg-white/95 dark:bg-gray-900/95 backdrop-blur-md shadow-md' : 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm'}`}>
      {({ open }) => (
        <>
          <div className="container">
            <div className="flex h-16 items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Link href="/" className="flex items-center">
                    <img 
                      src="/logo.jpg" 
                      alt="黄瓜病害识别" 
                      className="w-10 h-10 rounded-lg object-cover shadow-lg"
                    />
                    <span className="ml-2 text-xl font-bold text-gray-900 dark:text-white">
                      黄瓜病害识别
                    </span>
                  </Link>
                </div>
                <div className="hidden md:block">
                  <div className="ml-10 flex items-baseline space-x-4">
                    {navigation.map((item) => (
                      <button
                        key={item.name}
                        onClick={() => scrollToSection(item.href)}
                        className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                          isScrolled
                            ? 'text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20'
                            : 'text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20'
                        }`}
                      >
                        {item.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
              <div className="hidden md:block">
                <div className="ml-4 flex items-center md:ml-6">
                  <ThemeToggle />
                  <Link 
                    href="/analysis" 
                    className="ml-2 px-3 py-2 text-sm font-medium rounded-md shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 text-white"
                    style={{ backgroundColor: 'rgb(2 132 199 / var(--tw-bg-opacity, 1))' }}
                  >
                    立即体验
                  </Link>
                </div>
              </div>
              <div className="-mr-2 flex md:hidden">
                <Disclosure.Button className={`inline-flex items-center justify-center rounded-md p-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500`}>
                  <span className="sr-only">打开主菜单</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="md:hidden bg-white dark:bg-gray-900 shadow-lg">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigation.map((item) => (
                <Disclosure.Button
                  key={item.name}
                  as="button"
                  onClick={() => scrollToSection(item.href)}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200"
                >
                  {item.name}
                </Disclosure.Button>
              ))}
            </div>
            <div className="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700">
              <div className="px-2 flex items-center justify-center mb-4">
                <ThemeToggle />
              </div>
              <div className="px-2">
                <Link href="/analysis" className="block w-full text-center px-4 py-2 text-sm font-medium rounded-md shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 text-white" style={{ backgroundColor: 'rgb(2 132 199 / var(--tw-bg-opacity, 1))' }}>
                  立即体验
                </Link>
              </div>
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  )
}
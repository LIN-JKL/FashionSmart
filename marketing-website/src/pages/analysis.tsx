import { useState } from 'react'
import Head from 'next/head'
import { motion } from 'framer-motion'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import CookieBanner, { CookieSettings } from '../components/CookieBanner'
import { uploadAndAnalyze } from '../api/analysis'

// 病害信息映射，包含详细分析和防治建议
const diseaseInfo = {
  '炭疽病': {
    analysis: '炭疽病是黄瓜常见的真菌性病害，主要危害叶片、茎蔓和果实。初期在叶片上产生水渍状小斑点，后扩大为圆形或不规则形病斑，中央灰白色，边缘褐色，病斑上有黑色小点。茎蔓受害后出现凹陷的褐色病斑，严重时导致茎蔓枯萎。果实受害后出现暗褐色病斑，表面凹陷，严重影响果实品质和产量。',
    prevention: '1. 农业防治：选用抗病品种，合理轮作，加强通风透光，降低田间湿度。2. 种子处理：播种前用55℃温水浸种15分钟，或用多菌灵拌种。3. 药剂防治：发病初期可选用代森锰锌、炭疽福美、咪鲜胺等药剂喷雾防治，每隔7-10天喷一次，连续防治2-3次。4. 清洁田园：及时清除病残体，减少菌源。'
  },
  '细菌性枯萎病': {
    analysis: '细菌性枯萎病是由细菌引起的维管束病害，主要危害黄瓜的茎蔓。发病初期叶片出现暗绿色水浸状斑点，随后叶片迅速萎蔫，茎蔓维管束变褐，用手挤压病茎会流出白色菌脓。该病传播速度快，一旦发病，病情发展迅速，严重时可导致全株死亡。',
    prevention: '1. 农业防治：选用抗病品种，实行轮作，避免与瓜类作物连作。2. 种子处理：用温汤浸种或药剂拌种。3. 土壤消毒：种植前对土壤进行消毒处理。4. 药剂防治：发病初期可选用农用链霉素、新植霉素、中生菌素等药剂灌根或喷雾防治。5. 控制传播：及时清除病株，避免农事操作传播病菌。'
  },
  '脐腐病': {
    analysis: '脐腐病主要危害黄瓜果实，是一种生理病害。发病初期在果实脐部出现水渍状暗绿色斑点，后扩大为暗褐色凹陷病斑，严重时病斑可扩展至果实的1/3以上。该病主要是由于土壤缺钙或水分供应不均衡引起的，尤其是在果实快速膨大期。',
    prevention: '1. 合理施肥：增施有机肥，补充钙肥，避免偏施氮肥。2. 水分管理：保持土壤湿润，避免土壤忽干忽湿。3. 叶面补钙：在果实膨大期，可叶面喷施氯化钙或硝酸钙溶液。4. 品种选择：选用抗病品种。'
  },
  '霜霉病': {
    analysis: '霜霉病是黄瓜最常见的真菌性病害之一，主要危害叶片。发病初期叶片上出现淡黄色小斑点，后扩大为多角形病斑，叶背病斑上产生灰白色霉层。严重时叶片干枯，影响光合作用，导致产量下降。该病在高湿度、温度适宜的条件下容易发生。',
    prevention: '1. 农业防治：选用抗病品种，合理密植，加强通风透光，降低田间湿度。2. 药剂防治：发病初期可选用霜脲锰锌、烯酰吗啉、吡唑醚菌酯等药剂喷雾防治，每隔7-10天喷一次，连续防治2-3次。3. 生态防治：利用温湿度调控，创造不利于病害发生的环境条件。'
  },
  '茎枯病': {
    analysis: '茎枯病是由真菌引起的病害，主要危害黄瓜的茎蔓。发病初期在茎蔓上出现水渍状病斑，后扩大为褐色凹陷病斑，病斑上产生黑色小点。严重时茎蔓腐烂，导致植株死亡。该病在高温高湿的环境条件下容易发生。',
    prevention: '1. 农业防治：选用抗病品种，合理轮作，加强通风透光，降低田间湿度。2. 种子处理：播种前用多菌灵拌种。3. 药剂防治：发病初期可选用代森锰锌、甲基硫菌灵、多菌灵等药剂喷雾防治。4. 清洁田园：及时清除病残体，减少菌源。'
  },
  '腐霉果腐病': {
    analysis: '腐霉果腐病是由腐霉菌引起的病害，主要危害黄瓜果实。发病初期在果实表面出现水渍状斑点，后扩大为褐色软腐病斑，严重时整个果实腐烂。该病在高湿度、温度适宜的条件下容易发生，尤其是在果实接近成熟时。',
    prevention: '1. 农业防治：加强通风透光，降低田间湿度，避免果实与地面接触。2. 药剂防治：发病初期可选用甲霜灵、恶霉灵、霜霉威等药剂喷雾防治。3. 清洁田园：及时清除病果，减少菌源。4. 合理灌溉：避免大水漫灌，采用滴灌或喷灌。'
  },
  '健康黄瓜果实': {
    analysis: '该黄瓜果实生长正常，无明显病害症状。果实外观光滑，颜色均匀，无病斑、腐烂等现象。',
    prevention: '1. 继续保持良好的栽培管理，合理施肥浇水。2. 定期巡查，及时发现并处理病虫害。3. 注意通风透光，保持适宜的温湿度条件。4. 采收时注意轻拿轻放，避免机械损伤。'
  },
  '健康叶片': {
    analysis: '该黄瓜叶片生长正常，无明显病害症状。叶片颜色鲜绿，叶脉清晰，无病斑、黄化等现象。',
    prevention: '1. 继续保持良好的栽培管理，合理施肥浇水。2. 定期巡查，及时发现并处理病虫害。3. 注意通风透光，保持适宜的温湿度条件。4. 及时清除老叶、病叶，减少病虫害滋生的场所。'
  }
}

export default function Analysis() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [selectedModel, setSelectedModel] = useState('YOLOv8')
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      setResult(null)
    }
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    setPreviewUrl('')
    setResult(null)
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('请先选择一张图片')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    
    try {
      const response = await uploadAndAnalyze(selectedFile, selectedModel)

      if (response?.success === false && response?.errorMessage) {
        setError(String(response.errorMessage))
        setResult(response)
        return
      }

      // 将"gummy茎枯病"替换为"茎枯病"
      if (response.diseaseName === 'gummy茎枯病') {
        response.diseaseName = '茎枯病'
      }
      setResult(response)
    } catch (err) {
      const msg = err instanceof Error ? err.message : '分析失败，请重试'
      setError(msg || '分析失败，请重试')
    } finally {
      setIsAnalyzing(false)
    }
  }



  return (
    <>
      <Head>
        <title>黄瓜病害识别 - 在线识别</title>
    <meta name="description" content="使用先进的AI技术识别黄瓜病害，提供专业的防治建议" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        
        <main className="container mx-auto px-4 py-8 pt-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-10"
          >
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">黄瓜病害识别</h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              上传黄瓜图片，我们的模型系统将为您快速识别病害并提供专业防治建议
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* 上传区域 */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-6 flex items-center">
                  <span className="mr-2">📸</span> 上传黄瓜图片
                </h2>
                
                {!previewUrl ? (
                  <div className="border-2 border-dashed border-primary-300 dark:border-primary-600 rounded-lg p-8 text-center bg-primary-50 dark:bg-gray-700">
                    <div className="mb-4">
                      <svg className="mx-auto h-12 w-12 text-primary-500 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <span className="text-primary-600 dark:text-primary-400 font-medium">点击上传图片</span>
                      <span className="text-gray-500 dark:text-gray-400"> 或拖拽文件到此处</span>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">支持 JPG、PNG、WEBP 格式，大小不超过 10MB</p>
                      <input id="file-upload" name="file-upload" type="file" className="sr-only" accept="image/*" onChange={handleFileChange} />
                    </label>
                  </div>
                ) : (
                  <div className="relative">
                    <img src={previewUrl} alt="预览" className="w-full h-64 object-cover rounded-lg" />
                    <button
                      onClick={handleRemoveFile}
                      className="absolute top-2 right-2 bg-red-500 dark:bg-red-600 text-white rounded-full p-2 hover:bg-red-600 dark:hover:bg-red-700 transition-colors"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                )}

                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">选择模型：</label>
                  <select 
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-gray-200"
                  >
                    <option value="YOLOv8">YOLOv8黄瓜病害识别模型</option>
                  </select>
                </div>

                {error && (
                  <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 rounded-md">
                    {error}
                  </div>
                )}

                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || isAnalyzing}
                  className="w-full mt-6 bg-primary-600 dark:bg-primary-700 text-white py-3 px-4 rounded-md font-medium hover:bg-primary-700 dark:hover:bg-primary-600 disabled:bg-gray-400 dark:disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                >
                  {isAnalyzing ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      分析中...
                    </>
                  ) : (
                    <>
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                      </svg>
                      开始分析
                    </>
                  )}
                </button>
              </div>
            </motion.div>

            {/* 结果展示区域 */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              {result && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="space-y-6"
                >
                  {result.success === false && result.errorMessage && (
                    <div className="p-4 bg-red-50 dark:bg-red-900/40 border border-red-200 dark:border-red-800 rounded-lg text-red-800 dark:text-red-200 text-sm">
                      {result.errorMessage}
                    </div>
                  )}
                  {/* 识别概览 */}
                  <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">识别概览</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">识别类型</p>
                        <p className="font-medium dark:text-gray-200">{result.identificationType === 'pest' ? '害虫识别' : '病害识别'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">置信度</p>
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2.5 mr-2">
                            <div 
                              className="bg-blue-600 h-2.5 rounded-full" 
                              style={{ width: `${(result.confidence || 0) * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm dark:text-gray-300">{Math.round((result.confidence || 0) * 100)}%</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 植物信息 */}
                  <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border border-green-200 dark:border-green-800">
                    <h3 className="text-lg font-semibold text-green-800 dark:text-green-300 mb-3">植物信息</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">植物名称</p>
                        <p className="font-medium dark:text-gray-200">黄瓜</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">使用模型</p>
                        <p className="font-medium dark:text-gray-200">{result.modelUsed || selectedModel}</p>
                      </div>
                    </div>
                  </div>

                  {/* 病害检测结果 */}
                  {result.diseaseName && (
                    <div className="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg border border-red-200 dark:border-red-800">
                      <h3 className="text-lg font-semibold text-red-800 dark:text-red-300 mb-4 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        检测结果
                      </h3>
                      
                      <div className="space-y-3 text-gray-700 dark:text-gray-300">
                        <div className="flex items-start">
                          <span className="font-medium min-w-[80px]">病害名称：</span>
                          <span>{result.diseaseName}</span>
                        </div>
                        <div className="flex items-start">
                          <span className="font-medium min-w-[80px]">置信度：</span>
                          <span>{(result.confidence || 0) * 100}%</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* 详细分析 */}
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
                    <h3 className="text-lg font-semibold text-blue-800 dark:text-blue-300 mb-3">详细分析</h3>
                    <div className="text-gray-700 dark:text-gray-300">
                      {result.diseaseName && diseaseInfo[result.diseaseName] ? (
                        diseaseInfo[result.diseaseName].analysis.split('\n').map((line: string, index: number) => (
                          <p key={index} className="mb-2">{line}</p>
                        ))
                      ) : (
                        <>
                          {result.description && (
                            <p className="mb-2">{result.description}</p>
                          )}
                          {result.detailedAnalysis && (
                            <p className="mb-2">{result.detailedAnalysis}</p>
                          )}
                          {!result.description && !result.detailedAnalysis && (
                            <p className="mb-2">暂无详细分析信息</p>
                          )}
                        </>
                      )}
                    </div>
                  </div>

                  {/* 防治建议 */}
                  <div className="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-800">
                    <h3 className="text-lg font-semibold text-purple-800 dark:text-purple-300 mb-3">防治建议</h3>
                    <div className="text-gray-700 dark:text-gray-300">
                      {result.diseaseName && diseaseInfo[result.diseaseName] ? (
                        diseaseInfo[result.diseaseName].prevention.split('\n').map((line: string, index: number) => (
                          <p key={index} className="mb-2">{line}</p>
                        ))
                      ) : (
                        <>
                          {result.recommendations && result.recommendations.split('\n').map((line: string, index: number) => (
                            <p key={index} className="mb-2">{line}</p>
                          ))}
                          {result.suggestion && result.suggestion.split('\n').map((line: string, index: number) => (
                            <p key={index} className="mb-2">{line}</p>
                          ))}
                        </>
                      )}
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </div>
        </main>
        
        <Footer />
        
        {/* Cookie横幅和设置 */}
        <CookieBanner />
        <CookieSettings />
      </div>
    </>
  )
}
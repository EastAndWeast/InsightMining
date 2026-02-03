"use client";

import React, { useState } from 'react';

// 定义分析结果的类型接口
interface AnalysisResult {
  categories: {
    pain_points: string[];
    missing_features: string[];
    highlights: string[];
  };
  software_opportunity: {
    concept: string;
    target_users: string;
    value_prop: string;
  };
  marketing: {
    ad_copy: string;
    image_prompt: string;
    video_script: string;
  };
}

export default function DashboardPage() {
  const [url, setUrl] = useState('');
  const [platform, setPlatform] = useState('App Store');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, platform }),
      });

      if (!response.ok) throw new Error('捕获过程异常，请检查后端服务');

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || '系统繁忙，请稍后再试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#F5F3FF] p-4 md:p-8 lg:p-12">
      <div className="max-w-6xl mx-auto space-y-12">
        {/* Header Section */}
        <section className="text-center space-y-4">
          <div className="inline-block bg-indigo-100 text-[#6366F1] px-4 py-1.5 rounded-full text-sm font-bold tracking-tight mb-2">
            REVIEW INSIGHT V1.0
          </div>
          <h1 className="text-4xl md:text-5xl font-black text-[#1E1B4B] tracking-tighter">
            从<span className="text-[#6366F1]">用户槽点</span>中提取<span className="text-[#10B981]">商业机会</span>
          </h1>
          <p className="text-slate-500 max-w-xl mx-auto font-medium">
            AI 自动处理海量评价，为您揭示隐藏在负面反馈中的千万级软件空白点。
          </p>
        </section>

        {/* Input Control Box */}
        <section className="bg-white p-6 md:p-10 rounded-3xl shadow-2xl border border-white/50 space-y-8">
          <div className="space-y-4">
            <label className="text-xs font-black text-slate-400 uppercase tracking-widest pl-1">
              目标产品链接 (PRODUCT URL)
            </label>
            <div className="flex flex-col md:row-span-1 md:flex-row gap-4">
              <input
                type="text"
                placeholder="在此粘贴 Amazon, App Store, TikTok 或 Google Maps 链接..."
                className="flex-1 bg-slate-50 border border-slate-100 px-6 py-4 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <button
                onClick={handleAnalyze}
                disabled={loading || !url}
                className="bg-[#6366F1] text-white px-10 py-4 rounded-2xl font-black shadow-lg shadow-indigo-200 hover:bg-indigo-700 active:scale-95 transition-all disabled:opacity-50"
              >
                {loading ? 'AI 正在推演中...' : '启动 AI 洞察'}
              </button>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            {['App Store', 'Amazon', 'Google Maps', 'TikTok', 'Shopee'].map(p => (
              <button
                key={p}
                onClick={() => setPlatform(p)}
                className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all border ${platform === p
                    ? 'bg-[#1E1B4B] text-white border-transparent shadow-lg'
                    : 'bg-white text-slate-400 border-slate-100 hover:border-slate-300'
                  }`}
              >
                {p}
              </button>
            ))}
          </div>
        </section>

        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-2xl text-center font-bold border border-red-100 animate-bounce">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="py-20 text-center space-y-6">
            <div className="flex justify-center gap-2">
              <div className="w-3 h-12 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-3 h-12 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-3 h-12 bg-indigo-300 rounded-full animate-bounce"></div>
            </div>
            <p className="text-slate-400 font-black uppercase tracking-tighter animate-pulse">
              正在深度解析用户情感模型...
            </p>
          </div>
        )}

        {/* Results Dashboard */}
        {result && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-5 duration-700">

            {/* Opportunity Card - Left Column */}
            <div className="bg-[#6366F1] p-8 md:p-12 rounded-[2.5rem] text-white relative overflow-hidden flex flex-col justify-between min-h-[500px] shadow-2xl">
              <div className="absolute top-0 right-0 p-8 opacity-20 pointer-events-none">
                <svg className="w-32 h-32" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2z" /></svg>
              </div>

              <div className="space-y-4">
                <span className="bg-white/20 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest">推演机会 (OPPORTUNITY)</span>
                <h2 className="text-5xl font-black leading-none">{result.software_opportunity.concept}</h2>
                <p className="text-indigo-100 text-xl font-medium italic opacity-80 pt-4 leading-relaxed">
                  “{result.software_opportunity.value_prop}”
                </p>
              </div>

              <div className="space-y-6 pt-12">
                <div className="grid grid-cols-2 gap-6 border-t border-white/20 pt-8">
                  <div>
                    <p className="text-white/50 text-[10px] font-black uppercase tracking-widest mb-1">目标用户</p>
                    <p className="font-bold">{result.software_opportunity.target_users}</p>
                  </div>
                  <div>
                    <p className="text-white/50 text-[10px] font-black uppercase tracking-widest mb-1">破局逻辑</p>
                    <p className="font-bold">以痛点为基准降维打击</p>
                  </div>
                </div>
                <button className="w-full bg-[#10B981] hover:bg-emerald-600 text-white py-5 rounded-2xl font-black text-lg transition-all shadow-xl shadow-black/20 active:scale-95">
                  获取完整 PRD 框架 →
                </button>
              </div>
            </div>

            {/* Insight & Marketing - Right Column */}
            <div className="flex flex-col gap-8">
              {/* Pain Point Wall */}
              <div className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-xl space-y-6">
                <h3 className="text-sm font-black text-slate-300 uppercase tracking-widest">
                  用户情绪地图 (EMOTION MAP)
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.categories.pain_points.map((pt, i) => (
                    <span key={i} className="bg-red-50 text-red-600 px-4 py-2 rounded-xl text-xs font-bold border border-red-100">
                      {pt}
                    </span>
                  ))}
                  {result.categories.missing_features.map((ms, i) => (
                    <span key={i} className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-xl text-xs font-bold border border-indigo-100">
                      渴望: {ms}
                    </span>
                  ))}
                </div>
              </div>

              {/* Marketing Toolkit */}
              <div className="bg-slate-900 p-8 rounded-[2.5rem] shadow-xl space-y-8">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest">
                    AI 自动营销包 (MARKETING)
                  </h3>
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-red-500"></div>
                    <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  </div>
                </div>

                <div className="space-y-6">
                  <div>
                    <p className="text-emerald-400 font-mono text-[10px] mb-2 uppercase tracking-widest">// 社媒首发文案</p>
                    <div className="text-slate-300 text-xs font-medium leading-relaxed bg-white/5 p-5 rounded-2xl border border-white/10 italic">
                      {result.marketing.ad_copy}
                    </div>
                  </div>

                  <div>
                    <p className="text-indigo-400 font-mono text-[10px] mb-2 uppercase tracking-widest">// 生成海报提示词 (PROMPT)</p>
                    <code className="block bg-black p-5 rounded-2xl text-[10px] text-slate-500 border border-white/5 leading-relaxed overflow-x-auto">
                      {result.marketing.image_prompt}
                    </code>
                  </div>
                </div>

                <div className="pt-2">
                  <button className="flex items-center gap-2 text-white/40 hover:text-white transition-colors text-xs font-bold">
                    查看 15s 视频演示脚本 <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
      `}</style>
    </main>
  );
}

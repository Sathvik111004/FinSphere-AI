"use client";
 
import { useState } from "react";
import Sidebar from "../../../components/sidebar";
import { TrendingUp, Sparkles, FolderLock, AlertTriangle, ChevronRight, HelpCircle, FileText, CheckCircle2 } from "lucide-react";
import { apiService } from "../../../services/api";
 
export default function EarningsPage() {
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
 
  const sampleTranscript = (
    "First Quarter Financial Results Summary:\n\n" +
    "We delivered robust revenue growth of 18% year-over-year, beat our expectations. " +
    "Our enterprise cloud platforms outperformed expectations, driven by strong growth in SaaS adoptions. " +
    "Consequently, our operating margin improved to 22%, representing solid profitability expansion.\n\n" +
    "However, we expect persistent macroeconomic headwinds to create challenges in our EMEA channels. " +
    "We see a moderate contraction and deficit in supply chain logistics margins, representing liquidity-concerns. " +
    "We also face a potential lawsuit from proprietary infringements, which could cause a shortfall.\n\n" +
    "Looking forward to the future, our target guidance outlines a positive revenue outlook. " +
    "We target capital capex expansions of $45M as we expect robust synergies."
  );
 
  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!transcript.trim()) return;
    setLoading(true);
    try {
      const data = await apiService.ml.analyzeSentiment(transcript);
      setResults(data);
    } catch (e: any) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 pl-64 grid-dots pb-12">
      <Sidebar />
      
      <main className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
        
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            Earnings Call Tone & Risk Analyzer
          </h1>
          <p className="text-sm text-gray-400 max-w-[700px]">
            Paste raw transcript text from your corporate calls. The AI will analyze executive confidence, find future commitments, and highlight warning signs.
          </p>
        </div>
 
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Transcript input card */}
          <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4 h-fit">
            <h2 className="text-base font-extrabold text-white pl-0.5">Paste Call Transcript</h2>
            
            <form onSubmit={handleAnalyze} className="space-y-4">
              <div>
                <textarea
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  required
                  rows={10}
                  className="w-full px-3.5 py-3.5 bg-gray-900/60 border border-white/[0.06] rounded-2xl text-xs font-semibold font-mono text-gray-300 placeholder-gray-600 leading-relaxed"
                  placeholder="Paste raw earnings call transcript disclosures..."
                />
              </div>
 
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setTranscript(sampleTranscript)}
                  className="px-4 py-2.5 bg-white/[0.02] hover:bg-white/[0.04] border border-white/[0.05] text-[10px] text-gray-400 font-extrabold uppercase tracking-wider rounded-xl transition-all flex items-center gap-1.5 shrink-0"
                >
                  <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Use Sample</span>
                </button>
 
                <button
                  type="submit"
                  disabled={loading || !transcript.trim()}
                  className="flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all shadow-lg"
                >
                  {loading ? "Scanning Tone..." : "Scan Call Sentiment"}
                </button>
              </div>
            </form>
          </div>
 
          {/* Results Analysis output panels */}
          <div className="lg:col-span-2 space-y-6">
            
            {results ? (
              <div className="space-y-6 animate-fade-in">
                
                {/* Sentiment gauge preview */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="glass-panel-premium p-5 rounded-2xl border border-white/[0.04] flex justify-between items-center">
                    <div className="space-y-1">
                      <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wider">Overall Management Tone</span>
                      <div className={`text-xl font-black uppercase tracking-wide ${
                        results.overall_sentiment === "positive" 
                          ? "text-emerald-400 drop-shadow-[0_0_8px_rgba(16,185,129,0.3)]" 
                          : results.overall_sentiment === "negative" 
                          ? "text-red-400 drop-shadow-[0_0_8px_rgba(239,68,68,0.3)]" 
                          : "text-gray-400"
                      }`}>
                        {results.overall_sentiment}
                      </div>
                    </div>
                    <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.05] text-gray-400 shadow-inner">
                      <CheckCircle2 className={`w-5 h-5 ${results.overall_sentiment === "positive" ? "text-emerald-400" : "text-gray-500"}`} />
                    </div>
                  </div>
                  
                  <div className="glass-panel-premium p-5 rounded-2xl border border-white/[0.04] flex justify-between items-center">
                    <div className="space-y-1">
                      <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wider">Executive Confidence Index</span>
                      <div className="text-xl font-black text-indigo-400 drop-shadow-[0_0_8px_rgba(99,102,241,0.3)]">
                        {results.sentiment_score.toFixed(2)}
                      </div>
                    </div>
                    <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.05] text-indigo-400 shadow-inner">
                      <TrendingUp className="w-5 h-5" />
                    </div>
                  </div>
                </div>
 
                {/* Highlighted text preview */}
                <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4">
                  <h3 className="text-xs font-extrabold text-white uppercase tracking-widest pl-0.5">Paragraph-by-Paragraph Tone Breakdown</h3>
                  
                  <div className="space-y-3 max-h-60 overflow-y-auto pr-1">
                    {results.paragraph_breakdowns.map((p: any, idx: number) => {
                      const isPos = p.label === "positive";
                      const isNeg = p.label === "negative";
                      
                      return (
                        <div 
                          key={idx}
                          className={`p-4 rounded-2xl border text-xs leading-relaxed transition-all ${
                            isPos 
                              ? "bg-emerald-500/5 border-emerald-500/20 text-emerald-200" 
                              : isNeg 
                              ? "bg-red-500/5 border-red-500/20 text-red-200"
                              : "bg-white/[0.015] border-white/[0.035] text-gray-400"
                          }`}
                        >
                          {p.text}
                          <div className="text-[9px] mt-2.5 opacity-70 font-bold uppercase tracking-widest flex items-center gap-1">
                            <span className={`w-1.5 h-1.5 rounded-full ${isPos ? "bg-emerald-400 animate-pulse" : isNeg ? "bg-red-400 animate-pulse" : "bg-gray-500"}`} />
                            <span>Tone: {p.label} (Conf: {(p.confidence * 100).toFixed(0)}%)</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
 
                {/* Extracted targets metrics (guidance and risks) */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  <div className="glass-panel-premium p-5 rounded-3xl border border-white/[0.04] space-y-4">
                    <h4 className="text-xs font-extrabold text-emerald-400 uppercase tracking-widest pl-0.5">Extracted Commitments & Guidance</h4>
                    <div className="space-y-2">
                      {results.extracted_guidance.length === 0 ? (
                        <p className="text-[10px] text-gray-500 pl-0.5 uppercase font-semibold">No forward growth projections found.</p>
                      ) : (
                        results.extracted_guidance.map((item: string, idx: number) => (
                          <div key={idx} className="flex gap-2.5 p-3.5 bg-white/[0.01] border border-white/[0.03] rounded-2xl text-xs text-gray-300 leading-relaxed shadow-inner">
                            <ChevronRight className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                            <span>{item}</span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
 
                  <div className="glass-panel-premium p-5 rounded-3xl border border-white/[0.04] space-y-4">
                    <h4 className="text-xs font-extrabold text-red-400 uppercase tracking-widest pl-0.5">Identified Risk & Threat Warnings</h4>
                    <div className="space-y-2">
                      {results.extracted_risks.length === 0 ? (
                        <p className="text-[10px] text-gray-500 pl-0.5 uppercase font-semibold">No significant threats identified.</p>
                      ) : (
                        results.extracted_risks.map((item: string, idx: number) => (
                          <div key={idx} className="flex gap-2.5 p-3.5 bg-white/[0.01] border border-white/[0.03] rounded-2xl text-xs text-gray-300 leading-relaxed shadow-inner">
                            <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                            <span>{item}</span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
 
                </div>
 
              </div>
            ) : (
              <div className="h-64 border border-dashed border-white/[0.05] rounded-3xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                <TrendingUp className="w-8 h-8 text-gray-600 mb-2" />
                <p className="text-xs font-bold text-gray-400">Insert raw transcription files and analyze.</p>
                <p className="text-[9px] text-gray-500 mt-1 uppercase font-semibold">Interactive tone highlights and statement lists will output here.</p>
              </div>
            )}
 
          </div>
 
        </section>
 
      </main>
    </div>
  );
}

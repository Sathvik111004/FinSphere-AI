"use client";
 
import { useEffect, useState } from "react";
import Sidebar from "../../../components/sidebar";
import InteractiveChart from "../../../components/ui/InteractiveChart";
import { PieChart, Sparkles, FolderLock, PlusCircle, Check, ShieldAlert, BookOpen, Clock, ChevronRight } from "lucide-react";
import { apiService } from "../../../services/api";
 
export default function PortfolioPage() {
  const [riskProfile, setRiskProfile] = useState("Balanced");
  const [objectives, setObjectives] = useState("");
  const [sectors, setSectors] = useState<string[]>(["Technology", "Healthcare"]);
  
  // Recommendations list
  const [portfolio, setPortfolio] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
 
  const sectorOptions = ["Technology", "Healthcare", "Financials", "Energy", "Consumer Discretionary"];
 
  const fetchHistory = async () => {
    try {
      const data = await apiService.portfolio.getHistory();
      setHistory(data);
    } catch (_) {}
  };
 
  useEffect(() => {
    fetchHistory();
  }, []);
 
  const handleToggleSector = (s: string) => {
    if (sectors.includes(s)) {
      setSectors(prev => prev.filter(item => item !== s));
    } else {
      setSectors(prev => [...prev, s]);
    }
  };
 
  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiService.portfolio.generate({
        risk_profile: riskProfile,
        target_sectors: sectors,
        investment_objectives: objectives
      });
      setPortfolio(data);
      fetchHistory();
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
            Smart Investment Allocator
          </h1>
          <p className="text-sm text-gray-400 max-w-[700px]">
            Design a diversified investment allocation structured to balance risk, match your personal goals, and target specific market industries.
          </p>
        </div>
 
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Allocator Form panel */}
          <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-5 h-fit">
            <h2 className="text-base font-extrabold text-white pl-0.5">Configure Allocator Settings</h2>
            
            <form onSubmit={handleGenerate} className="space-y-5">
              <div>
                <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-2 pl-0.5">
                  Risk Tolerance Profile
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { label: "Low Risk", val: "Conservative" },
                    { label: "Balanced", val: "Balanced" },
                    { label: "High Growth", val: "Aggressive" }
                  ].map((item) => (
                    <button
                      type="button"
                      key={item.val}
                      onClick={() => setRiskProfile(item.val)}
                      className={`py-2 px-2.5 rounded-xl border text-[10px] font-extrabold uppercase tracking-wide transition-all ${
                        riskProfile === item.val
                          ? "bg-indigo-600 border-indigo-500/20 text-white shadow-md shadow-indigo-600/10 font-black"
                          : "bg-white/[0.015] border-white/[0.04] text-gray-400 hover:text-gray-200"
                      }`}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>
 
              <div>
                <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-2 pl-0.5">
                  Target Market Industries
                </label>
                <div className="flex flex-wrap gap-2 pt-0.5">
                  {sectorOptions.map((s) => {
                    const isSelected = sectors.includes(s);
                    return (
                      <button
                        type="button"
                        key={s}
                        onClick={() => handleToggleSector(s)}
                        className={`px-3 py-1.5 rounded-xl text-[10px] font-extrabold uppercase tracking-wider transition-all border ${
                          isSelected 
                            ? "bg-indigo-600/15 border-indigo-500/35 text-indigo-300"
                            : "bg-white/[0.015] border-white/[0.04] text-gray-400 hover:border-white/[0.08]"
                        }`}
                      >
                        {isSelected ? `✓ ${s}` : `+ ${s}`}
                      </button>
                    );
                  })}
                </div>
              </div>
 
              <div>
                <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-2 pl-0.5">
                  What are your primary investment goals?
                </label>
                <textarea
                  value={objectives}
                  onChange={(e) => setObjectives(e.target.value)}
                  rows={3}
                  className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200 placeholder-gray-600"
                  placeholder="E.g., Long-term wealth growth, keeping stable liquidity cash reserves..."
                />
              </div>
 
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all shadow-lg"
              >
                {loading ? "Re-optimizing Weights..." : "Optimize Investment Plan"}
              </button>
            </form>
          </div>
 
          {/* Allocation Results Panel */}
          <div className="lg:col-span-2 space-y-8">
            
            {portfolio ? (
              <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-6 animate-fade-in">
                <div className="flex justify-between items-center pb-3.5 border-b border-white/[0.04]">
                  <h3 className="font-extrabold text-white text-sm">Allocation Profile: {portfolio.risk_profile}</h3>
                  <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-[9px] font-extrabold uppercase tracking-wider">
                    <Sparkles className="w-3 h-3" />
                    <span>Optimized Plan</span>
                  </span>
                </div>
 
                {/* Explanation text */}
                <p className="text-xs leading-relaxed text-gray-400 bg-white/[0.01] p-4 rounded-2xl border border-white/[0.035]">
                  {portfolio.explanation}
                </p>
 
                {/* Dynamic Donut chart */}
                <div className="space-y-4 pt-1">
                  <h4 className="text-[9px] font-bold text-gray-500 uppercase tracking-widest pl-0.5">Asset Weight Distributions</h4>
                  <InteractiveChart type="donut" data={portfolio.allocations} />
                </div>
 
                <div className="text-[9px] text-gray-500 pl-0.5 font-medium italic border-t border-white/[0.04] pt-4">
                  * Advisory clause: {portfolio.financial_advisory_clause}
                </div>
              </div>
            ) : (
              <div className="h-72 border border-dashed border-white/[0.05] rounded-3xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                <PieChart className="w-8 h-8 text-gray-600 mb-2" />
                <p className="text-xs font-bold text-gray-400">Configure parameters & run optimization.</p>
                <p className="text-[9px] text-gray-500 mt-1 uppercase font-semibold">Your customized investment allocations chart will render here.</p>
              </div>
            )}
 
            {/* History Panel */}
            {history.length > 0 && (
              <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4">
                <h3 className="font-extrabold text-white text-sm pl-0.5">Allocation Run History</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-48 overflow-y-auto pr-1">
                  {history.map((h, idx) => (
                    <div 
                      key={idx} 
                      className="p-3.5 bg-white/[0.01] hover:bg-white/[0.02] border border-white/[0.03] rounded-2xl flex justify-between items-center transition-all group"
                    >
                      <div className="space-y-1">
                        <div className="font-extrabold text-xs text-gray-200">{h.risk_profile} Strategy</div>
                        <div className="flex items-center gap-1 text-[9px] text-gray-500 font-bold uppercase">
                          <Clock className="w-3 h-3" />
                          <span>{new Date(h.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      
                      <button 
                        onClick={() => setPortfolio(h)}
                        className="px-2.5 py-1.5 bg-indigo-500/10 hover:bg-indigo-500/25 border border-indigo-500/15 text-indigo-400 font-extrabold rounded-xl text-[9px] uppercase tracking-wide transition-colors flex items-center gap-1 group"
                      >
                        <span>View Plan</span>
                        <ChevronRight className="w-3 h-3 transition-transform duration-300 group-hover:translate-x-0.5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
 
          </div>
 
        </section>
 
      </main>
    </div>
  );
}

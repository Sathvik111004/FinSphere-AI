"use client";
 
import { useState } from "react";
import Sidebar from "../../../components/sidebar";
import HealthBadge from "../../../components/ui/HealthBadge";
import InteractiveChart from "../../../components/ui/InteractiveChart";
import { Activity, ShieldAlert, Sparkles, TrendingUp, AlertTriangle, RefreshCw, BarChart2, Eye, ShieldCheck, HelpCircle } from "lucide-react";
import { apiService } from "../../../services/api";
 
export default function AnalyticsPage() {
  const [activeTab, setActiveTab] = useState<"solvency" | "forecast" | "anomaly">("solvency");

  // Solvency States
  const [wc, setWc] = useState(45000000);
  const [re, setRe] = useState(120000000);
  const [ebit, setEbit] = useState(35000000);
  const [equity, setEquity] = useState(280000000);
  const [liabilities, setLiabilities] = useState(150000000);
  const [sales, setSales] = useState(400000000);
  const [assets, setAssets] = useState(500000000);
  const [riskRes, setRiskRes] = useState<any>(null);
 
  // Forecast States
  const [q1, setQ1] = useState(105.5);
  const [q2, setQ2] = useState(112.0);
  const [q3, setQ3] = useState(118.4);
  const [q4, setQ4] = useState(124.8);
  const [forecastRes, setForecastRes] = useState<any>(null);
 
  // Anomaly States
  const [margin, setMargin] = useState(-0.45);
  const [leverage, setLeverage] = useState(5.2);
  const [anomalyRes, setAnomalyRes] = useState<any>(null);
 
  // Loaders
  const [riskLoading, setRiskLoading] = useState(false);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [anomalyLoading, setAnomalyLoading] = useState(false);
 
  const handlePredictRisk = async (e: React.FormEvent) => {
    e.preventDefault();
    setRiskLoading(true);
    try {
      const data = await apiService.ml.predictRisk({
        working_capital: wc,
        retained_earnings: re,
        ebit,
        equity_market_val: equity,
        total_liabilities: liabilities,
        sales,
        total_assets: assets
      });
      setRiskRes(data);
    } catch (e: any) {
      alert(e.message);
    } finally {
      setRiskLoading(false);
    }
  };
 
  const handleForecast = async (e: React.FormEvent) => {
    e.preventDefault();
    setForecastLoading(true);
    try {
      const data = await apiService.ml.forecastRevenue([q1, q2, q3, q4]);
      setForecastRes(data);
    } catch (e: any) {
      alert(e.message);
    } finally {
      setForecastLoading(false);
    }
  };
 
  const handleAnomaly = async (e: React.FormEvent) => {
    e.preventDefault();
    setAnomalyLoading(true);
    try {
      const data = await apiService.ml.scanAnomalies(margin, leverage);
      setAnomalyRes(data);
    } catch (e: any) {
      alert(e.message);
    } finally {
      setAnomalyLoading(false);
    }
  };
 
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 pl-64 grid-dots pb-12">
      <Sidebar />
      
      <main className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
        
        {/* Header section */}
        <div className="space-y-2">
          <h1 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            Predictive Business Analytics
          </h1>
          <p className="text-sm text-gray-400 max-w-[750px]">
            Auditing tools powered by machine learning. Instantly assess business solvency zones, estimate revenue growth trends, and identify reporting discrepancies.
          </p>
        </div>

        {/* Dynamic Glass Tabs */}
        <div className="flex border-b border-white/[0.04] p-1.5 bg-white/[0.015] border border-white/[0.035] rounded-2xl w-fit gap-2">
          <button
            onClick={() => setActiveTab("solvency")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "solvency"
                ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            Business Health Check
          </button>
          <button
            onClick={() => setActiveTab("forecast")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "forecast"
                ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            Future Revenue Predictor
          </button>
          <button
            onClick={() => setActiveTab("anomaly")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "anomaly"
                ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            Accounting Error Scan
          </button>
        </div>
 
        <section className="grid grid-cols-1 gap-8">
          
          {/* solvency view */}
          {activeTab === "solvency" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-6">
                <div className="flex items-center gap-2.5">
                  <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl">
                    <ShieldAlert className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-base font-extrabold text-white">Business Health & Solvency Estimator</h2>
                    <p className="text-xs text-gray-500 mt-0.5">Calculates core stability scores to flag whether a company faces distress risks.</p>
                  </div>
                </div>
                
                <form onSubmit={handlePredictRisk} className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div className="relative group/field">
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Working Capital ($)</span>
                      <span title="Spare cash available for day-to-day operations">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={wc} onChange={(e) => setWc(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div>
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Retained Earnings ($)</span>
                      <span title="Total profits kept in the business over time">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={re} onChange={(e) => setRe(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div>
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Operating Profit - EBIT ($)</span>
                      <span title="Earnings earned before paying taxes and interest">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={ebit} onChange={(e) => setEbit(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div>
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Company Market Value ($)</span>
                      <span title="Total shares multiplied by current stock market price">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={equity} onChange={(e) => setEquity(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div>
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Total Liabilities ($)</span>
                      <span title="Total debt and money owed to other institutions">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={liabilities} onChange={(e) => setLiabilities(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div>
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Total Annual Sales ($)</span>
                      <span title="Total cash revenues from sales operations">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={sales} onChange={(e) => setSales(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
                  <div className="md:col-span-2">
                    <label className="flex items-center gap-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 pl-0.5">
                      <span>Total Assets Owned ($)</span>
                      <span title="Everything owned by the business (cash, inventory, property)">
                        <HelpCircle className="w-3 h-3 text-gray-600 hover:text-indigo-400 transition-colors cursor-pointer" />
                      </span>
                    </label>
                    <input type="number" value={assets} onChange={(e) => setAssets(Number(e.target.value))} className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                  </div>
 
                  <div className="md:col-span-2 pt-2">
                    <button
                      type="submit"
                      disabled={riskLoading}
                      className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all flex items-center justify-center gap-2"
                    >
                      {riskLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <span>Estimate Solvency Ratios</span>}
                    </button>
                  </div>
                </form>
              </div>

              {/* Solvency outputs */}
              <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] flex flex-col justify-center space-y-5">
                <h3 className="text-sm font-extrabold text-white pl-0.5 uppercase tracking-wider">Health Diagnostic Report</h3>
                {riskRes ? (
                  <div className="space-y-6 animate-fade-in">
                    <div className="p-4 rounded-2xl bg-white/[0.015] border border-white/[0.035] space-y-2">
                      <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wider">Estimated Solvency Level</span>
                      <div className="text-3xl font-extrabold text-indigo-300">{riskRes.altman_z_score.toFixed(2)}</div>
                      <div className="mt-1">
                        <HealthBadge status={riskRes.solvency_status} />
                      </div>
                    </div>
                    
                    <div className="p-4 rounded-2xl bg-white/[0.015] border border-white/[0.035] space-y-2">
                      <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wider">Bankruptcy Risk Indicator</span>
                      <div className="text-3xl font-extrabold text-emerald-400">{(riskRes.bankruptcy_probability * 100).toFixed(1)}%</div>
                      <p className="text-[10px] leading-relaxed text-gray-400 font-medium">
                        Machine Learning predicts this company is **{riskRes.bankruptcy_prediction_label}** over the next 24 months.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="h-56 border border-dashed border-white/[0.05] rounded-2xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                    <ShieldCheck className="w-8 h-8 text-gray-600 mb-2" />
                    <p className="text-xs font-bold text-gray-400">Input balance variables.</p>
                    <p className="text-[9px] text-gray-500 mt-1 uppercase font-semibold">Solvency zone diagnostic metrics will output here.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* forecast view */}
          {activeTab === "forecast" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-5 h-fit">
                <div className="flex items-center gap-2.5">
                  <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
                    <TrendingUp className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-base font-extrabold text-white">Future Revenue Predictor</h2>
                    <p className="text-xs text-gray-500 mt-0.5">Fits regularized time models to historical values to project next quarter revenue.</p>
                  </div>
                </div>
                
                <form onSubmit={handleForecast} className="space-y-4">
                  <div className="grid grid-cols-2 gap-3.5">
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Quarter 1 ($M)</label>
                      <input type="number" step="0.1" value={q1} onChange={(e) => setQ1(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Quarter 2 ($M)</label>
                      <input type="number" step="0.1" value={q2} onChange={(e) => setQ2(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Quarter 3 ($M)</label>
                      <input type="number" step="0.1" value={q3} onChange={(e) => setQ3(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Quarter 4 ($M)</label>
                      <input type="number" step="0.1" value={q4} onChange={(e) => setQ4(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                  </div>
 
                  <button
                    type="submit"
                    disabled={forecastLoading}
                    className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all"
                  >
                    {forecastLoading ? "Executing Forecast..." : "Project Q5 Growth"}
                  </button>
                </form>
              </div>

              <div className="lg:col-span-2 glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-6">
                <h3 className="text-sm font-extrabold text-white pl-0.5 uppercase tracking-wider">Revenue Trend Visualization</h3>
                {forecastRes ? (
                  <div className="space-y-6 animate-fade-in">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3.5 rounded-2xl bg-white/[0.015] border border-white/[0.035]">
                        <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wide">Q5 Revenue Forecast</span>
                        <div className="text-2xl font-extrabold text-emerald-400">${forecastRes.forecasted_revenue.toFixed(1)}M</div>
                      </div>
                      <div className="p-3.5 rounded-2xl bg-white/[0.015] border border-white/[0.035]">
                        <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wide">Trend Direction</span>
                        <div className="text-base font-extrabold text-gray-200 uppercase mt-0.5">{forecastRes.trend_direction}</div>
                      </div>
                    </div>

                    <InteractiveChart 
                      type="area" 
                      data={[
                        { name: "Q1", value: q1 },
                        { name: "Q2", value: q2 },
                        { name: "Q3", value: q3 },
                        { name: "Q4", value: q4 },
                        { name: "Q5 Proj", value: forecastRes.forecasted_revenue }
                      ]} 
                    />
                  </div>
                ) : (
                  <div className="h-64 border border-dashed border-white/[0.05] rounded-2xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                    <BarChart2 className="w-8 h-8 text-gray-600 mb-2" />
                    <p className="text-xs font-bold text-gray-400">Configure quarters parameters & run projection.</p>
                    <p className="text-[9px] text-gray-500 mt-1 uppercase font-semibold">Interactive gradient growth Area chart will render here.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* anomaly view */}
          {activeTab === "anomaly" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-5 h-fit">
                <div className="flex items-center gap-2.5">
                  <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 text-purple-400 rounded-xl">
                    <Activity className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-base font-extrabold text-white">Accounting Error Scan</h2>
                    <p className="text-xs text-gray-500 mt-0.5">Scrapes for outliers and structural accounting irregularities.</p>
                  </div>
                </div>
                
                <form onSubmit={handleAnomaly} className="space-y-4">
                  <div className="grid grid-cols-2 gap-3.5">
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Operating Margin</label>
                      <input type="number" step="0.01" value={margin} onChange={(e) => setMargin(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                    <div>
                      <label className="block text-[9px] font-bold text-gray-500 uppercase tracking-wider mb-1.5 pl-0.5">Leverage Ratio</label>
                      <input type="number" step="0.1" value={leverage} onChange={(e) => setLeverage(Number(e.target.value))} className="w-full px-3 py-2 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200" />
                    </div>
                  </div>
 
                  <button
                    type="submit"
                    disabled={anomalyLoading}
                    className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all"
                  >
                    {anomalyLoading ? "Executing Diagnostics..." : "Execute Outliers Scan"}
                  </button>
                </form>
              </div>

              <div className="lg:col-span-2 glass-panel-premium p-6 rounded-3xl border border-white/[0.04] flex flex-col justify-center space-y-4">
                <h3 className="text-sm font-extrabold text-white pl-0.5 uppercase tracking-wider">Outliers Assessment Report</h3>
                {anomalyRes ? (
                  <div className={`p-5 border rounded-2xl animate-fade-in space-y-3.5 ${
                    anomalyRes.is_anomaly 
                      ? "bg-red-500/10 border-red-500/25 text-red-300"
                      : "bg-white/[0.015] border-white/[0.035] text-gray-300"
                  }`}>
                    <div className="flex items-center gap-2">
                      <HealthBadge status={anomalyRes.is_anomaly ? "Anomaly Flagged" : "Balanced Distribution"} />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-1">Audit Diagnostic Summary:</h4>
                      <p className="text-xs leading-relaxed text-gray-400">{anomalyRes.reasoning}</p>
                    </div>
                  </div>
                ) : (
                  <div className="h-56 border border-dashed border-white/[0.05] rounded-2xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                    <Eye className="w-8 h-8 text-gray-600 mb-2" />
                    <p className="text-xs font-bold text-gray-400">Run diagnostic outlier check.</p>
                    <p className="text-[9px] text-gray-500 mt-1 uppercase font-semibold">Isolation Forest outlier scores will render here.</p>
                  </div>
                )}
              </div>
            </div>
          )}
 
        </section>
 
      </main>
    </div>
  );
}

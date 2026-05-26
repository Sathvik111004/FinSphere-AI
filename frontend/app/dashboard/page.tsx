"use client";
 
import { useEffect, useState } from "react";
import Link from "next/link";
import Sidebar from "../../components/sidebar";
import DashboardCard from "../../components/ui/DashboardCard";
import { 
  FolderLock, 
  TrendingUp, 
  Activity, 
  ShieldAlert, 
  FileText,
  ChevronRight,
  Sparkles,
  ShieldCheck,
  Cpu
} from "lucide-react";
import { apiService } from "../../services/api";
 
export default function DashboardHome() {
  const [user, setUser] = useState<any>(null);
  const [docsCount, setDocsCount] = useState(0);
  const [portfolioCount, setPortfolioCount] = useState(0);
  const [loading, setLoading] = useState(true);
 
  useEffect(() => {
    // Authenticate and pull quick stats
    Promise.all([
      apiService.auth.getMe(),
      apiService.documents.list(),
      apiService.portfolio.getHistory()
    ]).then(([uRes, dRes, pRes]) => {
      setUser(uRes);
      setDocsCount(dRes.length);
      setPortfolioCount(pRes.length);
    }).catch(() => {
      // Handled globally
    }).finally(() => {
      setLoading(false);
    });
  }, []);
 
  if (loading) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-[#0B0F19]">
        <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-indigo-500/10 border-t-indigo-500" />
      </div>
    );
  }
 
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 pl-64 grid-dots pb-12">
      <Sidebar />
      
      <main className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
        
        {/* Welcome Header banner */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center bg-gradient-to-r from-indigo-950/45 via-purple-950/15 to-transparent p-7 rounded-3xl border border-white/[0.04] backdrop-blur-xl relative overflow-hidden shadow-2xl">
          <div className="absolute w-[250px] h-[250px] bg-indigo-500/5 rounded-full blur-[70px] -top-10 -left-10 pointer-events-none" />
          
          <div className="space-y-2 z-10">
            <h1 className="text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
              Welcome back, <span className="bg-gradient-to-r from-indigo-200 via-purple-300 to-emerald-200 bg-clip-text text-transparent">{user?.email || "Analyst"}</span>
            </h1>
            <p className="text-sm text-gray-400 max-w-[620px] leading-relaxed">
              Your autonomous financial workspace is online. Review business health scores, forecast future operational revenues, or analyze corporate transcripts securely.
            </p>
          </div>
          
          <div className="mt-4 md:mt-0 flex items-center gap-2.5 px-4 py-2.5 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-wider shadow-inner z-10 animate-pulse">
            <Sparkles className="w-4 h-4" />
            <span>Workspace Active</span>
          </div>
        </header>
 
        {/* Stats Grid panel */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <DashboardCard
            title="Uploaded Reports"
            value={docsCount}
            description="Active filings in database"
            icon={FileText}
            color="text-indigo-400"
            trend={{ value: "Secure Store", isPositive: true }}
          />
          <DashboardCard
            title="Risk Audits Run"
            value={portfolioCount}
            description="Stored history allocations"
            icon={TrendingUp}
            color="text-emerald-400"
            trend={{ value: "Updated", isPositive: true }}
          />
          <DashboardCard
            title="Predictive Models"
            value="3 Active"
            description="RF, Ridge, Isolation Forest"
            icon={Cpu}
            color="text-purple-400"
            trend={{ value: "Live Models", isNeutral: true }}
          />
          <DashboardCard
            title="Workspace Shield"
            value="Enterprise"
            description="Secure session protection"
            icon={ShieldAlert}
            color="text-amber-400"
            trend={{ value: "Protected", isPositive: true }}
          />
        </section>
 
        {/* Action Center portal */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Quick Actions Panel */}
          <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4">
            <h2 className="text-base font-extrabold text-white pl-0.5">Quick Operations</h2>
            <div className="grid grid-cols-1 gap-3.5">
              <Link 
                href="/dashboard/upload" 
                className="flex items-center justify-between p-4 bg-white/[0.01] hover:bg-indigo-500/5 rounded-2xl border border-white/[0.03] hover:border-indigo-500/20 transition-all duration-300 group text-xs font-bold text-gray-200 uppercase tracking-wide"
              >
                <span>Upload Financial Files</span>
                <ChevronRight className="w-4 h-4 text-gray-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
              </Link>
              
              <Link 
                href="/dashboard/chat" 
                className="flex items-center justify-between p-4 bg-white/[0.01] hover:bg-purple-500/5 rounded-2xl border border-white/[0.03] hover:border-purple-500/20 transition-all duration-300 group text-xs font-bold text-gray-200 uppercase tracking-wide"
              >
                <span>AI Financial Copilot</span>
                <ChevronRight className="w-4 h-4 text-gray-500 group-hover:text-purple-400 group-hover:translate-x-1 transition-all" />
              </Link>
              
              <Link 
                href="/dashboard/analytics" 
                className="flex items-center justify-between p-4 bg-white/[0.01] hover:bg-emerald-500/5 rounded-2xl border border-white/[0.03] hover:border-emerald-500/20 transition-all duration-300 group text-xs font-bold text-gray-200 uppercase tracking-wide"
              >
                <span>Business Health Checker</span>
                <ChevronRight className="w-4 h-4 text-gray-500 group-hover:text-emerald-400 group-hover:translate-x-1 transition-all" />
              </Link>
            </div>
          </div>
 
          {/* Model Status Card */}
          <div className="lg:col-span-2 glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4">
            <h2 className="text-base font-extrabold text-white pl-0.5">Corporate Predictive Engines</h2>
            <div className="space-y-3.5">
              
              <div className="p-4 rounded-2xl bg-white/[0.01] border border-white/[0.03] hover:border-white/[0.06] transition-colors flex justify-between items-center text-xs">
                <div>
                  <h3 className="font-extrabold text-gray-200 text-sm">Business Solvency Predictor</h3>
                  <p className="text-gray-500 mt-1">Evaluates business stability ratios to flag default or distress zones.</p>
                </div>
                <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-extrabold uppercase tracking-wide">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Online</span>
                </span>
              </div>
              
              <div className="p-4 rounded-2xl bg-white/[0.01] border border-white/[0.03] hover:border-white/[0.06] transition-colors flex justify-between items-center text-xs">
                <div>
                  <h3 className="font-extrabold text-gray-200 text-sm">Future Revenue Forecaster</h3>
                  <p className="text-gray-500 mt-1">Analyzes historical quarters to model growth trajectories.</p>
                </div>
                <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-extrabold uppercase tracking-wide">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Online</span>
                </span>
              </div>
              
              <div className="p-4 rounded-2xl bg-white/[0.01] border border-white/[0.03] hover:border-white/[0.06] transition-colors flex justify-between items-center text-xs">
                <div>
                  <h3 className="font-extrabold text-gray-200 text-sm">Accounting Error Detector</h3>
                  <p className="text-gray-500 mt-1">Scans leverage and margin imbalances for anomalies or reporting errors.</p>
                </div>
                <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-extrabold uppercase tracking-wide">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Online</span>
                </span>
              </div>
 
            </div>
          </div>
 
        </section>
 
      </main>
    </div>
  );
}

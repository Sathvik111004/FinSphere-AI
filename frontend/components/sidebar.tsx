"use client";
 
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  LayoutDashboard, 
  UploadCloud, 
  MessageSquare, 
  TrendingUp, 
  PieChart, 
  Activity, 
  LogOut,
  FolderLock,
  Sparkles
} from "lucide-react";
import { apiService } from "../services/api";
 
export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
 
  const menuItems = [
    { name: "Overview", icon: LayoutDashboard, path: "/dashboard" },
    { name: "Uploaded Reports", icon: UploadCloud, path: "/dashboard/upload" },
    { name: "AI Financial Copilot", icon: MessageSquare, path: "/dashboard/chat" },
    { name: "Business Health", icon: Activity, path: "/dashboard/analytics" },
    { name: "Smart Allocator", icon: PieChart, path: "/dashboard/portfolio" },
    { name: "Earnings Tone Scan", icon: TrendingUp, path: "/dashboard/earnings" },
  ];
 
  const handleLogout = async () => {
    try {
      await apiService.auth.logout();
      router.push("/login");
    } catch (e) {
      router.push("/login");
    }
  };
 
  return (
    <aside className="w-64 h-screen fixed left-0 top-0 bg-gray-950/75 backdrop-blur-xl border-r border-white/[0.04] flex flex-col justify-between p-5 z-40 shadow-[4px_0_30px_rgba(0,0,0,0.5)]">
      <div className="space-y-6">
        {/* Brand logo container */}
        <div className="flex items-center gap-3 px-2.5 py-2">
          <div className="p-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 shadow-inner animate-float">
            <FolderLock className="w-5.5 h-5.5" />
          </div>
          <div>
            <h1 className="text-base font-extrabold tracking-tight bg-gradient-to-r from-indigo-300 via-purple-300 to-emerald-300 bg-clip-text text-transparent flex items-center gap-1">
              FinSphere AI
            </h1>
            <p className="text-[9px] text-gray-500 tracking-wider font-bold uppercase">
              Financial Intelligence
            </p>
          </div>
        </div>
 
        {/* Navigation list */}
        <nav className="space-y-1.5">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.path;
            
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold tracking-wide transition-all duration-300 group border ${
                  isActive 
                    ? "bg-indigo-500/10 border-indigo-500/25 text-indigo-300 neon-glow-primary font-bold shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]"
                    : "text-gray-400 hover:bg-white/[0.02] hover:text-gray-200 border-transparent hover:border-white/[0.02] hover:shadow-[0_4px_12px_-5px_rgba(0,0,0,0.3)]"
                }`}
              >
                <Icon className={`w-4 h-4 transition-all duration-300 group-hover:scale-110 ${
                  isActive ? "text-indigo-400 filter drop-shadow-[0_0_8px_rgba(99,102,241,0.5)]" : "text-gray-500 group-hover:text-gray-300"
                }`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
 
      {/* Footer / User controls */}
      <div className="space-y-4">
        {/* Sandbox status indicator */}
        <div className="p-3 bg-white/[0.015] border border-white/[0.035] rounded-xl flex items-center gap-2 text-[10px] text-gray-500 font-bold uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400/80 shrink-0" />
          <span>Auditor Workspace</span>
        </div>

        <div className="border-t border-white/[0.04] pt-4">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold tracking-wide text-gray-400 hover:bg-red-500/10 hover:text-red-400 border border-transparent hover:border-red-500/15 transition-all duration-300"
          >
            <LogOut className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-0.5" />
            <span>Sign Out Workspace</span>
          </button>
        </div>
      </div>
    </aside>
  );
}

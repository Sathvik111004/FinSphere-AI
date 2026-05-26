"use client";

import { LucideIcon } from "lucide-react";

interface DashboardCardProps {
  title: string;
  value: string | number;
  description: string;
  icon: LucideIcon;
  color?: string;
  trend?: {
    value: string;
    isPositive?: boolean;
    isNeutral?: boolean;
  };
}

export default function DashboardCard({
  title,
  value,
  description,
  icon: Icon,
  color = "text-indigo-400",
  trend
}: DashboardCardProps) {
  return (
    <div className="glass-panel-premium p-6 rounded-2xl border border-white/[0.04] flex justify-between items-start transition-all duration-300 relative overflow-hidden group">
      {/* Decorative inner glow hover element */}
      <div className="absolute -inset-px bg-gradient-to-r from-indigo-500/10 to-purple-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <div className="space-y-3 z-10">
        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest block pl-0.5">
          {title}
        </span>
        <div className="text-3xl font-extrabold tracking-tight text-white group-hover:text-indigo-50 transition-colors">
          {value}
        </div>
        
        <div className="flex items-center gap-2">
          {trend && (
            <span className={`px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase tracking-wide shrink-0 ${
              trend.isPositive
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/15"
                : trend.isNeutral
                ? "bg-gray-500/10 text-gray-400 border border-gray-500/15"
                : "bg-red-500/10 text-red-400 border border-red-500/15"
            }`}>
              {trend.value}
            </span>
          )}
          <p className="text-xs text-gray-400 font-medium truncate max-w-[150px] md:max-w-[200px]" title={description}>
            {description}
          </p>
        </div>
      </div>

      <div className={`p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] group-hover:border-indigo-500/20 group-hover:bg-indigo-500/5 transition-all duration-300 ${color} z-10`}>
        <Icon className="w-5 h-5 transition-transform duration-500 group-hover:scale-110" />
      </div>
    </div>
  );
}

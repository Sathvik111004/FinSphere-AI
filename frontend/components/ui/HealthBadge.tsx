"use client";

import { ShieldCheck, ShieldAlert, Shield } from "lucide-react";

interface HealthBadgeProps {
  status: string;
}

export default function HealthBadge({ status }: HealthBadgeProps) {
  const normStatus = status.toLowerCase();

  const isSafe = normStatus.includes("safe") || normStatus.includes("stable") || normStatus.includes("balanced");
  const isDistress = normStatus.includes("distress") || normStatus.includes("anomaly") || normStatus.includes("high risk");
  
  if (isSafe) {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-[10px] font-extrabold uppercase tracking-wider animate-pulse-glow-emerald shadow-inner">
        <ShieldCheck className="w-3.5 h-3.5 filter drop-shadow-[0_0_4px_rgba(16,185,129,0.3)]" />
        <span>{status}</span>
      </span>
    );
  }

  if (isDistress) {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/25 text-red-400 text-[10px] font-extrabold uppercase tracking-wider animate-pulse-glow-red shadow-inner">
        <ShieldAlert className="w-3.5 h-3.5 filter drop-shadow-[0_0_4px_rgba(239,68,68,0.3)]" />
        <span>{status}</span>
      </span>
    );
  }

  // Gray / Caution / Neutral
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/25 text-amber-400 text-[10px] font-extrabold uppercase tracking-wider shadow-inner">
      <Shield className="w-3.5 h-3.5 filter drop-shadow-[0_0_4px_rgba(245,158,11,0.3)]" />
      <span>{status}</span>
    </span>
  );
}

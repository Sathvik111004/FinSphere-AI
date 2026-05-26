"use client";

import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

interface InteractiveChartProps {
  type: "area" | "donut";
  data: any[];
  dataKeys?: string[];
  colors?: string[];
}

export default function InteractiveChart({
  type,
  data,
  dataKeys = ["value"],
  colors = ["#6366F1", "#10B981", "#8B5CF6", "#F55F88", "#F59E0B"]
}: InteractiveChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-full h-64 bg-white/[0.01] border border-white/[0.03] rounded-2xl flex items-center justify-center animate-pulse">
        <div className="text-xs text-gray-500 font-semibold tracking-wider uppercase">Loading interactive visualization...</div>
      </div>
    );
  }

  // --- AREA CHART IMPLEMENTATION (Revenue Projections) ---
  if (type === "area") {
    return (
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366F1" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="name" 
              stroke="#4B5563" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false} 
              dy={10} 
            />
            <YAxis 
              stroke="#4B5563" 
              fontSize={10} 
              tickLine={false} 
              axisLine={false} 
              dx={-5}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(10, 14, 26, 0.9)",
                borderColor: "rgba(255, 255, 255, 0.08)",
                borderRadius: "12px",
                fontSize: "11px",
                color: "#F3F4F6",
                boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
              }}
              labelStyle={{ fontWeight: "bold", color: "#8B5CF6", marginBottom: "4px" }}
            />
            <Area
              type="monotone"
              dataKey={dataKeys[0]}
              stroke="#6366F1"
              strokeWidth={2.5}
              fillOpacity={1}
              fill="url(#areaGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }

  // --- DONUT PIE CHART IMPLEMENTATION (Asset Allocation Weights) ---
  const transformedPieData = data.map((item, idx) => ({
    name: item.asset || item.name || `Asset ${idx}`,
    value: item.weight || item.value || 0,
    color: item.color || colors[idx % colors.length]
  }));

  return (
    <div className="w-full h-64 flex flex-col md:flex-row items-center justify-between gap-6">
      <div className="flex-1 w-full h-48 md:h-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={transformedPieData}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={75}
              paddingAngle={4}
              dataKey="value"
            >
              {transformedPieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} stroke="rgba(10, 14, 26, 0.8)" strokeWidth={2} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(10, 14, 26, 0.9)",
                borderColor: "rgba(255, 255, 255, 0.08)",
                borderRadius: "12px",
                fontSize: "11px",
                color: "#F3F4F6",
                boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
              }}
              formatter={(val) => [`${val}%`, "Weight"]}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Premium Glassmorphic Legend */}
      <div className="flex-1 w-full space-y-2 md:max-h-48 overflow-y-auto pr-1">
        {transformedPieData.map((entry, index) => (
          <div key={index} className="flex justify-between items-center p-2 rounded-xl bg-white/[0.015] border border-white/[0.035] text-[11px] font-semibold tracking-wide">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: entry.color }} />
              <span className="text-gray-300 truncate max-w-[120px]">{entry.name}</span>
            </div>
            <span className="text-indigo-400 font-bold">{entry.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

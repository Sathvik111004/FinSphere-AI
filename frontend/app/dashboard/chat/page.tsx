"use client";
 
import { useState, useRef, useEffect } from "react";
import Sidebar from "../../../components/sidebar";
import { MessageSquare, Send, Sparkles, HelpCircle, ChevronDown, ChevronUp, FileText, Bot, User } from "lucide-react";
import { apiService } from "../../../services/api";
import DOMPurify from "dompurify";

function renderMarkdown(text: string) {
  if (!text) return "";

  // 1. Escape HTML characters to prevent XSS
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // 2. Headers
  html = html
    .replace(/^### (.*?)$/gm, '<h3 class="text-xs font-extrabold text-white mt-3 mb-1.5">$1</h3>')
    .replace(/^#### (.*?)$/gm, '<h4 class="text-[10px] font-bold text-indigo-300 mt-2 mb-1">$1</h4>')
    .replace(/^## (.*?)$/gm, '<h2 class="text-sm font-black text-white mt-4 mb-2">$1</h2>')
    .replace(/^# (.*?)$/gm, '<h1 class="text-base font-black text-white mt-5 mb-2.5">$1</h1>');

  // 3. Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-extrabold text-indigo-300">$1</strong>');

  // 4. Italics
  html = html.replace(/\*(.*?)\*/g, '<em class="text-gray-300 italic">$1</em>');

  // 5. Bullet points
  html = html.replace(/^\s*[-*•]\s+(.*?)$/gm, '<li class="ml-4 list-disc pl-1 mb-1 text-gray-300">$1</li>');

  // Wrap contiguous <li> groups in <ul>
  const lines = html.split("\n");
  let inList = false;
  const processedLines = [];

  for (let line of lines) {
    if (line.trim().startsWith("<li")) {
      if (!inList) {
        processedLines.push('<ul class="space-y-1.5 my-2">');
        inList = true;
      }
      processedLines.push(line);
    } else {
      if (inList) {
        processedLines.push('</ul>');
        inList = false;
      }
      processedLines.push(line);
    }
  }
  if (inList) {
    processedLines.push('</ul>');
  }

  return processedLines.join("\n");
}
 
export default function AnalystChatPage() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [reasoningOpen, setReasoningOpen] = useState<Record<number, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);
 
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
 
  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);
 
  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || loading) return;
 
    const userMsg = { role: "user", content: prompt };
    setMessages(prev => [...prev, userMsg]);
    const activePrompt = prompt;
    setPrompt("");
    setLoading(true);
 
    try {
      // Map prior messages into standard roles structure
      const chatHistory = messages.map(m => ({
        role: m.role,
        content: m.content
      }));
      
      const res = await apiService.analyst.runTask(activePrompt, chatHistory);
      
      const agentMsg = {
        role: "assistant",
        content: res.output,
        reasoning: res.reasoning_steps
      };
      
      setMessages(prev => [...prev, agentMsg]);
    } catch (e: any) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: `Copilot warning: ${e.message || "Failed to finalize agent execution."}`,
        reasoning: ["Execution failed at coordinator boundary."]
      }]);
    } finally {
      setLoading(false);
    }
  };
 
  const toggleReasoning = (idx: number) => {
    setReasoningOpen(prev => ({
      ...prev,
      [idx]: !prev[idx]
    }));
  };
 
  const sampleQueries = [
    "Run bankruptcy risk calculations for our balance sheet.",
    "Evaluate revenue growth trajectory and project next-quarter performance.",
    "Identify major risk factors in the uploaded annual report."
  ];
 
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 pl-64 grid-dots">
      <Sidebar />
      
      <main className="h-screen flex flex-col max-w-5xl mx-auto p-6 relative">
        
        {/* Header workspace info */}
        <div className="pb-4 border-b border-white/[0.04] flex justify-between items-center shrink-0">
          <div>
            <h1 className="text-xl font-extrabold text-white flex items-center gap-2">
              AI Financial Copilot Workspace
            </h1>
            <p className="text-xs text-gray-400">
              Ask your copilot to fetch financial files, check solvency metrics, or analyze balance sheets.
            </p>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-[10px] font-bold uppercase tracking-wider shadow-inner">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI Copilot Active</span>
          </div>
        </div>
 
        {/* Chat message history container */}
        <div className="flex-1 overflow-y-auto py-6 space-y-6 min-h-0 pr-1">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col justify-center items-center text-center p-8 max-w-lg mx-auto space-y-6">
              <div className="p-4 rounded-3xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 shadow-xl animate-float">
                <MessageSquare className="w-9 h-9" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-bold text-white">Chat with your AI Financial Copilot</h3>
                <p className="text-xs text-gray-400 leading-relaxed max-w-[380px]">
                  Your copilot can access document libraries, calculate business health scores, and project future revenues. Get started with a question or use a sample query:
                </p>
              </div>
              
              <div className="grid grid-cols-1 gap-2.5 w-full text-left pt-2">
                {sampleQueries.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setPrompt(q)}
                    className="p-3.5 bg-white/[0.01] hover:bg-indigo-500/5 rounded-2xl border border-white/[0.03] hover:border-indigo-500/25 transition-all text-xs font-bold text-gray-300 flex items-center gap-2.5 group"
                  >
                    <HelpCircle className="w-4 h-4 text-indigo-400 shrink-0" />
                    <span className="truncate">{q}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => {
                const isUser = msg.role === "user";
                return (
                  <div 
                    key={i} 
                    className={`flex gap-4 ${isUser ? "justify-end animate-fade-in" : "animate-fade-in"}`}
                  >
                    {!isUser && (
                      <div className="p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 shadow-inner shrink-0 h-fit">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}
                    
                    <div className={`space-y-3 max-w-[80%] ${isUser ? "order-1" : "order-2"}`}>
                      {/* Message bubble card */}
                      {isUser ? (
                        <div className="p-4 rounded-2xl border text-xs leading-relaxed whitespace-pre-wrap bg-indigo-600 border-indigo-500/25 text-white rounded-tr-none shadow-lg shadow-indigo-600/10">
                          {msg.content}
                        </div>
                      ) : (
                        <div 
                          className="p-4 rounded-2xl border text-xs leading-relaxed glass-panel-premium text-gray-200 border-white/[0.04] rounded-tl-none"
                          dangerouslySetInnerHTML={{ __html: typeof window !== "undefined" ? DOMPurify.sanitize(renderMarkdown(msg.content)) : msg.content }}
                        />
                      )}
                      
                      {/* Collapsible details for Agent Reasoning steps */}
                      {!isUser && msg.reasoning && msg.reasoning.length > 0 && (
                        <div className="glass-panel-premium border border-white/[0.04] rounded-2xl overflow-hidden text-[10px]">
                          <button
                            onClick={() => toggleReasoning(i)}
                            className="w-full flex items-center justify-between px-3.5 py-2 bg-white/[0.015] text-gray-400 hover:text-gray-200 transition-colors font-bold uppercase tracking-wider"
                          >
                            <span>
                              Copilot Thinking Process ({msg.reasoning.length} Steps)
                            </span>
                            {reasoningOpen[i] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                          </button>
                          
                          {reasoningOpen[i] && (
                            <div className="p-3.5 bg-gray-950/60 border-t border-white/[0.04] space-y-1.5 text-gray-500 font-mono text-[9px] max-h-48 overflow-y-auto">
                              {msg.reasoning.map((step: string, sIdx: number) => (
                                <div key={sIdx} className="flex gap-2">
                                  <span className="text-indigo-400 font-bold">[{sIdx + 1}]</span>
                                  <span>{step}</span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {isUser && (
                      <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.05] text-gray-400 shadow-inner shrink-0 h-fit order-2">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                );
              })}
              
              {loading && (
                <div className="flex gap-4 animate-pulse">
                  <div className="p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/10 text-indigo-500 shrink-0 h-fit animate-spin">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div className="space-y-2.5 w-full max-w-[400px]">
                    <div className="h-10 bg-white/[0.01] border border-white/[0.035] rounded-2xl" />
                    <div className="h-3.5 bg-white/[0.005] border border-transparent rounded-lg w-[70%]" />
                  </div>
                </div>
              )}
              
              <div ref={scrollToBottom} />
            </div>
          )}
        </div>
 
        {/* Input box bottom bar */}
        <form onSubmit={handleSend} className="pt-4 border-t border-white/[0.04] shrink-0 flex gap-3">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={loading}
            required
            placeholder="Ask your copilot a question..."
            className="flex-1 px-4 py-3 bg-gray-900/60 border border-white/[0.06] rounded-2xl text-xs text-gray-200 placeholder-gray-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !prompt.trim()}
            className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:bg-gray-800 disabled:text-gray-500 text-white rounded-2xl font-bold text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2 shadow-lg shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
 
      </main>
    </div>
  );
}

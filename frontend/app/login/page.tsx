"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { FolderLock, AlertCircle, Sparkles } from "lucide-react";
import { apiService } from "../../services/api";

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(false);
  
  // Form fields
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  // Status states
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");
    setSuccessMsg("");
    setLoading(true);

    if (isSignUp && password.length < 12) {
      setErrorMsg("Password must be at least 12 characters long.");
      setLoading(false);
      return;
    }

    try {
      if (isSignUp) {
        // Run registration
        await apiService.auth.signup({ email, password, role: "analyst" });
        setSuccessMsg("Account created! Please sign in.");
        setIsSignUp(false);
        setPassword("");
      } else {
        // Run login which issues cookie
        await apiService.auth.login({ email, password });
        router.push("/dashboard");
      }
    } catch (e: any) {
      setErrorMsg(e.message || "Authentication process failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen w-screen items-center justify-center p-4 bg-background overflow-hidden relative">
      {/* Background neon glows */}
      <div className="absolute w-[400px] h-[400px] bg-indigo-500/10 rounded-full blur-[100px] -top-20 -left-20 pointer-events-none" />
      <div className="absolute w-[450px] h-[450px] bg-emerald-500/8 rounded-full blur-[120px] -bottom-30 -right-20 pointer-events-none" />
      
      <div className="w-full max-w-[420px] glass-panel rounded-2xl p-8 neon-glow-primary border border-gray-800 animate-fade-in relative z-10">
        
        {/* Logo and Brand Header */}
        <div className="flex flex-col items-center text-center mb-6">
          <div className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/25 text-indigo-400 mb-3 shadow-inner">
            <FolderLock className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-200 via-purple-300 to-emerald-200 bg-clip-text text-transparent">
            {isSignUp ? "Create Workspace Account" : "Access FinSphere AI"}
          </h1>
          <p className="text-xs text-gray-400 mt-1 max-w-[300px]">
            {isSignUp 
              ? "Establish high-security intelligence and quantitative risk credentials" 
              : "Autonomous financial risk decision system"
            }
          </p>
        </div>

        {/* Error notification */}
        {errorMsg && (
          <div className="mb-4 flex items-center gap-2.5 p-3 rounded-lg bg-red-500/15 border border-red-500/30 text-red-300 text-xs animate-fade-in">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <p>{errorMsg}</p>
          </div>
        )}

        {/* Success notification */}
        {successMsg && (
          <div className="mb-4 flex items-center gap-2.5 p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs animate-fade-in">
            <Sparkles className="w-4 h-4 shrink-0" />
            <p>{successMsg}</p>
          </div>
        )}

        {/* Form fields */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5 pl-0.5">
              Secure Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2.5 bg-gray-900/60 border border-gray-800 rounded-lg text-sm text-gray-100 placeholder-gray-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              placeholder="name@organization.com"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5 pl-0.5">
              Security Signature Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2.5 bg-gray-900/60 border border-gray-800 rounded-lg text-sm text-gray-100 placeholder-gray-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              placeholder="••••••••••••"
            />
            {isSignUp && (
              <p className="text-[10px] text-gray-500 mt-1 pl-0.5 font-medium">
                * Requires minimum of 12 robust characters.
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white rounded-lg text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 neon-glow-primary"
          >
            {loading ? (
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-white/20 border-t-white" />
            ) : (
              <span>{isSignUp ? "Provision Account" : "Open System Terminal"}</span>
            )}
          </button>
        </form>

        {/* Toggle link */}
        <div className="mt-5 text-center text-xs">
          <button
            onClick={() => {
              setIsSignUp(!isSignUp);
              setErrorMsg("");
              setSuccessMsg("");
            }}
            className="text-gray-400 hover:text-indigo-400 font-medium underline underline-offset-4 decoration-indigo-500/40 transition-colors"
          >
            {isSignUp ? "Already registered? Sign In" : "Need credentials? Sign Up"}
          </button>
        </div>
      </div>
    </main>
  );
}

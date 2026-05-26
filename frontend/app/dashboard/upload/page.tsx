"use client";
 
import { useEffect, useState } from "react";
import Sidebar from "../../../components/sidebar";
import { UploadCloud, FileText, Trash2, AlertCircle, CheckCircle2, ShieldCheck, HelpCircle } from "lucide-react";
import { apiService } from "../../../services/api";
 
export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [docType, setDocType] = useState("annual_report");
  const [documents, setDocuments] = useState<any[]>([]);
  
  // Status states
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  
  const [dragActive, setDragActive] = useState(false);

  const fetchDocs = async () => {
    try {
      const data = await apiService.documents.list();
      setDocuments(data);
    } catch (_) {}
  };
 
  useEffect(() => {
    fetchDocs();
  }, []);
 
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };
 
  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    setErrorMsg("");
    setSuccessMsg("");
 
    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_type", docType);
 
    try {
      await apiService.documents.upload(formData);
      setSuccessMsg("Your file was parsed and successfully indexed!");
      setFile(null);
      fetchDocs();
    } catch (e: any) {
      setErrorMsg(e.message || "Failed to process document file.");
    } finally {
      setLoading(false);
    }
  };
 
  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to permanently delete this report and its data?")) return;
    try {
      await apiService.documents.delete(id);
      fetchDocs();
    } catch (e: any) {
      alert(e.message);
    }
  };
 
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 pl-64 grid-dots pb-12">
      <Sidebar />
      
      <main className="p-8 max-w-6xl mx-auto space-y-8 animate-fade-in">
        
        {/* Header summary */}
        <div className="space-y-2">
          <h1 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            Uploaded Reports & Data Bank
          </h1>
          <p className="text-sm text-gray-400 max-w-[700px]">
            Upload PDF annual reports, CSV datasets, or TXT call transcripts. Uploaded files are automatically checked, parsed, and converted into secure data vectors.
          </p>
        </div>
 
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Upload card panel */}
          <div className="glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-5 h-fit">
            <h2 className="text-base font-extrabold text-white pl-0.5">Upload New Report</h2>
            
            {errorMsg && (
              <div className="flex items-center gap-2.5 p-3.5 rounded-xl bg-red-500/10 border border-red-500/25 text-red-300 text-xs">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <p>{errorMsg}</p>
              </div>
            )}
 
            {successMsg && (
              <div className="flex items-center gap-2.5 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-300 text-xs">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <p>{successMsg}</p>
              </div>
            )}
 
            <form onSubmit={handleUploadSubmit} className="space-y-5">
              <div>
                <label className="block text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2 pl-0.5">
                  Report Type
                </label>
                <select
                  value={docType}
                  onChange={(e) => setDocType(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-gray-900/60 border border-white/[0.06] rounded-xl text-xs text-gray-200"
                >
                  <option value="annual_report">Annual Report (10-K)</option>
                  <option value="SEC_filing">SEC Regulatory Filing</option>
                  <option value="transcript">Earnings Call Transcript</option>
                </select>
              </div>
 
              {/* Clickable & Drag-and-drop functional dropzone */}
              <label 
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`border border-dashed rounded-2xl p-6 flex flex-col items-center justify-center text-center cursor-pointer transition-all relative overflow-hidden group ${
                  dragActive 
                    ? "border-indigo-500 bg-indigo-500/10" 
                    : "border-white/[0.08] hover:border-indigo-500/40 bg-white/[0.01] hover:bg-indigo-500/5"
                }`}
              >
                <UploadCloud className={`w-10 h-10 transition-colors mb-2.5 ${dragActive ? "text-indigo-400" : "text-gray-500 group-hover:text-indigo-400"}`} />
                <span className="text-xs font-bold text-gray-300 group-hover:text-indigo-300 uppercase tracking-wider">
                  {dragActive ? "Drop file here" : "Select financial file"}
                </span>
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept=".pdf,.csv,.txt"
                  className="hidden"
                />
                <p className="text-[9px] text-gray-500 mt-1.5 uppercase font-semibold">PDF, CSV, TXT (Max 10MB)</p>
                {file && (
                  <div className="mt-3 px-3 py-1.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium rounded-lg max-w-[200px] truncate shadow-inner">
                    {file.name}
                  </div>
                )}
              </label>
 
              <button
                type="submit"
                disabled={loading || !file}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 disabled:bg-gray-800 disabled:text-gray-500 text-white rounded-xl text-xs font-bold uppercase tracking-wider transition-all flex items-center justify-center gap-2 shadow-lg"
              >
                {loading ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white/20 border-t-white" />
                ) : (
                  <span>Upload & Index File</span>
                )}
              </button>
            </form>
          </div>
 
          {/* Active Documents List panel */}
          <div className="lg:col-span-2 glass-panel-premium p-6 rounded-3xl border border-white/[0.04] space-y-4">
            <h2 className="text-base font-extrabold text-white pl-0.5">Securely Uploaded Reports</h2>
            
            {documents.length === 0 ? (
              <div className="h-56 border border-dashed border-white/[0.05] rounded-2xl flex flex-col justify-center items-center text-center p-6 bg-white/[0.005]">
                <FileText className="w-8 h-8 text-gray-600 mb-2" />
                <p className="text-xs font-bold text-gray-400">No reports uploaded yet.</p>
                <p className="text-[10px] text-gray-500 mt-1 uppercase font-semibold">Upload an annual report or CSV file to start auditing.</p>
              </div>
            ) : (
              <div className="space-y-3.5 max-h-[440px] overflow-y-auto pr-1">
                {documents.map((doc) => (
                  <div 
                    key={doc.id}
                    className="flex justify-between items-center p-4 bg-white/[0.015] hover:bg-white/[0.025] rounded-2xl border border-white/[0.035] transition-all"
                  >
                    <div className="flex items-center gap-3.5">
                      <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.05] text-indigo-400 shadow-inner">
                        <FileText className="w-5 h-5" />
                      </div>
                      <div className="space-y-1">
                        <h4 className="text-xs font-extrabold text-gray-200 max-w-[260px] md:max-w-[360px] truncate">{doc.filename}</h4>
                        <div className="flex gap-2.5 text-[9px] text-gray-500 font-bold uppercase tracking-wider">
                          <span className="text-indigo-400 font-extrabold">{doc.document_type.replace("_", " ")}</span>
                          <span>•</span>
                          <span>{(doc.size_bytes / 1024).toFixed(1)} KB</span>
                          <span>•</span>
                          <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <span className="hidden md:flex items-center gap-1 px-2.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[9px] font-extrabold uppercase tracking-wide">
                        <ShieldCheck className="w-3 h-3" />
                        <span>Indexed</span>
                      </span>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="p-2.5 bg-red-500/10 hover:bg-red-500/25 text-red-400 border border-red-500/15 hover:border-red-500/30 rounded-xl transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
 
        </section>
 
      </main>
    </div>
  );
}

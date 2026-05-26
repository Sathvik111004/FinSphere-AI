const BASE_URL = "http://localhost:8000/api/v1";

// Helper for HTTP requests sharing credentials cookies
async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${BASE_URL}${endpoint}`;
  
  // Set default header structures
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  
  const config = {
    ...options,
    headers,
    credentials: "include" as const, // CRITICAL: Ensures session cookies are sent back and forth
  };
  
  const response = await fetch(url, config);
  
  if (!response.ok) {
    let errMsg = "An error occurred with backend operations.";
    try {
      const errJSON = await response.json();
      errMsg = errJSON.detail || errMsg;
    } catch (_) {}
    throw new Error(errMsg);
  }
  
  // Handle empty bodies (e.g. logouts)
  if (response.status === 204) return null;
  
  try {
    return await response.json();
  } catch (e) {
    return null;
  }
}

export const apiService = {
  // 1. Authentication
  auth: {
    signup: (data: any) => fetchAPI("/auth/signup", { method: "POST", body: JSON.stringify(data) }),
    login: (data: any) => fetchAPI("/auth/login", { method: "POST", body: JSON.stringify(data) }),
    logout: () => fetchAPI("/auth/logout", { method: "POST" }),
    getMe: () => fetchAPI("/auth/me")
  },
  
  // 2. Document management
  documents: {
    upload: (formData: FormData) => fetchAPI("/documents/upload", { method: "POST", body: formData }),
    list: () => fetchAPI("/documents/"),
    delete: (id: string) => fetchAPI(`/documents/${id}`, { method: "DELETE" })
  },
  
  // 3. RAG Q&A
  rag: {
    query: (query: string) => fetchAPI("/rag/query", { method: "POST", body: JSON.stringify({ query }) })
  },
  
  // 4. ML / Risk / Sentiment
  ml: {
    predictRisk: (data: any) => fetchAPI("/ml/predict-risk", { method: "POST", body: JSON.stringify(data) }),
    forecastRevenue: (quarters: number[]) => fetchAPI("/ml/forecast-revenue", { method: "POST", body: JSON.stringify({ quarters_history: quarters }) }),
    scanAnomalies: (margin: number, leverage: number) => fetchAPI("/ml/detect-anomalies", { method: "POST", body: JSON.stringify({ operating_margin: margin, leverage_ratio: leverage }) }),
    analyzeSentiment: (text: string) => fetchAPI("/ml/analyze-sentiment", { method: "POST", body: JSON.stringify({ transcript_text: text }) })
  },
  
  // 5. Analyst Agent
  analyst: {
    runTask: (prompt: string, chatHistory: any[] = []) => fetchAPI("/analyst/run-task", { method: "POST", body: JSON.stringify({ prompt, chat_history: chatHistory }) })
  },
  
  // 6. Portfolio recommendations
  portfolio: {
    generate: (data: any) => fetchAPI("/portfolio/generate", { method: "POST", body: JSON.stringify(data) }),
    getHistory: () => fetchAPI("/portfolio/history")
  }
};
export default apiService;

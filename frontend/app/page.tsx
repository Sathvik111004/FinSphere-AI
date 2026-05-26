"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiService } from "../services/api";

export default function RootIndex() {
  const router = useRouter();

  useEffect(() => {
    // Check if the user is logged in
    apiService.auth.getMe()
      .then(() => {
        router.push("/dashboard");
      })
      .catch(() => {
        router.push("/login");
      });
  }, [router]);

  return (
    <div className="flex h-screen w-screen items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-4 text-center">
        {/* Loading Spinner */}
        <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-indigo-500/10 border-t-indigo-500" />
        <h2 className="text-sm font-semibold tracking-wide text-gray-400 uppercase">
          Verifying secure session tokens...
        </h2>
      </div>
    </div>
  );
}

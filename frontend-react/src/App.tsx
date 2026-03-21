import { useState } from "react";
import { HeroSection } from "./components/HeroSection";
import { SocialProofSection } from "./components/SocialProofSection";
import { AnalyzerForm } from "./components/AnalyzerForm";
import { ResultsDisplay, type AnalyzeResponse } from "./components/ResultsDisplay";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState("");

  const handleAnalyze = async (resumeText: string, resumeFile: File | null, jd: string) => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const formData = new FormData();
      if (resumeFile) {
        formData.append("resume_file", resumeFile);
      } else {
        formData.append("resume_text", resumeText);
      }
      formData.append("jd_text", jd);

      const response = await fetch("/api/v1/analyze", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Failed to analyze. Please try again.");
      }
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background relative selection:bg-primary/30">
      <HeroSection />
      <SocialProofSection />
      
      {/* Interactive Core App Section */}
      <section className="relative w-full z-20 py-24 px-4 bg-background">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent" />
        <div className="max-w-6xl mx-auto flex flex-col items-center">
          <AnalyzerForm onSubmit={handleAnalyze} isLoading={loading} />
          
          {error && (
            <div className="mt-8 p-4 liquid-glass border border-destructive/30 text-destructive-foreground rounded-lg w-full max-w-4xl text-center shadow-lg">
              {error}
            </div>
          )}
          
          {result && <ResultsDisplay data={result} />}
        </div>
      </section>
    </main>
  );
}

export default App;

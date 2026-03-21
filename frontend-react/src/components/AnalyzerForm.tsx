import { useState } from "react";
import { Button } from "./ui/button";
import { Sparkles, FileText, Briefcase } from "lucide-react";

interface AnalyzerFormProps {
  onSubmit: (resumeText: string, resumeFile: File | null, jd: string) => void;
  isLoading: boolean;
}

export function AnalyzerForm({ onSubmit, isLoading }: AnalyzerFormProps) {
  const [resumeText, setResumeText] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");

  const handleDemo = () => {
    setResumeFile(null);
    setResumeText("Senior Software Engineer with 6 years of experience. Expert in Python, Django, SQL, and AWS. Built scalable microservices and led a team of 4 engineers.");
    setJd("We are looking for an AI Engineer to join our team. Must have strong Python backend skills (FastAPI, PyTorch), experience with LLM integration, and Kubernetes for deployment.");
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setResumeFile(file);
      setResumeText(""); // clear text if file is uploaded
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!resumeText && !resumeFile) return alert("Please provide a Resume (PDF or Text).");
    if (!jd) return alert("Please provide the Job Description.");
    onSubmit(resumeText, resumeFile, jd);
  };

  return (
    <div className="liquid-glass rounded-3xl p-8 md:p-12 border border-white/5 relative z-20 mx-auto w-full max-w-4xl shadow-2xl">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-purple-400">
            AI Skill-Gap Analyzer
          </h2>
          <p className="text-hero-sub mt-2 max-w-lg">
            Compare a candidate's resume against the target job description to instantly generate a hyper-personalized adaptive learning pathway.
          </p>
        </div>
        <Button variant="outline" onClick={handleDemo} className="border-white/10 text-white hover:bg-white/10 shrink-0">
          <Sparkles className="w-4 h-4 mr-2 text-primary" />
          Load Demo Data
        </Button>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-3">
            <label className="text-sm font-medium text-foreground flex items-center justify-between">
              <span className="flex items-center gap-2"><FileText className="w-4 h-4 text-primary" /> Candidate Resume</span>
              {resumeFile && (
                <button type="button" onClick={() => setResumeFile(null)} className="text-xs text-destructive hover:underline">
                  Remove PDF
                </button>
              )}
            </label>
            
            {resumeFile ? (
              <div className="liquid-glass w-full h-48 rounded-xl flex items-center justify-center flex-col gap-2 border border-primary/30 bg-primary/5">
                <FileText className="w-8 h-8 text-primary" />
                <span className="text-sm font-medium">{resumeFile.name}</span>
                <span className="text-xs text-hero-sub">Ready for analysis</span>
              </div>
            ) : (
              <div className="relative h-48 group">
                <textarea
                  className="liquid-glass w-full h-full rounded-xl p-4 text-sm text-foreground bg-transparent placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-primary resize-none transition-all"
                  placeholder="Paste the candidate's full resume text here..."
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                />
                <div className="absolute bottom-3 right-3">
                  <input
                    type="file"
                    id="resume-upload"
                    accept=".pdf"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                  <label 
                    htmlFor="resume-upload" 
                    className="cursor-pointer text-xs flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-white/5 border border-white/10 hover:bg-white/10 text-white transition-colors"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    Upload PDF instead
                  </label>
                </div>
              </div>
            )}
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-foreground flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-primary" />
              Job Description
            </label>
            <textarea
              className="liquid-glass w-full h-48 rounded-xl p-4 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-primary resize-none transition-all"
              placeholder="Paste the target role description here..."
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />
          </div>
        </div>

        <Button 
          type="submit" 
          variant="hero" 
          className="w-full md:w-auto md:self-end mt-4 shadow-[0_0_30px_rgba(152,58,214,0.3)] transition-all hover:shadow-[0_0_40px_rgba(152,58,214,0.5)]"
          disabled={isLoading}
        >
          {isLoading ? "Analyzing Capabilities..." : "Generate Adaptive Pathway"}
        </Button>
      </form>
    </div>
  );
}

import { Zap } from "lucide-react";
import { Navbar } from "./Navbar";
import { Button } from "./ui/button";

export function HeroSection() {
  return (
    <section className="bg-background relative w-full overflow-hidden flex flex-col items-center">
      <Navbar />

      <div className="pt-20 px-4 w-full flex flex-col items-center justify-center relative z-10">
        {/* Decorative Tag */}
          <div className="liquid-glass inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/5 mb-8 shadow-sm">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium tracking-wide text-hero-sub">AI-Adaptive Pathways</span>
          </div>

          <h1 className="text-[120px] sm:text-[180px] lg:text-[230px] font-medium leading-[0.8] tracking-[-0.03em] mb-8 bg-clip-text text-transparent bg-[linear-gradient(223deg,#E8E8E9_0%,#3A7BBF_104.15%)] drop-shadow-2xl" style={{ fontFamily: "'General Sans', sans-serif" }}>
            InfiOnboard
          </h1>

          <p className="text-xl sm:text-2xl text-hero-sub max-w-2xl mx-auto font-light leading-relaxed tracking-wide mb-12">
            The intelligent onboarding engine <br className="hidden sm:block" />
            that generates precise learning pathways for every new hire
          </p>

          <Button variant="heroSecondary" size="lg" className="px-8 h-14 text-base tracking-wide" onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}>
            Try the Analyzer
          </Button>
      </div>
    </section>
  );
}

import { ArrowRight, Zap, Github, Figma, Framer, Slack, Twitch, Gitlab } from "lucide-react";
import { InfiniteSlider } from "./ui/infinite-slider";

const LOGOS = [Github, Figma, Framer, Slack, Twitch, Gitlab];

export function Hero() {


  return (
    <section className="relative w-full min-h-[90vh] flex flex-col items-center pt-24 pb-0 overflow-hidden bg-[#010101]">
      {/* ── Content (z-20) ──────────────────────────────────────────────────────── */}
      <div className="relative z-20 flex flex-col items-center text-center px-4 max-w-5xl mx-auto w-full">
        {/* Announcement Pill */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[rgba(28,27,36,0.15)] border border-white/10 mb-8 backdrop-blur-md shadow-lg">
          <div className="bg-gradient-to-tr from-[#FA93FA] via-[#C967E8] to-[#983AD6] p-1 rounded-full shadow-[0_0_10px_rgba(201,103,232,0.4)]">
            <Zap className="w-3 h-3 text-white" fill="currentColor" />
          </div>
          <span className="text-xs font-medium text-slate-300 tracking-wide pr-2">
            Used by founders. Loved by devs.
          </span>
        </div>

        {/* Headlines */}
        <h1 className="text-5xl sm:text-6xl md:text-[80px] font-black tracking-tight leading-[1.05] mb-6 drop-shadow-2xl">
          <span className="text-white">Your Vision</span>
          <br />
          <span className="gradient-text-primary">Our Digital Reality.</span>
        </h1>

        {/* Subheadline */}
        <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto font-medium leading-relaxed mb-10 drop-shadow-md">
          We turn bold ideas into modern designs that don't just look amazing,
          they grow your business fast.
        </p>

        {/* CTA Button */}
        <div className="p-[1px] rounded-full bg-gradient-to-r from-white/20 via-white/5 to-white/20 backdrop-blur-md shadow-[0_0_30px_-5px_var(--color-brand-500)]">
          <button className="flex items-center gap-3 bg-white text-black px-8 py-3.5 rounded-full font-bold text-[15px] hover:bg-slate-100 transition-colors shadow-xl group">
            Book a 15-min call
            <div className="bg-gradient-to-tr from-[#FA93FA] via-[#C967E8] to-[#983AD6] p-1.5 rounded-full group-hover:scale-110 transition-transform">
              <ArrowRight className="w-4 h-4 text-white" />
            </div>
          </button>
        </div>
      </div>

      {/* ── Video Background (z-10) ─────────────────────────────────────────────── */}
      <div className="relative w-full z-10 -mt-[150px] pointer-events-none select-none bg-gradient-to-br from-[#1c002e]/60 via-[#010101] to-[#25003b]/40 min-h-[600px] flex items-center justify-center">
        {/* Top/Bottom Fade Overlays */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#010101] via-transparent to-[#010101] z-10" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#010101] via-transparent to-[#010101] z-10 opacity-80" />
        <video
          src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260308_114720_3dabeb9e-2c39-4907-b747-bc3544e2d5b7.mp4"
          autoPlay
          muted
          loop
          playsInline
          className="w-full h-auto min-h-full object-cover opacity-80 mix-blend-screen absolute inset-0"
        />
      </div>

      {/* ── Logo Cloud ──────────────────────────────────────────────────────────── */}
      <div className="relative z-30 w-full bg-black/40 backdrop-blur-md border-t border-white/5 py-8 mt-[-80px]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center gap-8 md:gap-12 overflow-hidden">
          {/* Label */}
          <div className="flex items-center gap-6 shrink-0">
            <span className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400 whitespace-nowrap">
              Powering the best teams
            </span>
            <div className="hidden md:block w-px h-8 bg-white/10" />
          </div>

          {/* Marquee */}
          <div className="flex-1 w-full mask-edges overflow-hidden">
            <InfiniteSlider speed="slow" pauseOnHover={false}>
              {LOGOS.map((Icon, i) => (
                <div key={i} className="flex items-center justify-center opacity-60 hover:opacity-100 transition-opacity">
                  <Icon className="w-8 h-8 text-white" />
                </div>
              ))}
            </InfiniteSlider>
          </div>
        </div>
      </div>
    </section>
  );
}

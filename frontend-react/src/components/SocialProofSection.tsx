import { useEffect, useRef, useState } from "react";

const BRANDS = ["Vortex", "Nimbus", "Prysma", "Cirrus", "Kynder", "Halcyn"];

export function SocialProofSection() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [opacity, setOpacity] = useState(0);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    let rafId = 0;

    const updateFade = () => {
      const { currentTime, duration } = video;
      if (duration > 0) {
        const fadeDuration = 0.5;
        let newOpacity = 1;

        if (currentTime < fadeDuration) {
          newOpacity = currentTime / fadeDuration;
        } else if (currentTime > duration - fadeDuration) {
          newOpacity = (duration - currentTime) / fadeDuration;
        }

        setOpacity(newOpacity);
      }
      rafId = requestAnimationFrame(updateFade);
    };

    const handleEnded = () => {
      setOpacity(0);
      setTimeout(() => {
        video.currentTime = 0;
        video.play().catch(() => {});
      }, 100);
    };

    video.addEventListener("ended", handleEnded);
    rafId = requestAnimationFrame(updateFade);

    return () => {
      cancelAnimationFrame(rafId);
      video.removeEventListener("ended", handleEnded);
    };
  }, []);

  return (
    <section className="relative w-full overflow-hidden bg-background">
      {/* Background Video */}
      <div className="absolute inset-0 w-full h-full">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover transition-opacity duration-100"
          style={{ opacity }}
        >
          <source 
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260308_114720_3dabeb9e-2c39-4907-b747-bc3544e2d5b7.mp4" 
            type="video/mp4" 
          />
        </video>
        {/* Gradient Overlays */}
        <div className="absolute inset-0 bg-gradient-to-b from-background via-transparent to-background" />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center pt-16 pb-24 px-4 gap-20">
        {/* Spacer for video visibility */}
        <div className="h-40" />

        {/* Logo Marquee Container */}
        <div className="w-full max-w-5xl flex flex-col md:flex-row items-center gap-8 md:gap-16">
          <div className="text-foreground/50 text-sm whitespace-nowrap shrink-0 leading-tight">
            Relied on by brands <br /> across the globe
          </div>

          <div className="flex-1 overflow-hidden relative group">
            <div className="flex w-fit animate-marquee gap-16 items-center py-4">
              {[...BRANDS, ...BRANDS].map((brand, i) => (
                <div key={i} className="flex items-center gap-3 shrink-0">
                  <div className="liquid-glass w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-bold">
                    {brand[0]}
                  </div>
                  <span className="text-base font-semibold text-foreground">
                    {brand}
                  </span>
                </div>
              ))}
            </div>
            
            {/* Edge Fades for marquee */}
            <div className="absolute inset-y-0 left-0 w-20 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none" />
            <div className="absolute inset-y-0 right-0 w-20 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none" />
          </div>
        </div>
      </div>
    </section>
  );
}

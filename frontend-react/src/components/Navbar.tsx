import { ChevronDown } from "lucide-react";
import { Button } from "./ui/button";
import onboardLogo from "../assets/Onboard.png";

export function Navbar() {
  return (
    <div className="w-full relative z-50">
      <nav className="w-full py-5 px-8 flex flex-row justify-between items-center">
        {/* Left: Logo */}
          <div className="flex items-center gap-2 lg:gap-3 cursor-pointer group">
            <div className="w-10 h-10 lg:w-11 lg:h-11 rounded-full bg-white/5 border border-white/10 flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(152,58,214,0.3)] group-hover:shadow-[0_0_25px_rgba(152,58,214,0.5)] transition-all overflow-hidden p-0.5">
              <img src={onboardLogo} alt="InfiOnboard Logo" className="w-full h-full object-contain rounded-full" />
            </div>
            <span className="text-xl font-medium tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
              InfiOnboard
            </span>
          </div>

        {/* Center: Nav Items */}
        <div className="hidden md:flex flex-row items-center gap-1">
          <Button variant="ghost" className="text-foreground/90 text-base font-normal">
            Features <ChevronDown className="ml-1 h-4 w-4 opacity-50" />
          </Button>
          <Button variant="ghost" className="text-foreground/90 text-base font-normal">
            Solutions
          </Button>
          <Button variant="ghost" className="text-foreground/90 text-base font-normal">
            Plans
          </Button>
          <Button variant="ghost" className="text-foreground/90 text-base font-normal">
            Learning <ChevronDown className="ml-1 h-4 w-4 opacity-50" />
          </Button>
        </div>

        {/* Right: Sign Up */}
        <div className="flex items-center shrink-0">
          <Button variant="heroSecondary" size="sm" className="rounded-full px-4 py-2">
            Sign Up
          </Button>
        </div>
      </nav>

      {/* 1px gradient divider */}
      <div className="mt-[3px] w-full h-px bg-gradient-to-r from-transparent via-foreground/20 to-transparent" />
    </div>
  );
}

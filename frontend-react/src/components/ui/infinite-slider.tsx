import { cn } from "../../lib/utils";
import { motion } from "motion/react";
import useMeasure from "react-use-measure";

type InfiniteSliderProps = {
  children: React.ReactNode;
  direction?: "left" | "right";
  speed?: "fast" | "normal" | "slow";
  pauseOnHover?: boolean;
  className?: string;
};

export function InfiniteSlider({
  children,
  direction = "left",
  speed = "normal",
  pauseOnHover = true,
  className,
}: InfiniteSliderProps) {
  let [ref] = useMeasure();
  
  const speedMap = {
    fast: 20,
    normal: 40,
    slow: 60,
  };
  
  const duration = speedMap[speed];

  return (
    <div
      className={cn(
        "relative flex w-full overflow-hidden [mask-image:linear-gradient(to_right,transparent,white_10%,white_90%,transparent)]",
        className
      )}
    >
      <motion.div
        className={cn("flex flex-row w-max min-w-full shrink-0 gap-12 py-4", {
          "hover:[animation-play-state:paused]": pauseOnHover,
        })}
        initial={{ x: direction === "left" ? 0 : "-50%" }}
        animate={{ x: direction === "left" ? "-50%" : 0 }}
        transition={{
          duration: duration,
          ease: "linear",
          repeat: Infinity,
        }}
        ref={ref}
      >
        {children}
        {children}
      </motion.div>
    </div>
  );
}

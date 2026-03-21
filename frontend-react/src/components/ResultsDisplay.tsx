import { Video, BookOpen, Clock, Target, ShieldCheck, Zap } from "lucide-react";

export interface AnalyzeResponse {
  skills_extracted: string[];
  job_description_skills: string[];
  skill_gap_found: boolean;
  learning_pathway: Array<{
    week: number;
    modules: Array<{
      module_name: string;
      difficulty_level: string;
      estimated_hours: number;
      assigned_courses: Array<{
        course_id: string;
        title: string;
        provider: string;
        duration_hours: number;
        resource_link: string;
        resource_type: string;
        reasoning_trace?: string;
      }>;
    }>;
  }>;
  total_ttr_business_days: number;
  estimated_ttr_savings_business_days?: number;
}

export function ResultsDisplay({ data }: { data: AnalyzeResponse }) {
  if (!data) return null;

  return (
    <div className="w-full max-w-5xl mx-auto mt-12 mb-24 flex flex-col gap-8 animate-in fade-in slide-in-from-bottom-10 duration-700">
      
      {/* Overview Stats Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-primary/20 bg-primary/5">
          <div className="flex items-center gap-2 text-primary font-medium mb-1">
            <Clock className="w-5 h-5" />
            Time To Role (TTR)
          </div>
          <span className="text-4xl font-light">{data.total_ttr_business_days} <span className="text-xl text-hero-sub">Days</span></span>
          <span className="text-xs text-hero-sub mt-2">Optimized pathway duration</span>
        </div>

        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-green-500/20 bg-green-500/5">
          <div className="flex items-center gap-2 text-green-400 font-medium mb-1">
            <Zap className="w-5 h-5 fill-green-400/20" />
            TTR Savings
          </div>
          <span className="text-4xl font-light text-green-300">
            {data.estimated_ttr_savings_business_days || 0} <span className="text-xl">Days</span>
          </span>
          <span className="text-xs text-hero-sub mt-2">Saved by skipping known concepts</span>
        </div>

        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-blue-500/20 bg-blue-500/5">
          <div className="flex items-center gap-2 text-blue-400 font-medium mb-1">
            <ShieldCheck className="w-5 h-5" />
            Skill Gap Validation
          </div>
          <span className="text-2xl font-medium text-white line-clamp-2 leading-tight">
            {data.skill_gap_found ? "Adaptive Path Required" : "Candidate Ready"}
          </span>
          <span className="text-xs text-hero-sub mt-2 uppercase tracking-widest">
            {data.job_description_skills.length} target skills
          </span>
        </div>
      </div>

      {/* Pathway Timeline */}
      <div className="mt-8 relative border-l-2 border-primary/20 pl-8 ml-4 flex flex-col gap-12">
        {data.learning_pathway.map((weekData) => (
          <div key={weekData.week} className="relative">
            {/* Timeline Dot */}
            <div className="absolute -left-[41px] top-6 w-5 h-5 rounded-full bg-background border-4 border-primary shadow-[0_0_15px_rgba(152,58,214,0.5)] z-10" />
            
            <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/50 mb-6">
              Week {weekData.week}
            </h3>

            <div className="flex flex-col gap-6">
              {weekData.modules.map((mod, i) => (
                <div key={i} className="liquid-glass rounded-xl p-6 border border-white/5">
                  <div className="flex flex-col lg:flex-row justify-between lg:items-center gap-4 mb-5 pb-5 border-b border-white/10">
                    <div>
                      <h4 className="text-xl font-medium text-white flex items-center gap-2">
                        <Target className="w-5 h-5 text-primary" />
                        {mod.module_name}
                      </h4>
                      <div className="flex items-center gap-3 mt-2 text-sm">
                        <span className="px-2.5 py-1 rounded-full bg-white/5 text-hero-sub border border-white/10">
                          {mod.difficulty_level}
                        </span>
                        <span className="text-hero-sub flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" />
                          {mod.estimated_hours}h estimated
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {mod.assigned_courses.map((course) => (
                      <div key={course.course_id} className="bg-background/50 rounded-lg p-4 border border-white/5 flex flex-col gap-3 hover:bg-white/5 transition-colors group">
                        <div className="flex justify-between items-start gap-4">
                          <div className="flex flex-col">
                            <span className="font-medium text-[15px]">{course.title}</span>
                            <span className="text-xs text-primary/80 mt-1">{course.provider}</span>
                          </div>
                          <span className="shrink-0 text-xs font-mono text-muted-foreground bg-black/40 px-2 py-1 rounded">
                            {course.duration_hours}h
                          </span>
                        </div>
                        
                        {course.reasoning_trace && (
                          <div className="mt-1 text-xs text-hero-sub/80 italic leading-relaxed border-l-2 border-primary/30 pl-3">
                            "{course.reasoning_trace}"
                          </div>
                        )}

                        <div className="mt-auto pt-3">
                          <a 
                            href={course.resource_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 text-xs font-medium text-white hover:text-primary transition-colors"
                          >
                            {course.resource_type === "Video" ? <Video className="w-3.5 h-3.5" /> : <BookOpen className="w-3.5 h-3.5" />}
                            Access {course.resource_type}
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

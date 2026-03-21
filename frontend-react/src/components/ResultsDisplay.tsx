import { BookOpen, Clock, Target, ShieldCheck, Zap } from "lucide-react";

export interface CourseItem {
  id: number;
  title: string;
  skill_tag: string;
  duration_hours: number;
  level: string;
  description: string;
  resource_type: string;
  resource_link: string;
  matched_skill: string;
  reasoning: string;
}

export interface AnalyzeResponse {
  resume_skills: Record<string, string>;
  jd_skills: Record<string, string>;
  skill_gap: string[];
  common_skills: string[];
  pathway: CourseItem[];
  total_hours: number;
  total_catalog_hours: number;
  ttr_saved_hours: number;
  summary: string;
}

export function ResultsDisplay({ data }: { data: AnalyzeResponse }) {
  if (!data) return null;

  const totalJdSkills = Object.keys(data.jd_skills || {}).length;
  const hasGap = data.skill_gap && data.skill_gap.length > 0;

  return (
    <div className="w-full max-w-5xl mx-auto mt-12 mb-24 flex flex-col gap-8 animate-in fade-in slide-in-from-bottom-10 duration-700">
      
      {/* Overview Summary */}
      <div className="text-center max-w-2xl mx-auto mb-4">
        <p className="text-xl font-light text-hero-sub leading-relaxed">{data.summary}</p>
      </div>

      {/* Overview Stats Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-primary/20 bg-primary/5">
          <div className="flex items-center gap-2 text-primary font-medium mb-1">
            <Clock className="w-5 h-5" />
            Time To Role (TTR)
          </div>
          <span className="text-4xl font-light">{data.total_hours} <span className="text-xl text-hero-sub">Hours</span></span>
          <span className="text-xs text-hero-sub mt-2">Optimized pathway duration</span>
        </div>

        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-green-500/20 bg-green-500/5">
          <div className="flex items-center gap-2 text-green-400 font-medium mb-1">
            <Zap className="w-5 h-5 fill-green-400/20" />
            TTR Savings
          </div>
          <span className="text-4xl font-light text-green-300">
            {data.ttr_saved_hours || 0} <span className="text-xl">Hours</span>
          </span>
          <span className="text-xs text-hero-sub mt-2">Saved by skipping {data.common_skills?.length || 0} known skills</span>
        </div>

        <div className="liquid-glass p-6 rounded-2xl flex flex-col gap-1 border border-blue-500/20 bg-blue-500/5">
          <div className="flex items-center gap-2 text-blue-400 font-medium mb-1">
            <ShieldCheck className="w-5 h-5" />
            Skill Gap Validation
          </div>
          <span className="text-2xl font-medium text-white leading-tight">
            {hasGap ? `${data.skill_gap.length} Missing Skills` : "Candidate Ready"}
          </span>
          <span className="text-xs text-hero-sub mt-2 uppercase tracking-widest">
            {totalJdSkills} target skills found
          </span>
        </div>
      </div>

      {/* Pathway Timeline */}
      {hasGap && data.pathway?.length > 0 && (
        <div className="mt-8 relative border-l-2 border-primary/20 pl-8 ml-4 flex flex-col gap-8">
          {data.pathway.map((course, idx) => (
            <div key={idx} className="relative">
              {/* Timeline Dot */}
              <div className="absolute -left-[41px] top-6 w-5 h-5 rounded-full bg-background border-4 border-primary shadow-[0_0_15px_rgba(152,58,214,0.5)] z-10" />
              
              <div className="liquid-glass rounded-xl p-6 border border-white/5 hover:border-white/10 transition-colors">
                <div className="flex flex-col lg:flex-row justify-between lg:items-start gap-4 mb-3 pb-4 border-b border-white/10">
                  <div>
                    <h3 className="text-2xl font-medium text-white flex items-center gap-2">
                      <Target className="w-5 h-5 text-primary" />
                      {course.title}
                    </h3>
                    <p className="text-sm text-hero-sub mt-1 leading-relaxed max-w-2xl">{course.description}</p>
                    <div className="flex items-center gap-3 mt-4 text-sm">
                      <span className="px-2.5 py-1 rounded-full bg-primary/20 text-primary border border-primary/30 uppercase tracking-widest text-[10px] font-bold">
                        {course.matched_skill}
                      </span>
                      <span className="px-2.5 py-1 rounded-full bg-white/5 text-hero-sub border border-white/10">
                        {course.level}
                      </span>
                      <span className="text-hero-sub flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" />
                        {course.duration_hours}h
                      </span>
                    </div>
                  </div>
                  <a 
                    href={course.resource_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="shrink-0 inline-flex items-center justify-center gap-2 bg-white text-black hover:bg-white/90 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                  >
                    <BookOpen className="w-4 h-4" />
                    Access {course.resource_type}
                  </a>
                </div>

                {course.reasoning && (
                  <div className="mt-4 text-sm text-hero-sub italic leading-relaxed border-l-2 border-primary/30 pl-4 py-1">
                    "{course.reasoning}"
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

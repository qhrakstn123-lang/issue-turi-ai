import type { GenerationResult } from "../lib/types";

type ResultSummaryProps = {
  result: GenerationResult;
};

export function ResultSummary({ result }: ResultSummaryProps) {
  const scenes = result.storyboard.scenes;
  const totalDuration = result.timeline.total_duration;
  const targetDelta = Math.round((totalDuration - result.video_script.target_duration_seconds) * 10) / 10;
  const items = [
    ["제목", result.video_script.title],
    ["안전 상태", result.safety_status],
    ["사람 검토", result.required_human_review ? "필요" : "불필요"],
    ["장면 수", String(scenes.length)],
    ["타임라인 길이", `${Math.round(totalDuration * 10) / 10}s`],
    ["목표 대비", `${targetDelta > 0 ? "+" : ""}${targetDelta}s`],
  ];

  return (
    <section className="summary-grid" aria-label="Generation summary">
      {items.map(([label, value]) => (
        <div className="summary-item" key={label}>
          <span className="summary-label">{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </section>
  );
}

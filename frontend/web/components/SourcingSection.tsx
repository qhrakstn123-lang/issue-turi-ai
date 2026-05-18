import type { Scene } from "../lib/types";

type SourcingSectionProps = {
  scene: Scene;
};

export function SourcingSection({ scene }: SourcingSectionProps) {
  return (
    <section className="scene-section">
      <h3>기본 시각 제안</h3>
      <p className="muted-copy">fallback suggestion: Source Capture Plan이 있으면 원본 소스 우선 계획을 먼저 검토합니다.</p>
      <div className="scene-tags">
        <span>visual_source_strategy: {scene.visual_source_strategy || "-"}</span>
        <span>capture_source_type: {scene.capture_source_type || "-"}</span>
        <span>capture_usage_mode: {scene.capture_usage_mode || "-"}</span>
      </div>
      <p className="asset-note">{scene.asset_usage_note || "-"}</p>
    </section>
  );
}

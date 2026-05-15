import type { Scene } from "../lib/types";

type SourcingSectionProps = {
  scene: Scene;
};

export function SourcingSection({ scene }: SourcingSectionProps) {
  return (
    <section className="scene-section">
      <h3>소싱</h3>
      <div className="scene-tags">
        <span>전략: {scene.visual_source_strategy || "-"}</span>
        <span>출처: {scene.capture_source_type || "-"}</span>
        <span>사용 방식: {scene.capture_usage_mode || "-"}</span>
      </div>
      <p className="asset-note">{scene.asset_usage_note || "-"}</p>
    </section>
  );
}

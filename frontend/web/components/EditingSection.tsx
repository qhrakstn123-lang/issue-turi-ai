import type { Scene } from "../lib/types";

type EditingSectionProps = {
  scene: Scene;
};

export function EditingSection({ scene }: EditingSectionProps) {
  return (
    <section className="scene-section">
      <h3>편집</h3>
      <div className="scene-tags">
        <span>모션: {scene.motion_direction || "-"}</span>
        <span>효과음: {scene.sound_effect_hint || "-"}</span>
        <span>전환: {scene.transition || "-"}</span>
      </div>
      <p className="muted-copy">{scene.editing_notes || "-"}</p>
    </section>
  );
}

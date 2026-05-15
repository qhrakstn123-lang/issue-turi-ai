import type { Scene } from "../lib/types";
import { EditingSection } from "./EditingSection";
import { SourcingSection } from "./SourcingSection";
import { VisualSection } from "./VisualSection";

type SceneCardProps = {
  scene: Scene;
};

export function SceneCard({ scene }: SceneCardProps) {
  return (
    <article className="scene-card">
      <div className="scene-meta">
        <strong>
          {scene.scene_id} / {scene.scene_purpose}
        </strong>
        <span>{scene.estimated_duration}s</span>
      </div>

      <section className="scene-section">
        <h3>대본</h3>
        <p>{scene.narration || "-"}</p>
      </section>

      <section className="scene-section">
        <h3>자막</h3>
        <div className="scene-tags">
          <span>자막: {scene.subtitle || "-"}</span>
          <span>강조 문구: {scene.emphasis_caption || "-"}</span>
        </div>
      </section>

      <VisualSection scene={scene} />
      <SourcingSection scene={scene} />
      <EditingSection scene={scene} />
    </article>
  );
}

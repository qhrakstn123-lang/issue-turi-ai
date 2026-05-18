import type { Scene } from "../lib/types";
import { EditingSection } from "./EditingSection";
import { SceneEditor, type SceneEditablePatch } from "./SceneEditor";
import { SourcingSection } from "./SourcingSection";
import { VisualSection } from "./VisualSection";

type SceneCardProps = {
  scene: Scene;
  isEdited?: boolean;
  onChangeScene?: (sceneId: string, updates: SceneEditablePatch) => void;
  onResetScene?: (sceneId: string) => void;
};

export function SceneCard({ scene, isEdited = false, onChangeScene, onResetScene }: SceneCardProps) {
  return (
    <article className="scene-card">
      <div className="scene-meta">
        <strong>
          {scene.scene_id} / {scene.scene_purpose}
        </strong>
        <div className="scene-meta-actions">
          {isEdited ? <span className="edited-badge">Edited</span> : null}
          <span>{scene.estimated_duration}s</span>
        </div>
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

      {onChangeScene && onResetScene ? (
        <details className="scene-edit-details">
          <summary>장면 수정</summary>
          <SceneEditor scene={scene} isEdited={isEdited} onUpdateScene={onChangeScene} onResetScene={onResetScene} />
        </details>
      ) : null}
    </article>
  );
}

"use client";

import type { Scene } from "../lib/types";

export type SceneEditablePatch = Partial<
  Pick<
    Scene,
    | "narration"
    | "tts_text"
    | "subtitle"
    | "emphasis_caption"
    | "estimated_duration"
    | "visual_description"
    | "generated_image_prompt"
    | "asset_usage_note"
    | "editing_notes"
  >
>;

type SceneEditorProps = {
  scene: Scene;
  isEdited: boolean;
  onUpdateScene: (sceneId: string, updates: SceneEditablePatch) => void;
  onResetScene: (sceneId: string) => void;
};

export function SceneEditor({ scene, isEdited, onUpdateScene, onResetScene }: SceneEditorProps) {
  function updateText(field: keyof Omit<SceneEditablePatch, "estimated_duration">, value: string) {
    onUpdateScene(scene.scene_id, { [field]: value });
  }

  function updateDuration(value: string) {
    const parsed = Number(value);
    onUpdateScene(scene.scene_id, {
      estimated_duration: Number.isFinite(parsed) && parsed > 0 ? parsed : 1,
    });
  }

  return (
    <section className="scene-editor" aria-label={`${scene.scene_id} 장면 수정`}>
      <div className="scene-editor-heading">
        <div>
          <strong>장면 수정</strong>
          <span>compact editor</span>
        </div>
        <button className="link-button" type="button" onClick={() => onResetScene(scene.scene_id)} disabled={!isEdited}>
          원본으로 되돌리기
        </button>
      </div>

      <div className="editor-field-grid">
        <label>
          예상 길이
          <input
            name="estimated_duration"
            type="number"
            min={1}
            step={0.5}
            value={scene.estimated_duration}
            onChange={(event) => updateDuration(event.target.value)}
          />
        </label>
        <label>
          자막
          <input
            name="subtitle"
            value={scene.subtitle}
            onChange={(event) => updateText("subtitle", event.target.value)}
          />
        </label>
        <label>
          강조 문구
          <input
            name="emphasis_caption"
            value={scene.emphasis_caption}
            onChange={(event) => updateText("emphasis_caption", event.target.value)}
          />
        </label>
        <label>
          TTS 문장
          <input name="tts_text" value={scene.tts_text} onChange={(event) => updateText("tts_text", event.target.value)} />
        </label>
      </div>

      <label>
        내레이션
        <textarea
          name="narration"
          rows={3}
          value={scene.narration}
          onChange={(event) => updateText("narration", event.target.value)}
        />
      </label>

      <label>
        시각 자료 설명
        <textarea
          name="visual_description"
          rows={2}
          value={scene.visual_description}
          onChange={(event) => updateText("visual_description", event.target.value)}
        />
      </label>

      <details className="prompt-details scene-editor-prompt">
        <summary>생성 이미지 프롬프트</summary>
        <textarea
          name="generated_image_prompt"
          rows={4}
          value={scene.generated_image_prompt}
          onChange={(event) => updateText("generated_image_prompt", event.target.value)}
        />
      </details>

      <label>
        자료 사용 메모
        <textarea
          name="asset_usage_note"
          rows={2}
          value={scene.asset_usage_note}
          onChange={(event) => updateText("asset_usage_note", event.target.value)}
        />
      </label>

      <label>
        편집 메모
        <textarea
          name="editing_notes"
          rows={2}
          value={scene.editing_notes}
          onChange={(event) => updateText("editing_notes", event.target.value)}
        />
      </label>
    </section>
  );
}

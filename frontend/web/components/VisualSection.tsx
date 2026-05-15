import type { Scene } from "../lib/types";

type VisualSectionProps = {
  scene: Scene;
};

export function VisualSection({ scene }: VisualSectionProps) {
  return (
    <section className="scene-section">
      <h3>시각 자료</h3>
      <dl className="field-list">
        <div>
          <dt>유형</dt>
          <dd>{scene.visual_asset_type || "-"}</dd>
        </div>
        <div>
          <dt>설명</dt>
          <dd>{scene.visual_description || "-"}</dd>
        </div>
        <div>
          <dt>GIF/클립</dt>
          <dd>{scene.gif_or_clip_suggestion || "-"}</dd>
        </div>
      </dl>
      <div className="keyword-list">
        {scene.stock_search_keywords.length ? (
          scene.stock_search_keywords.map((keyword) => (
            <span className="keyword" key={keyword}>
              {keyword}
            </span>
          ))
        ) : (
          <span className="keyword empty">키워드 없음</span>
        )}
      </div>
      <details className="prompt-details">
        <summary>생성 이미지 프롬프트</summary>
        <pre>{scene.generated_image_prompt || "-"}</pre>
      </details>
    </section>
  );
}

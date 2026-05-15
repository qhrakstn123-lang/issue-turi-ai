import { AssetCandidateRegister } from "./AssetCandidateRegister";
import type { AssetSourceCandidate, GenerationResult } from "../lib/types";

type TimelinePanelProps = {
  result: GenerationResult;
  assetSourceCandidates: AssetSourceCandidate[];
  onAddAssetCandidate: (candidate: Omit<AssetSourceCandidate, "asset_candidate_id">) => void;
  onUpdateAssetCandidate: (assetCandidateId: string, updates: Partial<AssetSourceCandidate>) => void;
  onDeleteAssetCandidate: (assetCandidateId: string) => void;
};

function formatTime(seconds: number) {
  return `${seconds.toFixed(1)}s`;
}

export function TimelinePanel({
  result,
  assetSourceCandidates,
  onAddAssetCandidate,
  onUpdateAssetCandidate,
  onDeleteAssetCandidate,
}: TimelinePanelProps) {
  const timeline = result.timeline;

  return (
    <section className="timeline-panel" aria-label="제작 타임라인">
      <div className="panel-heading compact">
        <div>
          <p className="eyebrow">타임라인 빌더</p>
          <h3>제작 타이밍</h3>
        </div>
        <span className="status-pill muted">{formatTime(timeline.total_duration)}</span>
      </div>

      <div className="timeline-meta">
        <span>{timeline.aspect_ratio}</span>
        <span>{timeline.resolution}</span>
        <span>{timeline.fps}fps</span>
      </div>

      <ol className="timeline-list">
        {timeline.scenes.map((scene) => {
          const beats = scene.beats ?? [];
          const assetReviewChecklist = scene.asset_review_checklist ?? [];
          const sourceScene = result.storyboard.scenes.find((storyboardScene) => storyboardScene.scene_id === scene.scene_id);
          const sceneCandidates = assetSourceCandidates.filter((candidate) => candidate.scene_id === scene.scene_id);

          return (
            <li className="timeline-item" key={scene.scene_id}>
              <div className="timeline-time">
                <strong>
                  {formatTime(scene.start_time)} - {formatTime(scene.end_time)}
                </strong>
                <span>{formatTime(scene.duration)}</span>
              </div>
              <div className="timeline-copy">
                <strong>{scene.scene_id}</strong>
                <span>{scene.subtitle.text}</span>
                <small>
                  {scene.motion} / {scene.transition} / {scene.sound_effect.type}
                </small>
              </div>

              <details className="timeline-details">
                <summary>제작 beat {beats.length}</summary>
                <div className="beat-list">
                  {beats.length ? (
                    beats.map((beat) => (
                      <div className="beat-item" key={`${scene.scene_id}-${beat.beat_type}-${beat.start_time}`}>
                        <strong>{beat.beat_type}</strong>
                        <span>
                          {formatTime(beat.start_time)} - {formatTime(beat.end_time)}
                        </span>
                        <p>{beat.text}</p>
                        <small>
                          motion: {beat.motion} / sound: {beat.sound_effect}
                        </small>
                        <em>{beat.note}</em>
                      </div>
                    ))
                  ) : (
                    <p className="muted-copy">등록된 beat가 없습니다.</p>
                  )}
                </div>
              </details>

              <details className="timeline-details">
                <summary>asset review checklist {assetReviewChecklist.length}</summary>
                <ul className="timeline-checklist">
                  {assetReviewChecklist.length ? (
                    assetReviewChecklist.map((item) => <li key={item}>{item}</li>)
                  ) : (
                    <li>추가 확인 항목 없음</li>
                  )}
                </ul>
                <AssetCandidateRegister
                  scene={sourceScene}
                  sceneId={scene.scene_id}
                  candidates={sceneCandidates}
                  onAddCandidate={onAddAssetCandidate}
                  onUpdateCandidate={onUpdateAssetCandidate}
                  onDeleteCandidate={onDeleteAssetCandidate}
                />
              </details>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

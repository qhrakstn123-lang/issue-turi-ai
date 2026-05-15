import type { GenerationResult } from "../lib/types";

type TimelinePanelProps = {
  result: GenerationResult;
};

function formatTime(seconds: number) {
  return `${seconds.toFixed(1)}s`;
}

export function TimelinePanel({ result }: TimelinePanelProps) {
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
        {timeline.scenes.map((scene) => (
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
              <summary>제작 beat {scene.beats.length}</summary>
              <div className="beat-list">
                {scene.beats.length ? (
                  scene.beats.map((beat) => (
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
              <summary>asset review checklist {scene.asset_review_checklist.length}</summary>
              <ul className="timeline-checklist">
                {scene.asset_review_checklist.length ? (
                  scene.asset_review_checklist.map((item) => <li key={item}>{item}</li>)
                ) : (
                  <li>추가 확인 항목 없음</li>
                )}
              </ul>
            </details>
          </li>
        ))}
      </ol>
    </section>
  );
}

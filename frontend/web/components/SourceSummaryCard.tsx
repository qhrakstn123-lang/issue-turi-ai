import type { SourceBrief } from "../lib/types";

type SourceSummaryCardProps = {
  sourceBrief: SourceBrief | null;
};

export function SourceSummaryCard({ sourceBrief }: SourceSummaryCardProps) {
  if (!sourceBrief) {
    return null;
  }

  return (
    <section className="source-summary-card" aria-label="소스 요약">
      <div className="source-summary-heading">
        <span className="eyebrow">Source Summary</span>
        <strong>{sourceBrief.source_title || "소스 기반 기획"}</strong>
      </div>
      <dl>
        <div>
          <dt>source_type</dt>
          <dd>{sourceBrief.source_type}</dd>
        </div>
        {sourceBrief.source_url ? (
          <div>
            <dt>source_url</dt>
            <dd>{sourceBrief.source_url}</dd>
          </div>
        ) : null}
        {sourceBrief.source_angle ? (
          <div>
            <dt>source_angle</dt>
            <dd>{sourceBrief.source_angle}</dd>
          </div>
        ) : null}
        {sourceBrief.source_context ? (
          <div>
            <dt>source_context</dt>
            <dd>{sourceBrief.source_context}</dd>
          </div>
        ) : null}
      </dl>
      <p>외부 URL은 자동으로 읽지 않았습니다. 사용자가 제공한 소스 메타데이터와 맥락은 기획 참고용으로만 분리해 표시합니다.</p>
    </section>
  );
}

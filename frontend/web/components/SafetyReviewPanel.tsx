import type { GenerationResult } from "../lib/types";

type SafetyReviewPanelProps = {
  result: GenerationResult;
};

const riskGroups = [
  ["안전성 메모", "safety_notes"],
  ["저작권 위험", "copyright_risks"],
  ["루머/명예훼손 위험", "rumor_or_defamation_risks"],
  ["개인정보/초상권 위험", "privacy_or_portrait_risks"],
  ["출처 사용 위험", "source_usage_risks"],
] as const;

export function SafetyReviewPanel({ result }: SafetyReviewPanelProps) {
  return (
    <section className={result.required_human_review ? "safety-review safety-warn" : "safety-review"}>
      <div className="safety-heading">
        <h2>안전성 검토</h2>
        <span className={result.required_human_review ? "review-flag warn" : "review-flag"}>
          {result.required_human_review ? "사람 검토 필요" : "사람 검토 플래그 없음"}
        </span>
      </div>

      {riskGroups.map(([title, field]) => (
        <details className="risk-details" key={field} open={result[field].length > 0 || field === "safety_notes"}>
          <summary>
            {title} ({result[field].length})
          </summary>
          <ul className="risk-list">
            {result[field].length ? (
              result[field].map((item) => <li key={item}>{item}</li>)
            ) : (
              <li>없음</li>
            )}
          </ul>
        </details>
      ))}

      <section className="revision-box">
        <h3>권장 수정사항</h3>
        <ul className="risk-list">
          {result.recommended_revisions.length ? (
            result.recommended_revisions.map((item) => <li key={item}>{item}</li>)
          ) : (
            <li>수정 제안 없음</li>
          )}
        </ul>
      </section>
    </section>
  );
}

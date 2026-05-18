import type { SourceCapturePlan } from "../lib/types";

type SourceCapturePlanListProps = {
  plans: SourceCapturePlan[];
  sceneId: string;
};

export function SourceCapturePlanList({ plans, sceneId }: SourceCapturePlanListProps) {
  const plan = plans.find((candidate) => candidate.scene_id === sceneId);
  if (!plan) {
    return null;
  }

  return (
    <div className="source-capture-plan-card">
      <div className="source-capture-plan-heading">
        <strong>Source Capture Plan</strong>
        <div className="capture-plan-badges">
          <span className="capture-plan-badge priority">원본 소스 우선</span>
          <span className="capture-plan-badge">source-first priority</span>
          <span className={plan.primary_asset_plan === "source_capture" ? "capture-plan-badge strong" : "capture-plan-badge"}>
            {plan.primary_asset_plan}
          </span>
        </div>
      </div>
      <dl>
        <div>
          <dt>capture_target</dt>
          <dd>{plan.capture_target}</dd>
        </div>
        <div>
          <dt>fallback_asset_plan</dt>
          <dd className={plan.fallback_asset_plan === "mockup_rewrite" ? "attention-copy" : undefined}>
            {plan.fallback_asset_plan}
          </dd>
        </div>
        <div>
          <dt>backup_asset_plan</dt>
          <dd>{plan.backup_asset_plan}</dd>
        </div>
        <div>
          <dt>ai_image_needed</dt>
          <dd>{plan.ai_image_needed ? "yes" : "no"}</dd>
        </div>
      </dl>
      <p className="source-review-note">{plan.source_review_note}</p>
    </div>
  );
}

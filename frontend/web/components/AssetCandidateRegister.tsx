"use client";

import { useState } from "react";
import type { AssetLicenseStatus, AssetSourceCandidate, AssetSourceType, Scene } from "../lib/types";
import {
  applyLicenseStatusSafetyPreset,
  applySourceTypeSafetyPreset,
  buildSafeAssetCandidateDraft,
  type AssetCandidateManualOverride,
  type AssetCandidateSafetyState,
} from "../lib/assetCandidateSafety";

type CandidateDraft = Omit<AssetSourceCandidate, "asset_candidate_id">;

type AssetCandidateRegisterProps = {
  scene: Scene | undefined;
  sceneId: string;
  candidates: AssetSourceCandidate[];
  onAddCandidate: (candidate: CandidateDraft) => void;
  onUpdateCandidate: (assetCandidateId: string, updates: Partial<AssetSourceCandidate>) => void;
  onDeleteCandidate: (assetCandidateId: string) => void;
};

const sourceTypeOptions: AssetSourceType[] = [
  "community",
  "news",
  "youtube",
  "broadcast",
  "instagram",
  "google_image",
  "stock_site",
  "ai_generated",
  "user_provided",
  "mockup",
];

const licenseStatusOptions: AssetLicenseStatus[] = [
  "unchecked",
  "license_required",
  "permission_required",
  "cleared",
  "avoid",
];

export function AssetCandidateRegister({
  scene,
  sceneId,
  candidates,
  onAddCandidate,
  onUpdateCandidate,
  onDeleteCandidate,
}: AssetCandidateRegisterProps) {
  const [sourceType, setSourceType] = useState<AssetSourceType>(defaultSourceType(scene?.capture_source_type));
  const [licenseStatus, setLicenseStatus] = useState<AssetLicenseStatus>(
    defaultLicenseStatus(scene?.capture_usage_mode),
  );
  const [sourceUrl, setSourceUrl] = useState("");
  const [sourceTitle, setSourceTitle] = useState("");
  const [reviewNotes, setReviewNotes] = useState(scene?.asset_usage_note || "");
  const [needsBlur, setNeedsBlur] = useState(false);
  const [needsRewrite, setNeedsRewrite] = useState(false);
  const [approvedForUse, setApprovedForUse] = useState(false);
  const [manualOverride, setManualOverride] = useState<AssetCandidateManualOverride>({});

  function currentSafetyState(): AssetCandidateSafetyState {
    return {
      source_type: sourceType,
      license_status: licenseStatus,
      needs_blur: needsBlur,
      needs_rewrite: needsRewrite,
      approved_for_use: approvedForUse,
      review_notes: reviewNotes,
    };
  }

  function applySafetyState(next: AssetCandidateSafetyState) {
    setSourceType(next.source_type);
    setLicenseStatus(next.license_status);
    setNeedsBlur(next.needs_blur);
    setNeedsRewrite(next.needs_rewrite);
    setApprovedForUse(next.approved_for_use);
    setReviewNotes(next.review_notes);
  }

  function handleSourceTypeChange(value: AssetSourceType) {
    applySafetyState(applySourceTypeSafetyPreset(currentSafetyState(), value, manualOverride));
  }

  function handleLicenseStatusChange(value: AssetLicenseStatus) {
    setManualOverride((current) => ({ ...current, license_status: true }));
    applySafetyState(applyLicenseStatusSafetyPreset(currentSafetyState(), value, manualOverride));
  }

  function handleAddCandidate() {
    const safeCandidate = buildSafeAssetCandidateDraft({
      scene_id: sceneId,
      source_type: sourceType,
      source_url: sourceUrl.trim(),
      source_title: sourceTitle.trim() || `${sceneId} 자료 후보`,
      usage_mode: scene?.capture_usage_mode || "manual_review",
      license_status: licenseStatus,
      needs_blur: needsBlur,
      needs_rewrite: needsRewrite,
      approved_for_use: approvedForUse,
      review_notes: reviewNotes.trim(),
    });
    onAddCandidate(safeCandidate);
    setSourceUrl("");
    setSourceTitle("");
    setApprovedForUse(false);
  }

  return (
    <section className="asset-candidate-register" aria-label={`${sceneId} 자료 후보 등록`}>
      <div className="asset-register-heading">
        <div>
          <strong>자료 후보 등록</strong>
          <span>{candidates.length}개 후보</span>
        </div>
        <button className="compact-button" type="button" onClick={handleAddCandidate}>
          추가
        </button>
      </div>

      <div className="asset-register-form">
        <label>
          종류
          <select value={sourceType} onChange={(event) => handleSourceTypeChange(event.target.value as AssetSourceType)}>
            {sourceTypeOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
        <label>
          권리 상태
          <select
            value={licenseStatus}
            onChange={(event) => handleLicenseStatusChange(event.target.value as AssetLicenseStatus)}
          >
            {licenseStatusOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
        <label>
          제목
          <input value={sourceTitle} onChange={(event) => setSourceTitle(event.target.value)} />
        </label>
        <label>
          URL 선택
          <input value={sourceUrl} onChange={(event) => setSourceUrl(event.target.value)} />
        </label>
      </div>

      {isRiskySourceType(sourceType) ? (
        <p className="asset-risk-hint">권리/개인정보 검토가 필요한 자료 유형입니다.</p>
      ) : null}

      <div className="asset-register-checks">
        <label>
          <input
            type="checkbox"
            checked={needsBlur}
            onChange={(event) => {
              setManualOverride((current) => ({ ...current, needs_blur: true }));
              setNeedsBlur(event.target.checked);
            }}
          />
          블러 필요
        </label>
        <label>
          <input
            type="checkbox"
            checked={needsRewrite}
            onChange={(event) => {
              setManualOverride((current) => ({ ...current, needs_rewrite: true }));
              setNeedsRewrite(event.target.checked);
            }}
          />
          재작성 필요
        </label>
        <label>
          <input
            type="checkbox"
            checked={licenseStatus === "avoid" ? false : approvedForUse}
            disabled={licenseStatus === "avoid"}
            onChange={(event) => {
              setManualOverride((current) => ({ ...current, approved_for_use: true }));
              setApprovedForUse(event.target.checked);
            }}
          />
          사용 승인
        </label>
      </div>

      <label className="asset-notes-field">
        검토 메모
        <textarea
          rows={3}
          value={reviewNotes}
          onChange={(event) => {
            setManualOverride((current) => ({ ...current, review_notes: true }));
            setReviewNotes(event.target.value);
          }}
        />
      </label>

      <div className="asset-candidate-list">
        {candidates.length ? (
          candidates.map((candidate) => (
            <article className="asset-candidate-card" key={candidate.asset_candidate_id}>
              <div className="asset-candidate-topline">
                <strong>{candidate.source_title || "제목 없음"}</strong>
                <button
                  className="link-button"
                  type="button"
                  onClick={() => onDeleteCandidate(candidate.asset_candidate_id)}
                >
                  삭제
                </button>
              </div>
              <div className="asset-candidate-badges">
                <span className={isRiskySourceType(candidate.source_type) ? "risk-source-badge" : ""}>
                  {candidate.source_type}
                </span>
                <span className={isRiskyLicense(candidate.license_status) ? "risk-badge" : ""}>
                  {candidate.license_status}
                </span>
                <span className={candidate.approved_for_use ? "approved-badge" : "review-badge"}>
                  {candidate.approved_for_use ? "사용 가능" : "검토 필요"}
                </span>
              </div>
              {candidate.source_url ? <p className="asset-url">{candidate.source_url}</p> : null}
              {candidate.review_notes ? <p>{candidate.review_notes}</p> : null}
              <div className="asset-register-checks">
                <label>
                  <input
                    type="checkbox"
                    checked={candidate.needs_blur}
                    onChange={(event) =>
                      onUpdateCandidate(candidate.asset_candidate_id, { needs_blur: event.target.checked })
                    }
                  />
                  블러
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={candidate.needs_rewrite}
                    onChange={(event) =>
                      onUpdateCandidate(candidate.asset_candidate_id, { needs_rewrite: event.target.checked })
                    }
                  />
                  재작성
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={candidate.license_status === "avoid" ? false : candidate.approved_for_use}
                    disabled={candidate.license_status === "avoid"}
                    onChange={(event) =>
                      onUpdateCandidate(candidate.asset_candidate_id, {
                        approved_for_use: candidate.license_status === "avoid" ? false : event.target.checked,
                      })
                    }
                  />
                  승인
                </label>
              </div>
            </article>
          ))
        ) : (
          <p className="muted-copy">등록된 자료 후보가 없습니다.</p>
        )}
      </div>
    </section>
  );
}

function defaultSourceType(value: string | undefined): AssetSourceType {
  if (value && sourceTypeOptions.includes(value as AssetSourceType)) {
    return value as AssetSourceType;
  }
  return "mockup";
}

function defaultLicenseStatus(value: string | undefined): AssetLicenseStatus {
  if (value === "license_required" || value === "permission_required" || value === "avoid") {
    return value;
  }
  return "unchecked";
}

function isRiskyLicense(value: AssetLicenseStatus) {
  return value === "permission_required" || value === "license_required" || value === "avoid";
}

function isRiskySourceType(value: AssetSourceType) {
  return (
    value === "community" ||
    value === "instagram" ||
    value === "news" ||
    value === "youtube" ||
    value === "broadcast" ||
    value === "google_image"
  );
}

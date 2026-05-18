import type { AssetLicenseStatus, AssetSourceCandidate, AssetSourceType } from "./types";

export type AssetCandidateSafetyState = Pick<
  AssetSourceCandidate,
  "source_type" | "license_status" | "needs_blur" | "needs_rewrite" | "approved_for_use" | "review_notes"
>;

export type AssetCandidateManualOverride = Partial<Record<keyof AssetCandidateSafetyState, boolean>>;

type AssetCandidateSafetyPreset = Partial<AssetCandidateSafetyState>;

const COMMUNITY_REVIEW_NOTE =
  "닉네임, 프로필 이미지, 댓글 원문, 개인정보를 가리고 사용 여부를 확인하세요. 원문 캡처 대신 mockup/rewrite 사용을 우선 검토하세요.";

const RIGHTS_CAPTURE_REVIEW_NOTE =
  "로고, 화면 캡처 권리, 출처, 허가 필요 여부를 확인하세요. 가능하면 직접 제작한 요약 화면이나 mockup으로 대체하세요.";

const GOOGLE_IMAGE_REVIEW_NOTE = "이미지 라이선스와 원본 출처를 확인하세요. 사용권이 불명확하면 사용하지 마세요.";

const AI_GENERATED_REVIEW_NOTE = "실존 인물 오인, 브랜드/캐릭터 유사성, 허위 사실 암시 여부를 확인하세요.";

const USER_PROVIDED_REVIEW_NOTE = "직접 소유하거나 사용 허가를 받은 자료인지 확인하세요.";

const AVOID_REVIEW_NOTE = "사용 금지 또는 대체 필요";

export function getSourceTypeSafetyPreset(source_type: AssetSourceType): AssetCandidateSafetyPreset {
  if (source_type === "community" || source_type === "instagram") {
    return {
      source_type,
      needs_blur: true,
      needs_rewrite: true,
      approved_for_use: false,
      review_notes: COMMUNITY_REVIEW_NOTE,
    };
  }

  if (source_type === "news" || source_type === "youtube" || source_type === "broadcast") {
    return {
      source_type,
      needs_blur: true,
      needs_rewrite: false,
      approved_for_use: false,
      license_status: "permission_required",
      review_notes: RIGHTS_CAPTURE_REVIEW_NOTE,
    };
  }

  if (source_type === "google_image") {
    return {
      source_type,
      license_status: "license_required",
      approved_for_use: false,
      review_notes: GOOGLE_IMAGE_REVIEW_NOTE,
    };
  }

  if (source_type === "ai_generated") {
    return {
      source_type,
      needs_blur: false,
      needs_rewrite: false,
      license_status: "unchecked",
      approved_for_use: false,
      review_notes: AI_GENERATED_REVIEW_NOTE,
    };
  }

  if (source_type === "user_provided") {
    return {
      source_type,
      license_status: "unchecked",
      approved_for_use: false,
      review_notes: USER_PROVIDED_REVIEW_NOTE,
    };
  }

  return { source_type };
}

export function applySourceTypeSafetyPreset(
  current: AssetCandidateSafetyState,
  source_type: AssetSourceType,
  manualOverride: AssetCandidateManualOverride = {},
): AssetCandidateSafetyState {
  const preset = getSourceTypeSafetyPreset(source_type);
  return {
    ...current,
    source_type,
    license_status: manualOverride.license_status
      ? current.license_status
      : preset.license_status ?? current.license_status,
    needs_blur: manualOverride.needs_blur ? current.needs_blur : preset.needs_blur ?? current.needs_blur,
    needs_rewrite: manualOverride.needs_rewrite
      ? current.needs_rewrite
      : preset.needs_rewrite ?? current.needs_rewrite,
    approved_for_use:
      preset.approved_for_use === false
        ? false
        : manualOverride.approved_for_use
          ? current.approved_for_use
          : preset.approved_for_use ?? current.approved_for_use,
    review_notes: manualOverride.review_notes
      ? current.review_notes
      : appendReviewNote(current.review_notes, preset.review_notes),
  };
}

export function applyLicenseStatusSafetyPreset(
  current: AssetCandidateSafetyState,
  license_status: AssetLicenseStatus,
  manualOverride: AssetCandidateManualOverride = {},
): AssetCandidateSafetyState {
  if (license_status === "avoid") {
    return {
      ...current,
      license_status,
      approved_for_use: false,
      review_notes: appendReviewNote(current.review_notes, AVOID_REVIEW_NOTE),
    };
  }

  return {
    ...current,
    license_status,
    approved_for_use: manualOverride.approved_for_use ? current.approved_for_use : current.approved_for_use,
  };
}

export function buildSafeAssetCandidateDraft<T extends AssetCandidateSafetyState>(candidate: T): T {
  if (candidate.license_status !== "avoid") {
    return candidate;
  }
  return {
    ...candidate,
    approved_for_use: false,
    review_notes: appendReviewNote(candidate.review_notes, AVOID_REVIEW_NOTE),
  };
}

function appendReviewNote(current: string, note: string | undefined) {
  const trimmed = current.trim();
  if (!note) {
    return trimmed;
  }
  if (trimmed.includes(note)) {
    return trimmed;
  }
  return trimmed ? `${trimmed}\n${note}` : note;
}

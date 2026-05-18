import type {
  AssetSourceType,
  BackupAssetPlan,
  FallbackAssetPlan,
  PrimaryAssetPlan,
  Scene,
  SourceBrief,
  SourceCapturePlan,
} from "./types";

type ScenePurpose =
  | "hook"
  | "context"
  | "reaction"
  | "key_issue"
  | "turning_point"
  | "conclusion"
  | "comment_cta"
  | "other";

export function buildSourceCapturePlans(scenes: Scene[], sourceBrief: SourceBrief | null): SourceCapturePlan[] {
  if (!sourceBrief) {
    return [];
  }
  return scenes.map((scene) => buildSourceCapturePlan(scene, sourceBrief));
}

function buildSourceCapturePlan(scene: Scene, sourceBrief: SourceBrief): SourceCapturePlan {
  const purpose = normalizeScenePurpose(scene.scene_purpose);
  if (sourceBrief.source_type === "community" || sourceBrief.source_type === "instagram") {
    return buildCommunityPlan(scene, sourceBrief, purpose);
  }
  if (isPermissionSource(sourceBrief.source_type)) {
    return buildPermissionSourcePlan(scene, sourceBrief, purpose);
  }
  if (sourceBrief.source_type === "google_image") {
    return buildGoogleImagePlan(scene, sourceBrief, purpose);
  }
  if (sourceBrief.source_type === "user_provided") {
    return buildGenericPlan(scene, sourceBrief, purpose, "user_provided", "text_card", "licensed_stock", false);
  }
  if (sourceBrief.source_type === "ai_generated") {
    return buildGenericPlan(scene, sourceBrief, purpose, "ai_generated_background", "text_card", "licensed_stock", true);
  }
  if (sourceBrief.source_type === "stock_site") {
    return buildGenericPlan(scene, sourceBrief, purpose, "licensed_stock", "text_card", "user_provided", false);
  }
  return buildGenericPlan(scene, sourceBrief, purpose, "mockup_rewrite", "text_card", "licensed_stock", false);
}

function buildCommunityPlan(scene: Scene, sourceBrief: SourceBrief, purpose: ScenePurpose): SourceCapturePlan {
  const useSourceCapture = purpose === "hook" || purpose === "context" || purpose === "reaction";
  return {
    scene_id: scene.scene_id,
    primary_asset_plan: useSourceCapture ? "source_capture" : primaryForPurpose(purpose),
    capture_target: communityCaptureTarget(sourceBrief, purpose),
    fallback_asset_plan: "mockup_rewrite",
    backup_asset_plan: "text_card",
    ai_image_needed: false,
    source_review_note:
      "닉네임, 프로필 이미지, 댓글 원문, 개인정보, 명예훼손 위험 확인이 필요합니다. 원문 캡처 대신 blur/mockup/rewrite 사용을 우선 검토하세요.",
  };
}

function buildPermissionSourcePlan(scene: Scene, sourceBrief: SourceBrief, purpose: ScenePurpose): SourceCapturePlan {
  const sourceCapturePurpose = purpose === "hook" || purpose === "context" || purpose === "turning_point";
  return {
    scene_id: scene.scene_id,
    primary_asset_plan: sourceCapturePurpose ? "source_capture" : "mockup_rewrite",
    capture_target: permissionCaptureTarget(sourceBrief, purpose),
    fallback_asset_plan: purpose === "key_issue" || purpose === "conclusion" || purpose === "comment_cta" ? "text_card" : "mockup_rewrite",
    backup_asset_plan: "licensed_stock",
    ai_image_needed: false,
    source_review_note:
      "로고, 화면 캡처 권리, 출처, 허가 필요 여부 확인이 필요합니다. 가능하면 자체 요약 카드나 mockup으로 대체하세요.",
  };
}

function buildGoogleImagePlan(scene: Scene, sourceBrief: SourceBrief, purpose: ScenePurpose): SourceCapturePlan {
  return {
    scene_id: scene.scene_id,
    primary_asset_plan: "licensed_stock",
    capture_target: sourceBrief.source_title || captureTargetForPurpose(purpose),
    fallback_asset_plan: "text_card",
    backup_asset_plan: "google_image_reference",
    ai_image_needed: purpose === "context" || purpose === "turning_point",
    source_review_note:
      "Google 이미지는 원본 출처와 라이선스 확인 전까지 사용 후보일 뿐입니다. 자동 캡처나 사용 승인으로 보지 마세요.",
  };
}

function buildGenericPlan(
  scene: Scene,
  sourceBrief: SourceBrief,
  purpose: ScenePurpose,
  primary_asset_plan: PrimaryAssetPlan,
  fallback_asset_plan: FallbackAssetPlan,
  backup_asset_plan: BackupAssetPlan,
  ai_image_needed: boolean,
): SourceCapturePlan {
  return {
    scene_id: scene.scene_id,
    primary_asset_plan: purpose === "conclusion" || purpose === "comment_cta" ? "text_card" : primary_asset_plan,
    capture_target: sourceBrief.source_title || captureTargetForPurpose(purpose),
    fallback_asset_plan,
    backup_asset_plan,
    ai_image_needed,
    source_review_note: "소스 권리, 출처, 개인정보, 초상권, 맥락 왜곡 위험을 확인하세요.",
  };
}

function normalizeScenePurpose(scenePurpose: string): ScenePurpose {
  const normalized = scenePurpose.toLowerCase();
  if (normalized.includes("hook")) return "hook";
  if (normalized.includes("context")) return "context";
  if (normalized.includes("reaction")) return "reaction";
  if (normalized.includes("key_issue") || normalized.includes("issue")) return "key_issue";
  if (normalized.includes("turning")) return "turning_point";
  if (normalized.includes("conclusion")) return "conclusion";
  if (normalized.includes("comment") || normalized.includes("cta")) return "comment_cta";
  return "other";
}

function isPermissionSource(sourceType: AssetSourceType) {
  return sourceType === "news" || sourceType === "youtube" || sourceType === "broadcast";
}

function primaryForPurpose(purpose: ScenePurpose): PrimaryAssetPlan {
  if (purpose === "key_issue" || purpose === "turning_point") return "mockup_rewrite";
  if (purpose === "conclusion" || purpose === "comment_cta") return "text_card";
  return "source_capture";
}

function communityCaptureTarget(sourceBrief: SourceBrief, purpose: ScenePurpose) {
  const title = sourceBrief.source_title || "원본 커뮤니티/인스타 자료";
  if (purpose === "hook") return `${title}의 게시글 제목 또는 핵심 논쟁 캡처 후보`;
  if (purpose === "context") return `${title}의 게시글 상단과 사건 요약 맥락`;
  if (purpose === "reaction") return `${title}의 핵심 반응 영역과 댓글 반응 흐름`;
  if (purpose === "key_issue") return "쟁점 비교 text card 또는 커뮤니티 mockup";
  if (purpose === "turning_point") return "추가 맥락 또는 반전 근거 화면";
  if (purpose === "conclusion") return "요약 text card";
  if (purpose === "comment_cta") return "댓글 유도 text card";
  return `${title}의 핵심 반응 영역`;
}

function permissionCaptureTarget(sourceBrief: SourceBrief, purpose: ScenePurpose) {
  const title = sourceBrief.source_title || "원본 자료";
  if (purpose === "hook") return `${title}의 제목/대표 장면 캡처 후보`;
  if (purpose === "context") return `${title}의 사건 요약 카드 또는 원본 화면 상단`;
  if (purpose === "reaction") return "시청자 반응을 직접 캡처하지 않고 요약 text card";
  if (purpose === "key_issue") return "쟁점 비교 text card 또는 mockup";
  if (purpose === "turning_point") return "추가 맥락/반전 근거 화면";
  if (purpose === "conclusion") return "요약 text card";
  if (purpose === "comment_cta") return "댓글 유도 text card";
  return `${title}의 출처 확인 가능한 핵심 화면`;
}

function captureTargetForPurpose(purpose: ScenePurpose) {
  if (purpose === "hook") return "게시글 제목/핵심 논쟁 캡처 후보";
  if (purpose === "context") return "사건 요약 카드 또는 원본 게시글 상단";
  if (purpose === "reaction") return "댓글 반응/커뮤니티 반응 영역";
  if (purpose === "key_issue") return "쟁점 비교 text card 또는 mockup";
  if (purpose === "turning_point") return "추가 맥락/반전 근거 화면";
  if (purpose === "conclusion") return "요약 text card";
  if (purpose === "comment_cta") return "댓글 유도 text card";
  return "scene 핵심 설명 text card";
}

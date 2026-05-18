"use client";

import { useState } from "react";
import { JsonDownloadButton } from "../components/JsonDownloadButton";
import { ProjectForm } from "../components/ProjectForm";
import { ResultSummary } from "../components/ResultSummary";
import { SafetyReviewPanel } from "../components/SafetyReviewPanel";
import { SceneCard } from "../components/SceneCard";
import { TimelinePanel } from "../components/TimelinePanel";
import { createProject, generateShortsPlan } from "../lib/api";
import { applySourceTypeSafetyPreset, buildSafeAssetCandidateDraft } from "../lib/assetCandidateSafety";
import { normalizeGenerationResult } from "../lib/normalize";
import type { AssetSourceCandidate, GenerationResult, ProjectPayload, Scene, SourceBrief, TimelineScene } from "../lib/types";
import type { SceneEditablePatch } from "../components/SceneEditor";

const menuItems = [
  "홈",
  "프로젝트",
  "템플릿",
  "AI 아이디어",
  "대본 & 훅",
  "장면",
  "에셋",
  "분석",
  "설정",
];

export default function HomePage() {
  const [result, setResult] = useState<GenerationResult | null>(null);
  const [originalResult, setOriginalResult] = useState<GenerationResult | null>(null);
  const [sourceBrief, setSourceBrief] = useState<SourceBrief | null>(null);
  const [assetSourceCandidates, setAssetSourceCandidates] = useState<AssetSourceCandidate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  async function handleGenerate(payload: ProjectPayload) {
    setIsGenerating(true);
    setError(null);
    setResult(null);
    setOriginalResult(null);
    setSourceBrief(payload.source_brief ?? null);
    setAssetSourceCandidates([]);
    try {
      const created = await createProject(buildSourceAwareProjectPayload(payload));
      const generated = await generateShortsPlan(created.project.project_id);
      const normalizedResult = normalizeGenerationResult(generated.result);
      setResult(normalizedResult);
      setOriginalResult(normalizedResult);
      if (payload.source_brief) {
        setAssetSourceCandidates([createInitialSourceCandidate(payload.source_brief, normalizedResult)]);
      }
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "요청에 실패했습니다.");
    } finally {
      setIsGenerating(false);
    }
  }

  function onAddAssetCandidate(candidate: Omit<AssetSourceCandidate, "asset_candidate_id">) {
    setAssetSourceCandidates((current) => [
      ...current,
      {
        ...candidate,
        asset_candidate_id: createAssetCandidateId(),
      },
    ]);
  }

  function onUpdateAssetCandidate(assetCandidateId: string, updates: Partial<AssetSourceCandidate>) {
    setAssetSourceCandidates((current) =>
      current.map((candidate) =>
        candidate.asset_candidate_id === assetCandidateId ? { ...candidate, ...updates } : candidate,
      ),
    );
  }

  function onDeleteAssetCandidate(assetCandidateId: string) {
    setAssetSourceCandidates((current) =>
      current.filter((candidate) => candidate.asset_candidate_id !== assetCandidateId),
    );
  }

  function onUpdateScene(sceneId: string, updates: SceneEditablePatch) {
    setResult((current) => {
      if (!current) {
        return current;
      }
      const scenes = current.storyboard.scenes.map((scene) =>
        scene.scene_id === sceneId ? { ...scene, ...updates } : scene,
      );
      return rebuildResultWithScenes(current, scenes);
    });
  }

  function onResetScene(sceneId: string) {
    if (!originalResult) {
      return;
    }
    const originalScene = originalResult.storyboard.scenes.find((scene) => scene.scene_id === sceneId);
    if (!originalScene) {
      return;
    }
    setResult((current) => {
      if (!current) {
        return current;
      }
      const scenes = current.storyboard.scenes.map((scene) => (scene.scene_id === sceneId ? originalScene : scene));
      return rebuildResultWithScenes(current, scenes);
    });
  }

  function isSceneEdited(scene: Scene) {
    const originalScene = originalResult?.storyboard.scenes.find((candidate) => candidate.scene_id === scene.scene_id);
    return originalScene ? isEditableSceneChanged(scene, originalScene) : false;
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="ShortsFlow 탐색 메뉴">
        <div className="brand-block">
          <div className="brand-mark">SF</div>
          <div>
            <strong>ShortsFlow</strong>
            <span>AI 쇼츠 기획 스튜디오</span>
          </div>
        </div>

        <nav className="sidebar-nav" aria-label="미리보기 탐색 메뉴">
          {menuItems.map((item, index) => (
            <div className={index === 0 ? "nav-item active" : "nav-item"} key={item} aria-disabled={index !== 0}>
              <span className="nav-glyph">{item.slice(0, 1)}</span>
              <span>{item}</span>
              {index !== 0 ? <em>준비 중</em> : null}
            </div>
          ))}
        </nav>

        <div className="sidebar-card">
          <span className="eyebrow">현재 단계</span>
          <strong>기획 MVP</strong>
          <p>미리보기, 안전성 검토, 장면 카드, JSON 내보내기를 사용할 수 있습니다.</p>
        </div>
      </aside>

      <section className="studio-shell">
        <header className="topbar">
          <div className="search-box" aria-label="Search placeholder">
            <span>프로젝트, 템플릿, 아이디어 검색...</span>
            <kbd>K</kbd>
          </div>
          <div className="topbar-actions">
            <button className="ghost-button" type="button" disabled>
              새 프로젝트
            </button>
            <JsonDownloadButton
              result={result}
              assetSourceCandidates={assetSourceCandidates}
              sourceBrief={sourceBrief}
            />
            <span className={result && result.safety_status !== "approved" ? "status-pill warn" : "status-pill muted"}>
              {result?.safety_status || "검토 전"}
            </span>
          </div>
        </header>

        <section className="hero-panel">
          <div>
            <span className="eyebrow">ShortsFlow</span>
            <h1>AI 쇼츠 기획 스튜디오</h1>
            <p>더 잘 기획하고, 더 빠르게 만들고, 더 크게 성장하세요.</p>
            {sourceBrief ? <span className="source-first-badge">소스 기반 기획</span> : null}
          </div>
          <div className="hero-orbit" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
        </section>

        <section className="workspace">
          <ProjectForm isGenerating={isGenerating} onSubmit={handleGenerate} />

          <section className="result-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">프로젝트 작업실</p>
                <h2>{result?.video_script.title || "생성 결과"}</h2>
              </div>
            </div>

            {error ? <p className="error-box">{error}</p> : null}

            {result ? (
              <>
                <ResultSummary result={result} />
                <div className="editor-grid">
                  <div className="scene-list">
                    {result.storyboard.scenes.map((scene) => (
                      <SceneCard
                        key={scene.scene_id}
                        scene={scene}
                        isEdited={isSceneEdited(scene)}
                        onChangeScene={onUpdateScene}
                        onResetScene={onResetScene}
                      />
                    ))}
                  </div>
                  <aside className="review-column">
                    <TimelinePanel
                      result={result}
                      assetSourceCandidates={assetSourceCandidates}
                      onAddAssetCandidate={onAddAssetCandidate}
                      onUpdateAssetCandidate={onUpdateAssetCandidate}
                      onDeleteAssetCandidate={onDeleteAssetCandidate}
                      sourceBrief={sourceBrief}
                    />
                    <SafetyReviewPanel result={result} />
                    <div className="placeholder-card">
                      <span className="eyebrow">Preview</span>
                      <strong>영상 미리보기</strong>
                      <p>이미지 생성, TTS, MP4 렌더링은 준비 중입니다.</p>
                    </div>
                  </aside>
                </div>
              </>
            ) : (
              <div className="empty-state">
                <h2>쇼츠 기획을 시작해보세요</h2>
                <p>프로젝트를 생성하면 대본, 시각 자료 소싱, 편집 방향, 안전성 검토, JSON 내보내기를 확인할 수 있습니다.</p>
              </div>
            )}
          </section>
        </section>
      </section>
    </main>
  );
}

function buildSourceAwareProjectPayload(payload: ProjectPayload): ProjectPayload {
  if (!payload.source_brief) {
    return payload;
  }
  const sourceBrief = payload.source_brief;
  const sourceContext = [
    sourceBrief.source_title ? `소스 제목: ${sourceBrief.source_title}` : "",
    sourceBrief.source_context ? `소스 맥락: ${sourceBrief.source_context}` : "",
    sourceBrief.source_angle ? `쇼츠 관점: ${sourceBrief.source_angle}` : "",
    sourceBrief.source_url ? `사용자 제공 원본 링크: ${sourceBrief.source_url}` : "",
    "외부 URL 내용은 자동으로 읽지 않았고, 사용자가 제공한 소스 맥락만 반영한다.",
  ]
    .filter(Boolean)
    .join("\n");
  return {
    ...payload,
    topic: `${payload.topic}\n\n[소스 기반 기획]\n${sourceContext}`,
  };
}

function createInitialSourceCandidate(sourceBrief: SourceBrief, result: GenerationResult): AssetSourceCandidate {
  const sceneId = result.storyboard.scenes[0]?.scene_id || "scene_001";
  const safetyState = applySourceTypeSafetyPreset(
    {
      source_type: sourceBrief.source_type,
      license_status: "unchecked",
      needs_blur: false,
      needs_rewrite: false,
      approved_for_use: false,
      review_notes: sourceBrief.source_context || "",
    },
    sourceBrief.source_type,
  );
  return {
    ...buildSafeAssetCandidateDraft({
      scene_id: sceneId,
      asset_candidate_id: createAssetCandidateId(),
      source_type: safetyState.source_type,
      source_url: sourceBrief.source_url,
      source_title: sourceBrief.source_title || `${sceneId} 원본 소스 기반 캡처 후보`,
      usage_mode: "source_first_manual_review",
      license_status: safetyState.license_status,
      needs_blur: safetyState.needs_blur,
      needs_rewrite: safetyState.needs_rewrite,
      approved_for_use: false,
      review_notes: safetyState.review_notes,
    }),
  };
}

function rebuildResultWithScenes(result: GenerationResult, scenes: Scene[]): GenerationResult {
  return {
    ...result,
    storyboard: {
      ...result.storyboard,
      scenes,
    },
    timeline: rebuildTimelineForScenes(result, scenes),
  };
}

function rebuildTimelineForScenes(result: GenerationResult, scenes: Scene[]) {
  let cursor = 0;
  const timelineScenes = scenes.map((scene) => {
    const previousTimelineScene = result.timeline.scenes.find((candidate) => candidate.scene_id === scene.scene_id);
    const duration = scene.estimated_duration > 0 ? scene.estimated_duration : 1;
    const startTime = cursor;
    const endTime = startTime + duration;
    cursor = endTime;
    return rebuildTimelineScene(previousTimelineScene, scene, startTime, endTime, duration);
  });

  return {
    ...result.timeline,
    total_duration: cursor,
    scenes: timelineScenes,
  };
}

function rebuildTimelineScene(
  previousTimelineScene: TimelineScene | undefined,
  scene: Scene,
  startTime: number,
  endTime: number,
  duration: number,
): TimelineScene {
  const fallbackScene: TimelineScene = {
    scene_id: scene.scene_id,
    start_time: startTime,
    end_time: endTime,
    duration,
    visual_asset: {
      type: scene.visual_asset_type,
      url: scene.generated_image_url,
    },
    narration_audio: {
      url: null,
    },
    subtitle: {
      text: scene.subtitle,
      start_time: startTime,
      end_time: endTime,
    },
    emphasis_caption: {
      text: scene.emphasis_caption,
      start_time: startTime,
      end_time: endTime,
    },
    motion: scene.motion_direction,
    transition: scene.transition,
    sound_effect: {
      type: scene.sound_effect_hint,
      start_time: startTime,
    },
    beats: [],
    asset_review_checklist: [],
  };

  const source = previousTimelineScene ?? fallbackScene;
  const sourceBeats = source.beats ?? [];
  const previousDuration = source.duration > 0 ? source.duration : duration;

  return {
    ...source,
    scene_id: scene.scene_id,
    start_time: startTime,
    end_time: endTime,
    duration,
    visual_asset: {
      ...source.visual_asset,
      type: scene.visual_asset_type,
      url: scene.generated_image_url,
    },
    subtitle: {
      ...source.subtitle,
      text: scene.subtitle,
      start_time: startTime,
      end_time: endTime,
    },
    emphasis_caption: {
      ...source.emphasis_caption,
      text: scene.emphasis_caption,
      start_time: startTime,
      end_time: Math.min(endTime, startTime + Math.max(1, duration * 0.45)),
    },
    motion: scene.motion_direction,
    transition: scene.transition,
    sound_effect: {
      ...source.sound_effect,
      type: scene.sound_effect_hint,
      start_time: startTime,
    },
    beats: sourceBeats.map((beat) => {
      const relativeStart = (beat.start_time - source.start_time) / previousDuration;
      const relativeEnd = (beat.end_time - source.start_time) / previousDuration;
      return {
        ...beat,
        start_time: startTime + clampRatio(relativeStart) * duration,
        end_time: startTime + clampRatio(relativeEnd) * duration,
      };
    }),
    asset_review_checklist: source.asset_review_checklist ?? [],
  };
}

function isEditableSceneChanged(scene: Scene, originalScene: Scene) {
  return (
    scene.narration !== originalScene.narration ||
    scene.tts_text !== originalScene.tts_text ||
    scene.subtitle !== originalScene.subtitle ||
    scene.emphasis_caption !== originalScene.emphasis_caption ||
    scene.estimated_duration !== originalScene.estimated_duration ||
    scene.visual_description !== originalScene.visual_description ||
    scene.generated_image_prompt !== originalScene.generated_image_prompt ||
    scene.asset_usage_note !== originalScene.asset_usage_note ||
    scene.editing_notes !== originalScene.editing_notes
  );
}

function clampRatio(value: number) {
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.min(1, Math.max(0, value));
}

function createAssetCandidateId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `asset-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

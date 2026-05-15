"use client";

import { useState } from "react";
import { JsonDownloadButton } from "../components/JsonDownloadButton";
import { ProjectForm } from "../components/ProjectForm";
import { ResultSummary } from "../components/ResultSummary";
import { SafetyReviewPanel } from "../components/SafetyReviewPanel";
import { SceneCard } from "../components/SceneCard";
import { TimelinePanel } from "../components/TimelinePanel";
import { createProject, generateShortsPlan } from "../lib/api";
import type { AssetSourceCandidate, GenerationResult, ProjectPayload } from "../lib/types";

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
  const [assetSourceCandidates, setAssetSourceCandidates] = useState<AssetSourceCandidate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  async function handleGenerate(payload: ProjectPayload) {
    setIsGenerating(true);
    setError(null);
    setResult(null);
    setAssetSourceCandidates([]);
    try {
      const created = await createProject(payload);
      const generated = await generateShortsPlan(created.project.project_id);
      setResult(generated.result);
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
            <JsonDownloadButton result={result} assetSourceCandidates={assetSourceCandidates} />
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
                      <SceneCard key={scene.scene_id} scene={scene} />
                    ))}
                  </div>
                  <aside className="review-column">
                    <TimelinePanel
                      result={result}
                      assetSourceCandidates={assetSourceCandidates}
                      onAddAssetCandidate={onAddAssetCandidate}
                      onUpdateAssetCandidate={onUpdateAssetCandidate}
                      onDeleteAssetCandidate={onDeleteAssetCandidate}
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

function createAssetCandidateId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `asset-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

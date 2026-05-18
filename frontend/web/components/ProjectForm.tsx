"use client";

import type { FormEvent } from "react";
import type { AssetSourceType, ProjectPayload, SourceBrief } from "../lib/types";

type ProjectFormProps = {
  isGenerating: boolean;
  onSubmit: (payload: ProjectPayload) => void;
};

export function ProjectForm({ isGenerating, onSubmit }: ProjectFormProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const sourceBrief = buildSourceBrief(formData);
    onSubmit({
      topic: String(formData.get("topic") || "").trim(),
      target_audience: String(formData.get("target_audience") || "").trim(),
      tone: String(formData.get("tone") || "").trim(),
      style_template_id: String(formData.get("style_template_id") || "issue_turi_basic"),
      video_length_seconds: Number(formData.get("video_length_seconds") || 50),
      output_format: "youtube_shorts",
      ...(sourceBrief ? { source_brief: sourceBrief } : {}),
    });
  }

  return (
    <form className="input-panel" onSubmit={handleSubmit}>
      <div className="panel-heading">
        <h1>이슈털이 쇼츠 플래너</h1>
        <span className="status-pill muted">{isGenerating ? "생성 중" : "대기"}</span>
      </div>

      <label>
        주제
        <textarea
          name="topic"
          rows={4}
          required
          defaultValue="커뮤니티에서 반응이 갈린 카페 주문 사건"
        />
      </label>

      <div className="field-grid">
        <label>
          타깃 시청자
          <input name="target_audience" defaultValue="이슈 쇼츠 시청자" />
        </label>
        <label>
          톤
          <input name="tone" defaultValue="빠르고 친근한 설명체" />
        </label>
        <label>
          스타일
          <select name="style_template_id" defaultValue="issue_turi_basic">
            <option value="issue_turi_basic">이슈털이 기본형</option>
            <option value="issue_summary">이슈 요약형</option>
            <option value="controversy_roundup">논란 정리형</option>
          </select>
        </label>
        <label>
          길이
          <input name="video_length_seconds" type="number" min={40} max={60} defaultValue={50} />
        </label>
      </div>

      <details className="source-first-section">
        <summary>
          <span>소스 기반 쇼츠 만들기</span>
          <em>선택</em>
        </summary>
        <p>URL을 자동으로 읽지 않습니다. 사용자가 제공한 링크와 맥락만 기획 참고 자료로 저장합니다.</p>

        <label>
          원본 링크
          <input name="source_url" placeholder="https://..." />
        </label>

        <div className="field-grid">
          <label>
            소스 유형
            <select name="source_type" defaultValue="community">
              <option value="community">community</option>
              <option value="news">news</option>
              <option value="youtube">youtube</option>
              <option value="broadcast">broadcast</option>
              <option value="instagram">instagram</option>
              <option value="google_image">google_image</option>
              <option value="stock_site">stock_site</option>
              <option value="user_provided">user_provided</option>
              <option value="mockup">mockup</option>
              <option value="ai_generated">ai_generated</option>
            </select>
          </label>
          <label>
            소스 제목
            <input name="source_title" placeholder="자료 제목 또는 게시글 제목" />
          </label>
        </div>

        <label>
          소스 요약/맥락
          <textarea name="source_context" rows={3} placeholder="직접 요약하거나 필요한 맥락을 붙여넣으세요." />
        </label>

        <label>
          쇼츠 관점
          <input name="source_angle" placeholder="반응 갈림, 쟁점, 맥락 전환, 댓글 유도 등" />
        </label>
      </details>

      <button type="submit" disabled={isGenerating}>
        {isGenerating ? "생성 중..." : "AI 기획 생성"}
      </button>
    </form>
  );
}

function buildSourceBrief(formData: FormData): SourceBrief | null {
  const source_url = String(formData.get("source_url") || "").trim();
  const source_title = String(formData.get("source_title") || "").trim();
  const source_context = String(formData.get("source_context") || "").trim();
  const source_angle = String(formData.get("source_angle") || "").trim();
  if (!source_url && !source_title && !source_context && !source_angle) {
    return null;
  }
  return {
    source_url,
    source_type: String(formData.get("source_type") || "community") as AssetSourceType,
    source_title,
    source_context,
    source_angle,
  };
}

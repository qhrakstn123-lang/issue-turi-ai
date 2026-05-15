"use client";

import type { FormEvent } from "react";
import type { ProjectPayload } from "../lib/types";

type ProjectFormProps = {
  isGenerating: boolean;
  onSubmit: (payload: ProjectPayload) => void;
};

export function ProjectForm({ isGenerating, onSubmit }: ProjectFormProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    onSubmit({
      topic: String(formData.get("topic") || "").trim(),
      target_audience: String(formData.get("target_audience") || "").trim(),
      tone: String(formData.get("tone") || "").trim(),
      style_template_id: String(formData.get("style_template_id") || "issue_turi_basic"),
      video_length_seconds: Number(formData.get("video_length_seconds") || 50),
      output_format: "youtube_shorts",
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

      <button type="submit" disabled={isGenerating}>
        {isGenerating ? "생성 중..." : "AI 기획 생성"}
      </button>
    </form>
  );
}

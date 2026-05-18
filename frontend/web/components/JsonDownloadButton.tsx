"use client";

import type {
  AssetSourceCandidate,
  AssetSourceExportPayload,
  GenerationResult,
  SourceBrief,
  SourceCapturePlan,
} from "../lib/types";
import { normalizeGenerationResult } from "../lib/normalize";

type JsonDownloadButtonProps = {
  result: GenerationResult | null;
  assetSourceCandidates?: AssetSourceCandidate[];
  sourceBrief?: SourceBrief | null;
  sourceCapturePlans?: SourceCapturePlan[];
};

export function JsonDownloadButton({
  result,
  assetSourceCandidates = [],
  sourceBrief = null,
  sourceCapturePlans = [],
}: JsonDownloadButtonProps) {
  function handleDownload() {
    if (!result) {
      return;
    }
    const exportPayload: AssetSourceExportPayload = {
      generation_result: normalizeGenerationResult(result),
      ...(sourceBrief ? { source_brief: sourceBrief } : {}),
      source_capture_plans: sourceCapturePlans,
      asset_source_candidates: assetSourceCandidates,
    };
    const json = JSON.stringify(exportPayload, null, 2);
    const blob = new Blob([json], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `issue-turi-plan-${timestampForFilename(new Date())}.json`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  if (!result) {
    return null;
  }

  return (
    <button className="secondary-button" type="button" onClick={handleDownload}>
      JSON 다운로드
    </button>
  );
}

function timestampForFilename(date: Date) {
  const pad = (value: number) => String(value).padStart(2, "0");
  return [
    date.getFullYear(),
    pad(date.getMonth() + 1),
    pad(date.getDate()),
    "-",
    pad(date.getHours()),
    pad(date.getMinutes()),
    pad(date.getSeconds()),
  ].join("");
}

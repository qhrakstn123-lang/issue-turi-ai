import type { GenerationResult } from "./types";

export function normalizeGenerationResult(result: GenerationResult): GenerationResult {
  return {
    ...result,
    timeline: {
      ...result.timeline,
      scenes: result.timeline.scenes.map((scene) => ({
        ...scene,
        beats: scene.beats ?? [],
        asset_review_checklist: scene.asset_review_checklist ?? [],
      })),
    },
  };
}

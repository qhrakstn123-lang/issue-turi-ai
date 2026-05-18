export type OutputFormat = "youtube_shorts";

export type SafetyStatus = "approved" | "needs_review" | "review_required" | "rejected";

export type ProjectPayload = {
  topic: string;
  target_audience: string;
  tone: string;
  style_template_id: string;
  video_length_seconds: number;
  output_format: OutputFormat;
  source_brief?: SourceBrief;
};

export type Project = ProjectPayload & {
  project_id: string;
  status: string;
  generation_result: GenerationResult | null;
};

export type VideoScript = {
  title: string;
  narration: string;
  target_duration_seconds: number;
  style_notes: string[];
};

export type Scene = {
  scene_id: string;
  scene_purpose: string;
  narration: string;
  tts_text: string;
  subtitle: string;
  emphasis_caption: string;
  visual_asset_type: string;
  visual_description: string;
  generated_image_prompt: string;
  gif_or_clip_suggestion: string;
  stock_search_keywords: string[];
  motion_direction: string;
  transition: string;
  sound_effect_hint: string;
  estimated_duration: number;
  editing_notes: string;
  copyright_safety_note: string;
  visual_source_strategy: string;
  capture_source_type: string;
  capture_usage_mode: string;
  asset_usage_note: string;
  generated_image_url: string | null;
  sound_effect_asset: string | null;
  actual_duration: number | null;
};

export type Storyboard = {
  scenes: Scene[];
};

export type BeatType = "hook" | "evidence" | "reaction" | "turning_point" | "payoff" | "cta";

export type ProductionBeat = {
  beat_type: BeatType;
  start_time: number;
  end_time: number;
  text: string;
  motion: string;
  sound_effect: string;
  note: string;
};

export type TimelineScene = {
  scene_id: string;
  start_time: number;
  end_time: number;
  duration: number;
  visual_asset: {
    type: string;
    url: string | null;
  };
  narration_audio: {
    url: string | null;
  };
  subtitle: {
    text: string;
    start_time: number;
    end_time: number;
  };
  emphasis_caption: {
    text: string;
    start_time: number;
    end_time: number;
  };
  motion: string;
  transition: string;
  sound_effect: {
    type: string;
    start_time: number;
  };
  beats: ProductionBeat[];
  asset_review_checklist: string[];
};

export type Timeline = {
  project_id: string;
  output_format: OutputFormat;
  aspect_ratio: string;
  resolution: string;
  fps: number;
  total_duration: number;
  audio_mix: {
    background_music: string | null;
    background_music_volume: number;
    narration_volume: number;
    sfx_volume: number;
  };
  scenes: TimelineScene[];
};

export type AssetSourceType =
  | "community"
  | "news"
  | "youtube"
  | "broadcast"
  | "instagram"
  | "google_image"
  | "stock_site"
  | "ai_generated"
  | "user_provided"
  | "mockup";

export type AssetLicenseStatus = "unchecked" | "license_required" | "permission_required" | "cleared" | "avoid";

export type AssetSourceCandidate = {
  asset_candidate_id: string;
  scene_id: string;
  source_type: AssetSourceType;
  source_url: string;
  source_title: string;
  usage_mode: string;
  license_status: AssetLicenseStatus;
  needs_blur: boolean;
  needs_rewrite: boolean;
  approved_for_use: boolean;
  review_notes: string;
};

export type SourceBrief = {
  source_url: string;
  source_type: AssetSourceType;
  source_title: string;
  source_context: string;
  source_angle: string;
};

export type AssetSourceExportPayload = {
  generation_result: GenerationResult;
  source_brief?: SourceBrief;
  asset_source_candidates: AssetSourceCandidate[];
};

export type GenerationResult = {
  project_id: string;
  video_script: VideoScript;
  storyboard: Storyboard;
  timeline: Timeline;
  safety_status: SafetyStatus;
  safety_notes: string[];
  copyright_risks: string[];
  rumor_or_defamation_risks: string[];
  privacy_or_portrait_risks: string[];
  source_usage_risks: string[];
  required_human_review: boolean;
  recommended_revisions: string[];
};

export type CreateProjectResponse = {
  project: Project;
};

export type GenerateShortsPlanResponse = {
  result: GenerationResult;
};

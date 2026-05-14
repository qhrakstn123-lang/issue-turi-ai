const form = document.querySelector("#project-form");
const sceneList = document.querySelector("#scene-list");
const scriptTitle = document.querySelector("#script-title");
const statusPill = document.querySelector("#status-pill");
const safetyStatus = document.querySelector("#safety-status");
const resultSummary = document.querySelector("#result-summary");
const safetyReview = document.querySelector("#safety-review");
const downloadJsonButton = document.querySelector("#download-json");
const template = document.querySelector("#scene-template");
let currentGenerationResult = null;

downloadJsonButton.addEventListener("click", () => {
  downloadCurrentGenerationResult();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("Generating", false);
  currentGenerationResult = null;
  downloadJsonButton.hidden = true;
  resultSummary.replaceChildren();
  safetyReview.replaceChildren();
  sceneList.replaceChildren();

  try {
    const projectPayload = collectProjectPayload();
    const projectResponse = await postJson("/api/projects", projectPayload);
    const projectId = projectResponse.project.project_id;
    const resultResponse = await postJson("/api/generate/shorts-plan", { project_id: projectId });
    renderResult(resultResponse.result);
    currentGenerationResult = resultResponse.result;
    downloadJsonButton.hidden = false;
    setStatus("Complete", false);
  } catch (error) {
    setStatus("Failed", true);
    currentGenerationResult = null;
    downloadJsonButton.hidden = true;
    resultSummary.replaceChildren();
    safetyReview.replaceChildren();
    sceneList.replaceChildren(createErrorRow(error));
  }
});

function collectProjectPayload() {
  return {
    topic: fieldValue("topic"),
    target_audience: fieldValue("target_audience"),
    tone: fieldValue("tone"),
    style_template_id: fieldValue("style_template_id"),
    video_length_seconds: Number(fieldValue("video_length_seconds")),
    output_format: "youtube_shorts",
  };
}

function fieldValue(id) {
  return document.getElementById(id).value.trim();
}

async function postJson(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

function renderResult(result) {
  scriptTitle.textContent = result.video_script.title;
  setSafetyPill(result.safety_status);
  renderSummary(result);
  renderSafetyReview(result);

  const rows = result.storyboard.scenes.map((scene) => {
    const row = template.content.firstElementChild.cloneNode(true);
    row.querySelector(".scene-purpose").textContent = `${scene.scene_id} / ${scene.scene_purpose}`;
    row.querySelector(".scene-duration").textContent = `${scene.estimated_duration}s`;
    row.querySelector(".scene-narration").textContent = valueOrDash(scene.narration);
    row.querySelector(".scene-subtitle").textContent = labelValue("Subtitle", scene.subtitle);
    row.querySelector(".scene-emphasis").textContent = labelValue("Emphasis", scene.emphasis_caption);
    row.querySelector(".scene-visual-type").textContent = valueOrDash(scene.visual_asset_type);
    row.querySelector(".scene-visual-description").textContent = valueOrDash(scene.visual_description);
    row.querySelector(".scene-gif-suggestion").textContent = valueOrDash(scene.gif_or_clip_suggestion);
    row.querySelector(".scene-image-prompt").textContent = valueOrDash(scene.generated_image_prompt);
    renderKeywordTags(row.querySelector(".scene-keywords"), scene.stock_search_keywords || []);
    row.querySelector(".scene-source-strategy").textContent = labelValue("Strategy", scene.visual_source_strategy);
    row.querySelector(".scene-capture-source").textContent = labelValue("Source", scene.capture_source_type);
    row.querySelector(".scene-capture-usage").textContent = labelValue("Usage", scene.capture_usage_mode);
    row.querySelector(".asset-note").textContent = valueOrDash(scene.asset_usage_note);
    row.querySelector(".scene-motion").textContent = labelValue("Motion", scene.motion_direction);
    row.querySelector(".scene-sound").textContent = labelValue("Sound", scene.sound_effect_hint);
    row.querySelector(".scene-notes").textContent = valueOrDash(scene.editing_notes);
    return row;
  });
  sceneList.replaceChildren(...rows);
}

function setSafetyPill(status) {
  const label = {
    approved: "Approved",
    needs_review: "Needs review",
    review_required: "Needs review",
    rejected: "Rejected",
  }[status] || status || "Not reviewed";

  safetyStatus.textContent = label;
  safetyStatus.classList.toggle("warn", isRiskySafetyStatus(status));
  safetyStatus.classList.toggle("danger", status === "rejected");
  safetyStatus.classList.toggle("muted", !status);
}

function renderSummary(result) {
  const scenes = result.storyboard.scenes || [];
  const totalDuration = scenes.reduce((sum, scene) => sum + Number(scene.estimated_duration || 0), 0);
  const items = [
    ["Title", result.video_script.title],
    ["Safety", result.safety_status],
    ["Human review", result.required_human_review ? "required" : "not required"],
    ["Scenes", String(scenes.length)],
    ["Estimated duration", `${roundOne(totalDuration)}s`],
  ];

  resultSummary.replaceChildren(...items.map(([label, value]) => summaryItem(label, value)));
  resultSummary.classList.toggle("summary-warn", isRiskySafetyStatus(result.safety_status));
}

function summaryItem(label, value) {
  const item = document.createElement("div");
  item.className = "summary-item";

  const term = document.createElement("span");
  term.className = "summary-label";
  term.textContent = label;

  const detail = document.createElement("strong");
  detail.textContent = valueOrDash(value);

  item.append(term, detail);
  return item;
}

function renderSafetyReview(result) {
  const heading = document.createElement("div");
  heading.className = "safety-heading";

  const title = document.createElement("h3");
  title.textContent = "Safety review";

  const humanReview = document.createElement("span");
  humanReview.className = result.required_human_review ? "review-flag warn" : "review-flag";
  humanReview.textContent = result.required_human_review ? "Human review required" : "No human review flag";

  heading.append(title, humanReview);

  const notes = riskDetails("Safety notes", result.safety_notes || [], true);
  const riskSections = [
    riskDetails("Copyright risks", result.copyright_risks || []),
    riskDetails("Rumor or defamation risks", result.rumor_or_defamation_risks || []),
    riskDetails("Privacy or portrait risks", result.privacy_or_portrait_risks || []),
    riskDetails("Source usage risks", result.source_usage_risks || []),
  ];
  const revisions = revisionBox(result.recommended_revisions || []);

  safetyReview.replaceChildren(heading, notes, ...riskSections, revisions);
  safetyReview.classList.toggle("safety-warn", isRiskySafetyStatus(result.safety_status) || result.required_human_review);
}

function riskDetails(title, items, open = false) {
  const details = document.createElement("details");
  details.className = "risk-details";
  details.open = open || items.length > 0;

  const summary = document.createElement("summary");
  summary.textContent = `${title} (${items.length})`;

  const list = document.createElement("ul");
  list.className = "risk-list";
  if (items.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "None";
    list.append(empty);
  } else {
    items.forEach((item) => {
      const row = document.createElement("li");
      row.textContent = item;
      list.append(row);
    });
  }

  details.append(summary, list);
  return details;
}

function revisionBox(items) {
  const box = document.createElement("section");
  box.className = "revision-box";

  const title = document.createElement("h3");
  title.textContent = "Recommended revisions";

  const list = document.createElement("ul");
  list.className = "risk-list";
  if (items.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No revision suggestions";
    list.append(empty);
  } else {
    items.forEach((item) => {
      const row = document.createElement("li");
      row.textContent = item;
      list.append(row);
    });
  }

  box.append(title, list);
  return box;
}

function renderKeywordTags(container, keywords) {
  if (!keywords.length) {
    const empty = document.createElement("span");
    empty.className = "keyword empty";
    empty.textContent = "No keywords";
    container.replaceChildren(empty);
    return;
  }

  const tags = keywords.map((keyword) => {
    const tag = document.createElement("span");
    tag.className = "keyword";
    tag.textContent = keyword;
    return tag;
  });
  container.replaceChildren(...tags);
}

function createErrorRow(error) {
  const row = document.createElement("li");
  row.className = "scene-row";
  row.textContent = error.message;
  return row;
}

function setStatus(text, isWarning) {
  statusPill.textContent = text;
  statusPill.classList.toggle("warn", isWarning);
}

function downloadCurrentGenerationResult() {
  if (!currentGenerationResult) {
    return;
  }

  const json = JSON.stringify(currentGenerationResult, null, 2);
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

function timestampForFilename(date) {
  const pad = (value) => String(value).padStart(2, "0");
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

function isRiskySafetyStatus(status) {
  return status === "needs_review" || status === "review_required" || status === "rejected";
}

function labelValue(label, value) {
  return `${label}: ${valueOrDash(value)}`;
}

function valueOrDash(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return String(value);
}

function roundOne(value) {
  return Math.round(value * 10) / 10;
}

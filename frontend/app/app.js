const form = document.querySelector("#project-form");
const sceneList = document.querySelector("#scene-list");
const scriptTitle = document.querySelector("#script-title");
const statusPill = document.querySelector("#status-pill");
const safetyStatus = document.querySelector("#safety-status");
const template = document.querySelector("#scene-template");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("생성 중", false);
  sceneList.replaceChildren();

  try {
    const projectPayload = collectProjectPayload();
    const projectResponse = await postJson("/api/projects", projectPayload);
    const projectId = projectResponse.project.project_id;
    const resultResponse = await postJson("/api/generate/shorts-plan", { project_id: projectId });
    renderResult(resultResponse.result);
    setStatus("완료", false);
  } catch (error) {
    setStatus("실패", true);
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
    throw new Error(data.error || "요청 실패");
  }
  return data;
}

function renderResult(result) {
  scriptTitle.textContent = result.video_script.title;
  safetyStatus.textContent = result.safety_status === "review_required" ? "검토 필요" : "승인";
  safetyStatus.classList.toggle("warn", result.safety_status === "review_required");

  const rows = result.storyboard.scenes.map((scene) => {
    const row = template.content.firstElementChild.cloneNode(true);
    row.querySelector(".scene-purpose").textContent = `${scene.scene_id} · ${scene.scene_purpose}`;
    row.querySelector(".scene-duration").textContent = `${scene.estimated_duration}초`;
    row.querySelector(".scene-narration").textContent = scene.narration;
    row.querySelector(".scene-subtitle").textContent = scene.subtitle;
    row.querySelector(".scene-motion").textContent = scene.motion_direction;
    row.querySelector(".scene-sound").textContent = scene.sound_effect_hint;
    row.querySelector(".scene-notes").textContent = scene.editing_notes;
    return row;
  });
  sceneList.replaceChildren(...rows);
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

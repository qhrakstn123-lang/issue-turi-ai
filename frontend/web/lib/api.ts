import type { CreateProjectResponse, GenerateShortsPlanResponse, ProjectPayload } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";

async function postJson<TResponse>(path: string, payload: unknown): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data as TResponse;
}

export function createProject(payload: ProjectPayload): Promise<CreateProjectResponse> {
  return postJson<CreateProjectResponse>("/api/projects", payload);
}

export function generateShortsPlan(projectId: string): Promise<GenerateShortsPlanResponse> {
  return postJson<GenerateShortsPlanResponse>("/api/generate/shorts-plan", {
    project_id: projectId,
  });
}

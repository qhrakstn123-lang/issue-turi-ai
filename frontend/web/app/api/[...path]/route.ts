const BACKEND_API_BASE_URL = process.env.BACKEND_API_BASE_URL || "http://127.0.0.1:8000";

type RouteContext = {
  params: {
    path: string[];
  };
};

async function proxyRequest(request: Request, context: RouteContext) {
  const incomingUrl = new URL(request.url);
  const backendUrl = new URL(`/api/${context.params.path.join("/")}${incomingUrl.search}`, BACKEND_API_BASE_URL);
  const headers = new Headers(request.headers);
  for (const header of ["host", "connection", "content-length", "expect", "keep-alive", "transfer-encoding"]) {
    headers.delete(header);
  }

  const response = await fetch(backendUrl, {
    method: request.method,
    headers,
    body: request.method === "GET" || request.method === "HEAD" ? undefined : await request.text(),
    cache: "no-store",
  });

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
}

export async function GET(request: Request, context: RouteContext) {
  return proxyRequest(request, context);
}

export async function POST(request: Request, context: RouteContext) {
  return proxyRequest(request, context);
}

export async function PATCH(request: Request, context: RouteContext) {
  return proxyRequest(request, context);
}

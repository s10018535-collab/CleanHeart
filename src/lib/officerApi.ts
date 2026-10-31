const SESSION_KEY = "clean-hearts-officer-session";

export interface OfficerSession {
  token: string;
  department: string;
}

export function loadOfficerSession(): OfficerSession | null {
  const raw = sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as Partial<OfficerSession>;
    if (typeof parsed.token === "string" && typeof parsed.department === "string") {
      return { token: parsed.token, department: parsed.department };
    }
  } catch {
    // fall through to clearing the stored value
  }
  sessionStorage.removeItem(SESSION_KEY);
  return null;
}

export function saveOfficerSession(session: OfficerSession) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearOfficerSession() {
  sessionStorage.removeItem(SESSION_KEY);
}

export class OfficerApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export async function callOfficerApi<T>(
  action: string,
  payload: Record<string, unknown> = {},
): Promise<T> {
  const url = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/officer-api`;
  let response: Response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Apikey: import.meta.env.VITE_SUPABASE_ANON_KEY,
        Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
      },
      body: JSON.stringify({ action, ...payload }),
    });
  } catch {
    throw new OfficerApiError("Network problem. Please check your connection and try again.", 0);
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    throw new OfficerApiError("The officer service returned an unexpected response.", response.status);
  }

  const error = (body as { error?: unknown } | null)?.error;
  if (!response.ok) {
    throw new OfficerApiError(
      typeof error === "string" ? error : "Something went wrong. Please try again.",
      response.status,
    );
  }
  return body as T;
}

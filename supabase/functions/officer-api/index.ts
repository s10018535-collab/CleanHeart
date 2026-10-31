import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const DEPARTMENTS = [
  "Public Works",
  "Water & Drainage",
  "Sanitation",
  "Electrical & Lighting",
  "Parks & Recreation",
  "Public Safety",
  "General Services",
];
const STATUSES = ["new", "in_progress", "resolved"];
const SESSION_HOURS = 8;
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

async function sha256Hex(text: string) {
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, "0")).join("");
}

function randomToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

function isUuid(value: unknown): value is string {
  return typeof value === "string" && UUID_PATTERN.test(value);
}

// deno-lint-ignore no-explicit-any
async function findSession(supabase: any, token: unknown) {
  if (typeof token !== "string" || token.length !== 64) return null;
  const { data, error } = await supabase
    .from("officer_sessions")
    .select("department, expires_at")
    .eq("token", token)
    .maybeSingle();
  if (error) throw error;
  if (!data || new Date(data.expires_at).getTime() < Date.now()) return null;
  return data as { department: string; expires_at: string };
}

// deno-lint-ignore no-explicit-any
async function login(supabase: any, body: Record<string, unknown>) {
  const password = body.password;
  const department = body.department;
  if (typeof password !== "string" || password.length === 0 || password.length > 200) {
    return json({ error: "Please enter the officer password." }, 400);
  }
  if (typeof department !== "string" || !DEPARTMENTS.includes(department)) {
    return json({ error: "Please choose a valid department." }, 400);
  }

  const { data: credentials, error: credentialsError } = await supabase
    .from("officer_credentials")
    .select("salt, password_hash")
    .eq("id", 1)
    .maybeSingle();
  if (credentialsError) throw credentialsError;
  if (!credentials) return json({ error: "Officer access is not configured." }, 500);

  const attemptHash = await sha256Hex(`${credentials.salt}:${password}`);
  if (attemptHash !== credentials.password_hash) {
    return json({ error: "Incorrect password." }, 401);
  }

  const token = randomToken();
  const expiresAt = new Date(Date.now() + SESSION_HOURS * 60 * 60 * 1000).toISOString();
  const { error: insertError } = await supabase
    .from("officer_sessions")
    .insert({ token, department, expires_at: expiresAt });
  if (insertError) throw insertError;

  return json({ token, department, expiresAt });
}

// deno-lint-ignore no-explicit-any
async function updateStatus(supabase: any, body: Record<string, unknown>) {
  const session = await findSession(supabase, body.token);
  if (!session) return json({ error: "Your officer session has expired. Please sign in again." }, 401);

  if (!isUuid(body.issueId)) return json({ error: "Invalid issue." }, 400);
  if (typeof body.status !== "string" || !STATUSES.includes(body.status)) {
    return json({ error: "Invalid status." }, 400);
  }

  const { data, error } = await supabase
    .from("issues")
    .update({ status: body.status })
    .eq("id", body.issueId)
    .eq("department", session.department)
    .select("id, status")
    .maybeSingle();
  if (error) throw error;
  if (!data) return json({ error: "This issue is not in your department." }, 404);

  return json({ id: data.id, status: data.status });
}

// deno-lint-ignore no-explicit-any
async function session(supabase: any, body: Record<string, unknown>) {
  const current = await findSession(supabase, body.token);
  if (!current) return json({ error: "Your officer session has expired. Please sign in again." }, 401);
  return json({ department: current.department, expiresAt: current.expires_at });
}

// deno-lint-ignore no-explicit-any
async function logout(supabase: any, body: Record<string, unknown>) {
  if (typeof body.token === "string" && body.token.length === 64) {
    const { error } = await supabase.from("officer_sessions").delete().eq("token", body.token);
    if (error) throw error;
  }
  return json({ ok: true });
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const body = (await req.json()) as Record<string, unknown>;

    switch (body.action) {
      case "login":
        return await login(supabase, body);
      case "session":
        return await session(supabase, body);
      case "logout":
        return await logout(supabase, body);
      case "updateStatus":
        return await updateStatus(supabase, body);
      default:
        return json({ error: "Unknown action." }, 400);
    }
  } catch (err) {
    console.error("officer-api failed", err);
    return json({ error: "Something went wrong. Please try again." }, 500);
  }
});

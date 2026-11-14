// Shared helper: calls the Gemini API with the key stored in Vercel env vars.
export const MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash";

export function checkAccess(req, res) {
  const code = process.env.ACCESS_CODE;
  if (!code) return true;
  if ((req.headers["x-access-code"] || "") === code) return true;
  res.status(401).json({ error: "access_code" });
  return false;
}

export async function gemini({ contents, json = false, temperature = 0.2 }) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) throw Object.assign(new Error("GEMINI_API_KEY is not set in Vercel"), { status: 500 });
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
  const body = {
    contents,
    generationConfig: { temperature, ...(json ? { responseMimeType: "application/json" } : {}) },
  };
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": key },
    body: JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(data?.error?.message || `Gemini error ${r.status}`), { status: r.status === 429 ? 429 : 502 });
  const text = (data?.candidates?.[0]?.content?.parts || []).map(p => p.text || "").join("");
  if (!text) throw Object.assign(new Error("Gemini returned no text"), { status: 502 });
  return text;
}

// Shared helper: calls the Gemini API with the key stored in Vercel env vars.
let picked = process.env.GEMINI_MODEL || "", list = null;
// If GEMINI_MODEL isn't set, ask Google which Flash models this key can use and take the newest.
export const allModels = () => list;
export async function getModel() {
  if (picked) return picked;
  const key = process.env.GEMINI_API_KEY;
  const r = await fetch("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", { headers: { "x-goog-api-key": key }, signal: AbortSignal.timeout(10000) });
  const d = await r.json().catch(() => ({}));
  const ver = n => parseFloat((n.match(/gemini-([\d.]+)/) || [])[1] || "0");
  const names = (d.models || []).filter(m => (m.supportedGenerationMethods || []).includes("generateContent"))
    .map(m => m.name.replace(/^models\//, "")).filter(n => /^gemini-[\d.]+-flash$/.test(n) || n === "gemini-flash-latest")
    .sort((a, b) => ver(b) - ver(a));
  list = names.length ? names : ["gemini-flash-latest"];
  picked = list[0];
  return picked;
}

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
  await getModel();
  const body = {
    contents,
    generationConfig: { temperature, ...(json ? { responseMimeType: "application/json" } : {}) },
  };
  const models = list ? list.slice(0, 3) : [picked];
  let r, data;
  for (const m of models) {
    r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(50000),
    }).catch(e => { throw Object.assign(new Error(e.name === "TimeoutError" ? "Gemini took too long to answer" : "Could not reach Gemini"), { status: 504 }); });
    if (r.status !== 503 && r.status !== 404 && r.status !== 429) break; // overloaded / gone / quota: try the next model
  }
  data = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(data?.error?.message || `Gemini error ${r.status}`), { status: r.status === 429 ? 429 : 502 });
  const text = (data?.candidates?.[0]?.content?.parts || []).map(p => p.text || "").join("");
  if (!text) throw Object.assign(new Error("Gemini returned no text"), { status: 502 });
  return text;
}

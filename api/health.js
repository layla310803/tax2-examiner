import { getModel, allModels } from "./_gemini.js";
export const config = { maxDuration: 60 };
export default async function handler(req, res) {
  const keySet = !!process.env.GEMINI_API_KEY;
  let model = null;
  if (keySet) { try { model = await getModel(); } catch {} }
  const out = { ok: true, model, models: allModels(), keySet, codeRequired: !!process.env.ACCESS_CODE };
  // ?probe=1 sends a tiny prompt to each model and reports how it responds (for diagnosing slow/overloaded models).
  if (keySet && req.query?.probe) {
    out.probe = await Promise.all((allModels() || []).map(async m => {
      const t0 = Date.now();
      try {
        const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`, {
          method: "POST", headers: { "Content-Type": "application/json", "x-goog-api-key": process.env.GEMINI_API_KEY },
          body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: "Reply OK" }] }] }), signal: AbortSignal.timeout(25000) });
        return { m, status: r.status, ms: Date.now() - t0 };
      } catch (e) { return { m, status: e.name, ms: Date.now() - t0 }; }
    }));
  }
  res.status(200).json(out);
}

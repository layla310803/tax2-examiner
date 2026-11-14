import { gemini, checkAccess } from "./_gemini.js";

export const config = { maxDuration: 60 };

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  if (!checkAccess(req, res)) return;
  const { prompt } = req.body || {};
  if (typeof prompt !== "string" || !prompt.trim() || prompt.length > 200000)
    return res.status(400).json({ error: "bad_prompt" });
  try {
    const text = await gemini({ contents: [{ role: "user", parts: [{ text: prompt }] }], json: true });
    let out;
    try { out = JSON.parse(text); }
    catch { const m = text.match(/\{[\s\S]*\}/); out = m ? JSON.parse(m[0]) : null; }
    if (!out) return res.status(502).json({ error: "invalid_json" });
    res.status(200).json(out);
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message });
  }
}

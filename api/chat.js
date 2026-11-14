import { gemini, checkAccess } from "./_gemini.js";

export const config = { maxDuration: 60 };

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  if (!checkAccess(req, res)) return;
  const { turns } = req.body || {};
  if (!Array.isArray(turns) || !turns.length) return res.status(400).json({ error: "bad_turns" });
  const contents = turns.slice(-16).map(t => ({
    role: t.role === "assistant" ? "model" : "user",
    parts: [{ text: String(t.content || "").slice(0, 120000) }],
  }));
  try {
    const text = await gemini({ contents, temperature: 0.4 });
    res.status(200).json({ text });
  } catch (e) {
    res.status(e.status || 500).json({ error: e.message });
  }
}

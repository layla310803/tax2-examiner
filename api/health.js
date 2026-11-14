import { MODEL } from "./_gemini.js";
export default function handler(req, res) {
  res.status(200).json({ ok: true, model: MODEL, keySet: !!process.env.GEMINI_API_KEY, codeRequired: !!process.env.ACCESS_CODE });
}

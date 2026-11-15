import { getModel, allModels } from "./_gemini.js";
export default async function handler(req, res) {
  const keySet = !!process.env.GEMINI_API_KEY;
  let model = null;
  if (keySet) { try { model = await getModel(); } catch {} }
  res.status(200).json({ ok: true, model, models: allModels(), keySet, codeRequired: !!process.env.ACCESS_CODE });
}

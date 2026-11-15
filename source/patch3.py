import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t = open("template.html", encoding="utf-8").read()
def rep(a, b):
    global t
    assert a in t, a[:70]
    t = t.replace(a, b, 1)

# ---- CSS ----
rep(".hint{font-size:13px;color:var(--muted)}",
    ".hint{font-size:13px;color:var(--muted)}\n"
    "dialog#keyDlg{border:1px solid var(--rule);border-radius:12px;background:var(--sheet);color:var(--ink);max-width:520px;width:calc(100% - 32px);padding:20px 22px}\n"
    "dialog#keyDlg::backdrop{background:rgba(0,0,0,.45)}\n"
    "#keyDlg h3{margin:0 0 6px;font-family:var(--font-display);font-size:20px}\n"
    "#keyDlg p{font-size:13px;color:var(--muted);margin:0 0 12px}\n"
    "#keyDlg label{display:block;font-size:13px;font-weight:600;margin:12px 0 4px}\n"
    "#keyDlg .prov{display:flex;gap:16px;font-weight:400}\n"
    "#keyDlg .prov label{font-weight:400;margin:0;display:flex;gap:6px;align-items:center}\n"
    "#keyDlg input[type=password],#keyDlg input[type=text]{width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);color:var(--ink);font:inherit}\n"
    "#keyDlg .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}\n"
    "#keyStatus{font-size:13px;margin-top:10px;min-height:1.2em}\n"
    "#keyStatus.ok{color:var(--good)} #keyStatus.bad{color:var(--pen)}")

# ---- top-bar button + dialog ----
rep('  <button class="btn small" id="homeBtn" hidden>All papers</button>\n</header>',
    '  <button class="btn small" id="keyBtn" hidden>AI key</button>\n'
    '  <button class="btn small" id="homeBtn" hidden>All papers</button>\n</header>\n'
    '<dialog id="keyDlg" aria-labelledby="keyTitle">\n'
    '  <h3 id="keyTitle">Use your own AI key</h3>\n'
    '  <p>Your key is saved only in this browser and sent straight to Google or Anthropic, never to this site. Without one, the site uses its shared Gemini key if that is working.</p>\n'
    '  <label>Provider</label>\n'
    '  <div class="prov"><label><input type="radio" name="prov" value="gemini" checked> Gemini (free key)</label><label><input type="radio" name="prov" value="claude"> Claude (paid key)</label></div>\n'
    '  <div class="hint" id="provHint" style="margin-top:6px"></div>\n'
    '  <label for="keyIn">API key</label><input id="keyIn" type="password" autocomplete="off" spellcheck="false">\n'
    '  <label for="modelIn">Model <span class="hint">(leave blank to pick automatically)</span></label><input id="modelIn" type="text" spellcheck="false">\n'
    '  <div class="row"><button class="btn primary" id="keySave">Save and test</button><button class="btn" id="keyRemove">Remove my key</button><span style="flex:1"></span><button class="btn" id="keyClose">Close</button></div>\n'
    '  <div id="keyStatus" role="status"></div>\n'
    '</dialog>')

# ---- backends ----
old_start = t.index("/* Marker backends:")
old_end = t.index("/* ---------- document renderer")
t = t[:old_start] + r'''/* Marker backends, in order: Claude (inside a Claude artifact) > the user's own key (Gemini or Claude, called
   straight from the browser) > this site's shared Gemini key via /api (on Vercel) > self-mark. */
let sample = null, sampleReady = false, api = null; // api = {model, codeRequired}
const CODE_KEY = "tax2-examiner-code", BYOK_KEY = "tax2-examiner-byok";
function getCode(){ try { return localStorage.getItem(CODE_KEY) || ""; } catch { return ""; } }
function setCode(v){ try { localStorage.setItem(CODE_KEY, v); } catch {} }
function getByok(){ try { const b = JSON.parse(localStorage.getItem(BYOK_KEY) || "null"); return b && b.key ? b : null; } catch { return null; } }
function setByok(b){ try { b ? localStorage.setItem(BYOK_KEY, JSON.stringify(b)) : localStorage.removeItem(BYOK_KEY); } catch {} }
let byok = getByok();
const onWeb = /^https?:$/.test(location.protocol) && !window.claude;
(async () => {
  if (onWeb) {
    try { const r = await fetch("api/health"); if (r.ok){ const h = await r.json(); if (h.ok && h.keySet) api = h; } } catch {}
  }
  if (!onWeb) { try { if (window.claude?.use) sample = await window.claude.use("sample"); } catch { sample = null; } }
  sampleReady = true; $("#keyBtn").hidden = !!sample;
  if (view.paper && document.getElementById("right")) renderRight();
})();
const backend = () => sample ? "claude-artifact" : byok ? "byok" : api ? "api" : null;
const canMark = () => !!backend();
function markerLabel(){
  const b = backend();
  if (b === "byok") return `Marked with your own ${byok.provider === "claude" ? "Claude" : "Gemini"} key (${esc(byok.model || "auto")}).`;
  if (b === "api") return `Marked by the site's shared Gemini key (${esc(api.model)}).`;
  return "";
}
async function apiPost(path, body, signal){
  const r = await fetch(path, { method:"POST", signal, headers:{ "Content-Type":"application/json", "x-access-code": getCode() }, body: JSON.stringify(body) });
  const data = await r.json().catch(() => ({}));
  if (r.status === 401) throw { code: "access_code" };
  if (r.status === 429) throw { code: "rate_limited" };
  if (!r.ok) throw { code: data.error === "invalid_json" ? "invalid_json" : "upstream_error", message: data.error };
  return data;
}
/* --- direct (bring-your-own-key) calls --- */
async function pickGeminiModel(key){
  const r = await fetch("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", { headers: { "x-goog-api-key": key } });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw { code: r.status === 400 || r.status === 401 || r.status === 403 ? "bad_key" : "upstream_error", message: d?.error?.message };
  const names = (d.models || []).filter(m => (m.supportedGenerationMethods || []).includes("generateContent"))
    .map(m => m.name.replace(/^models\//, ""))
    .filter(n => /^gemini-[\d.]+-flash$/.test(n) || /^gemini-flash-latest$/.test(n));
  const ver = n => parseFloat((n.match(/gemini-([\d.]+)/) || [])[1] || "0");
  names.sort((a, b) => ver(b) - ver(a));
  if (!names.length) throw { code: "upstream_error", message: "No Gemini Flash model is available to this key." };
  return names[0];
}
async function byokCall(turns, { json = false, signal } = {}){
  const b = byok;
  if (b.provider === "claude") {
    const sys = json ? "Reply with a single valid JSON object and nothing else." : undefined;
    const r = await fetch("https://api.anthropic.com/v1/messages", { method: "POST", signal,
      headers: { "content-type": "application/json", "x-api-key": b.key, "anthropic-version": "2023-06-01", "anthropic-dangerous-direct-browser-access": "true" },
      body: JSON.stringify({ model: b.model || "claude-sonnet-5-5", max_tokens: 8000, ...(sys ? { system: sys } : {}),
        messages: turns.map(x => ({ role: x.role === "assistant" ? "assistant" : "user", content: String(x.content) })) }) });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw { code: r.status === 401 || r.status === 403 ? "bad_key" : r.status === 429 ? "rate_limited" : "upstream_error", message: d?.error?.message };
    return (d.content || []).filter(c => c.type === "text").map(c => c.text).join("");
  }
  if (!b.model) { b.model = await pickGeminiModel(b.key); setByok(b); }
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(b.model)}:generateContent`, { method: "POST", signal,
    headers: { "Content-Type": "application/json", "x-goog-api-key": b.key },
    body: JSON.stringify({ contents: turns.map(x => ({ role: x.role === "assistant" ? "model" : "user", parts: [{ text: String(x.content) }] })),
      generationConfig: { temperature: json ? 0.2 : 0.4, ...(json ? { responseMimeType: "application/json" } : {}) } }) });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw { code: r.status === 400 && /api key/i.test(d?.error?.message || "") || r.status === 401 || r.status === 403 ? "bad_key" : r.status === 429 ? "rate_limited" : "upstream_error", message: d?.error?.message };
  const text = (d?.candidates?.[0]?.content?.parts || []).map(p => p.text || "").join("");
  if (!text) throw { code: "upstream_error", message: "The model returned no text." };
  return text;
}
function parseJSON(text){
  try { return JSON.parse(text); } catch {}
  const m = String(text).match(/\{[\s\S]*\}/); if (m) { try { return JSON.parse(m[0]); } catch {} }
  throw { code: "invalid_json" };
}
async function markJSON(prompt, signal){
  const b = backend();
  if (b === "byok") return parseJSON(await byokCall([{ role: "user", content: prompt }], { json: true, signal }));
  if (b === "api") return apiPost("api/mark", { prompt }, signal);
  return sample.json(prompt, { modelTier: "complex", signal });
}
async function chatText(turns, onText){
  const b = backend();
  if (b === "byok") { const text = await byokCall(turns); onText(text); return text; }
  if (b === "api") { const { text } = await apiPost("api/chat", { turns }); onText(text); return text; }
  const { text } = await sample(turns, { cache:false, onText: ({text}) => onText(text) });
  return text;
}
/* --- key dialog --- */
const PROV_HINT = {
  gemini: 'Free: go to <a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener">aistudio.google.com/apikey</a>, click Create API key, and paste it here (starts with AIza).',
  claude: 'Paid per use: create a key at <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">console.anthropic.com</a> (starts with sk-ant-). Default model: claude-sonnet-5-5.',
};
function openKeyDlg(){
  const d = $("#keyDlg"), b = byok || { provider: "gemini", key: "", model: "" };
  d.querySelectorAll('input[name=prov]').forEach(r => { r.checked = r.value === b.provider; r.onchange = () => { $("#provHint").innerHTML = PROV_HINT[r.value]; $("#modelIn").value = ""; }; });
  $("#provHint").innerHTML = PROV_HINT[b.provider];
  $("#keyIn").value = b.key; $("#modelIn").value = b.model || "";
  $("#keyStatus").textContent = byok ? "A key is saved in this browser." : ""; $("#keyStatus").className = "";
  d.showModal();
}
$("#keyBtn").onclick = openKeyDlg;
$("#keyClose").onclick = () => $("#keyDlg").close();
$("#keyRemove").onclick = () => { byok = null; setByok(null); $("#keyIn").value = ""; $("#modelIn").value = "";
  const st = $("#keyStatus"); st.className = ""; st.textContent = "Removed. Marking falls back to the site's shared key (or self-marking).";
  if (view.paper && document.getElementById("right")) renderRight(); };
$("#keySave").onclick = async () => {
  const st = $("#keyStatus"), prov = $("#keyDlg").querySelector('input[name=prov]:checked').value;
  const key = $("#keyIn").value.trim(), model = $("#modelIn").value.trim();
  if (!key) { st.className = "bad"; st.textContent = "Paste a key first."; return; }
  const prev = byok; byok = { provider: prov, key, model };
  st.className = ""; st.textContent = "Testing the key…"; $("#keySave").disabled = true;
  try {
    await byokCall([{ role: "user", content: "Reply with the single word OK." }]);
    setByok(byok); $("#modelIn").value = byok.model || "";
    st.className = "ok"; st.textContent = `Saved. Marking will use ${prov === "claude" ? "Claude" : "Gemini"} (${byok.model || "claude-sonnet-5-5"}).`;
    if (prov === "claude" && !byok.model) { byok.model = "claude-sonnet-5-5"; setByok(byok); }
    if (view.paper && document.getElementById("right")) renderRight();
  } catch (e) {
    byok = prev;
    st.className = "bad";
    st.textContent = e?.code === "bad_key" ? "That key was rejected. Check you copied all of it." :
      e?.code === "rate_limited" ? "The key works but is rate-limited right now. Try again in a minute." :
      `Test failed: ${e?.message || "connection problem"}`;
  } finally { $("#keySave").disabled = false; }
};

''' + t[old_end:]

# ---- right pane notices ----
rep('''    ${sampleReady && !canMark() ? `<div class="notice">Automatic marking isn't connected here (it works on the Vercel site or inside Claude). You can still submit, compare against the memo tab and record your own mark.</div>` : ""}
    ${api ? `<div class="hint">Marked by Gemini (${esc(api.model)}).${api.codeRequired ? ` <button class="btn small" id="codeBtn">${getCode() ? "Change" : "Enter"} access code</button>` : ""}</div>` : ""}''',
'''    ${sampleReady && !canMark() ? `<div class="notice">Automatic marking isn't set up in this browser. <button class="btn small" id="keyBtn2">Add your own AI key</button> (free Gemini key) or submit and self-mark against the memo.</div>` : ""}
    ${backend() === "byok" || backend() === "api" ? `<div class="hint">${markerLabel()} <button class="btn small" id="keyBtn2">${byok ? "Change" : "Use my own"} key</button>${backend() === "api" && api.codeRequired ? ` <button class="btn small" id="codeBtn">${getCode() ? "Change" : "Enter"} access code</button>` : ""}</div>` : ""}''')
rep('  const cb = $("#codeBtn"); if (cb) cb.onclick = askCode;',
    '  const cb = $("#codeBtn"); if (cb) cb.onclick = askCode;\n  const kb = $("#keyBtn2"); if (kb) kb.onclick = openKeyDlg;')

# ---- submit ----
rep('  if (api?.codeRequired && !getCode()){ askCode(); return; }',
    '  if (backend() === "api" && api.codeRequired && !getCode()){ askCode(); return; }')
rep('''      access_code: "That access code was wrong. Enter it again, then press Submit.",
    }[e?.code] || "Marking failed (connection or service problem). Press Submit to try again.";''',
'''      access_code: "That access code was wrong. Enter it again, then press Submit.",
      bad_key: "Your AI key was rejected. Open AI key (top right) and check it.",
    }[e?.code] || `Marking failed${e?.message ? ": " + e.message : " (connection or service problem)"}. Press Submit to try again.`;''')
rep('    if (e?.code === "not_granted"){ sample = null; }',
    '    if (e?.name === "AbortError") $("#fbSlot").innerHTML = `<div class="notice">Marking stopped.</div>`;\n    if (e?.code === "not_granted"){ sample = null; }')

open("template.html", "w", encoding="utf-8").write(t)
print("ok")

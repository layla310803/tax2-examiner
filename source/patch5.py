import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t = open("template.html", encoding="utf-8").read()
def rep(a, b):
    global t
    assert a in t, a[:70]
    t = t.replace(a, b, 1)

# ---- CSS ----
rep(".meter>i{display:block;height:100%;background:var(--accent)}",
    ".meter>i{display:block;height:100%;background:var(--accent)}\n"
    ".topics h2,.home h2.sec{font-family:var(--font-display);font-size:20px;margin:0 0 4px}\n"
    ".topicgrid{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}\n"
    ".tbtn{border:1px solid var(--rule);background:var(--sheet);border-radius:999px;padding:7px 14px;cursor:pointer;font-size:14px;display:inline-flex;gap:8px;align-items:center}\n"
    ".tbtn:hover{border-color:var(--accent);color:var(--accent)}\n"
    ".tbtn .n{font-family:var(--font-mono);font-size:12px;color:var(--muted)}\n"
    ".tlist{display:grid;gap:8px}\n"
    ".titem{background:var(--sheet);border:1px solid var(--rule);border-radius:10px;padding:12px 14px;cursor:pointer;text-align:left;display:grid;grid-template-columns:auto 1fr auto;gap:4px 14px;align-items:baseline}\n"
    ".titem:hover{border-color:var(--accent)}\n"
    ".titem .src{font-weight:600;white-space:nowrap}\n"
    ".titem .req{color:var(--muted);font-size:14px;grid-column:2;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}\n"
    ".titem .sc{font-family:var(--font-mono);font-size:13px;white-space:nowrap}\n"
    ".titem .tags{grid-column:2;font-size:12px;color:var(--muted)}\n"
    ".topicbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 12px;margin-bottom:10px;border:1px solid var(--accent);background:var(--accent-soft);border-radius:8px;font-size:13px}\n"
    ".topicbar strong{color:var(--accent)}\n"
    ".tagline{font-size:12px;color:var(--muted);margin:-4px 0 8px}")

# ---- data ----
rep("const PAPERS = /*__DATA__*/null;",
    "const PAPERS = /*__DATA__*/null;\nconst TOPICS = /*__TOPICS__*/null;\n"
    "const topicName = id => (TOPICS.find(x => x.id === id) || {}).name || id;\n"
    "function topicItems(tid){ const out = []; PAPERS.forEach(p => p.questions.forEach((q, qi) => q.parts.forEach((pt, pi) => { if ((pt.topics || []).includes(tid)) out.push({ p, qi, pi, pt }); }))); return out; }")

# ---- routing: #topic/<id> and #<paper>/<qi>/<pi> ----
rep('''  const id = location.hash.slice(1);
  const paper = PAPERS.find(p => p.id === id);
  if (!paper){ view.paper = null; renderHome(); return; }
  if (view.paper !== paper){''',
'''  const parts = location.hash.slice(1).split("/");
  if (parts[0] === "topic" && TOPICS.some(x => x.id === parts[1])){ view.paper = null; view.topic = parts[1]; renderTopic(parts[1]); return; }
  const paper = PAPERS.find(p => p.id === parts[0]);
  if (!paper){ view.paper = null; view.topic = null; renderHome(); return; }
  if (parts.length === 3){
    const qi = +parts[1], pi = +parts[2];
    if (paper.questions[qi]?.parts[pi]){ const moved = view.paper !== paper || view.q !== qi || view.p !== pi; view.paper = paper; view.q = qi; view.p = pi; if (moved){ view.tab = "scenario"; resetTimer(); } renderExam(); return; }
  }
  view.topic = null;
  if (view.paper !== paper){''')

# ---- home: topics section ----
rep('''      <p>Your answers and scores are saved in this browser.</p>
    </div>''',
'''      <p>Your answers and scores are saved in this browser.</p>
    </div>
    <section class="topics" aria-labelledby="topicsH">
      <h2 id="topicsH">Practise by topic</h2>
      <div class="hint">Every required on that topic, across all the papers.</div>
      <div class="topicgrid">${TOPICS.map(tp => { const items = topicItems(tp.id); const done = items.filter(x => best(x.p, x.pt) !== null).length;
        return `<button class="tbtn" data-t="${tp.id}">${esc(tp.name)} <span class="n">${done}/${items.length}</span></button>`; }).join("")}</div>
    </section>
    <h2 class="sec">Full papers</h2>''')
rep('  document.querySelectorAll(".card").forEach(c => c.onclick = () => go(c.dataset.id));',
    '  document.querySelectorAll(".card").forEach(c => c.onclick = () => go(c.dataset.id));\n'
    '  document.querySelectorAll(".tbtn").forEach(b => b.onclick = () => go("topic/" + b.dataset.t));')

# ---- topic page ----
rep("function fmt(n){",
'''function renderTopic(tid){
  $("#homeBtn").hidden = false; $("#crumb").textContent = topicName(tid); applyLayout();
  $("#app").className = "";
  const items = topicItems(tid);
  const got = items.reduce((a, x) => a + (best(x.p, x.pt) ?? 0), 0), tot = items.reduce((a, x) => a + x.pt.marks, 0);
  $("#app").innerHTML = `<div class="home">
    <div><h2 class="sec">${esc(topicName(tid))}</h2>
      <div class="hint">${items.length} requireds · ${tot} marks · best so far <span class="mono">${fmt(got)} / ${tot}</span>. Pick one, or start at the first you haven't done; "Next in topic" then takes you through the rest.</div></div>
    <div class="row"><button class="btn primary" id="tstart">Start practising</button><button class="btn" id="tback">All topics</button></div>
    <div class="tlist">${items.map((x, i) => { const b = best(x.p, x.pt);
      return `<button class="titem" data-i="${i}"><span class="src">${esc(x.p.short)} · ${esc(x.pt.id)}</span><span class="req">${esc(x.pt.required.split("\\n")[0])}</span>
        <span class="sc">${b === null ? `${x.pt.marks} marks` : `<span class="${band(b, x.pt.marks)}">${fmt(b)}</span> / ${x.pt.marks}`}</span>
        <span class="tags">${x.pt.topics.filter(t => t !== tid).map(topicName).map(esc).join(" · ")}</span></button>`; }).join("")}</div>
  </div>`;
  const open = x => go(`${x.p.id}/${x.qi}/${x.pi}`);
  document.querySelectorAll(".titem").forEach(b => b.onclick = () => { view.topic = tid; open(items[+b.dataset.i]); });
  $("#tstart").onclick = () => { view.topic = tid; open(items.find(x => best(x.p, x.pt) === null) || items[0]); };
  $("#tback").onclick = () => go("");
}
function topicNav(){
  if (!view.topic || !view.paper) return "";
  const items = topicItems(view.topic), i = items.findIndex(x => x.p === view.paper && x.qi === view.q && x.pi === view.p);
  if (i < 0) return "";
  return `<div class="topicbar"><span>Topic: <strong>${esc(topicName(view.topic))}</strong> · ${i + 1} of ${items.length}</span><span style="flex:1"></span>
    <button class="btn small" id="tprev" ${i <= 0 ? "disabled" : ""}>← Previous in topic</button>
    <button class="btn small" id="tnext" ${i >= items.length - 1 ? "disabled" : ""}>Next in topic →</button>
    <button class="btn small" id="tlist">Topic list</button></div>`;
}
function wireTopicNav(){
  if (!view.topic) return;
  const items = topicItems(view.topic), i = items.findIndex(x => x.p === view.paper && x.qi === view.q && x.pi === view.p);
  const to = x => { if (x) go(`${x.p.id}/${x.qi}/${x.pi}`); };
  const a = $("#tprev"), b = $("#tnext"), c = $("#tlist");
  if (a) a.onclick = () => to(items[i - 1]);
  if (b) b.onclick = () => to(items[i + 1]);
  if (c) c.onclick = () => go("topic/" + view.topic);
}

function fmt(n){''')

# ---- exam: crumb + topic bar + tag line ----
rep('  $("#homeBtn").hidden = false; $("#crumb").textContent = paper.title;\n  $("#app").className = "exam";',
    '  $("#homeBtn").hidden = false; $("#crumb").textContent = view.topic ? `${topicName(view.topic)} · ${paper.short}` : paper.title;\n  $("#app").className = "exam";')
rep('''  $("#right").innerHTML = `
    <nav class="partnav" aria-label="Requireds">''',
'''  $("#right").innerHTML = `${topicNav()}
    <nav class="partnav" aria-label="Requireds">''')
rep('''    <div class="required">${esc(pt.required)}</div>''',
'''    <div class="tagline">Topics: ${(pt.topics || []).map(topicName).map(esc).join(" · ")}</div>
    <div class="required">${esc(pt.required)}</div>''')
rep('''    <label for="answer" class="hint">Your answer. Set calculations out like the exam: <span class="mono">Item | Reason/working | Amount</span>, one line each.</label>''',
'''    <label for="answer" class="hint">Your answer.${prefs.markLayout ? ` Set calculations out like the exam: <span class="mono">Item | Reason/working | Amount</span>, one line each.` : ""}</label>''')
rep('  const kb = $("#keyBtn2"); if (kb) kb.onclick = openKeyDlg;',
    '  const kb = $("#keyBtn2"); if (kb) kb.onclick = openKeyDlg;\n  wireTopicNav();')

open("template.html", "w", encoding="utf-8").write(t)
print("ok")

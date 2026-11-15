import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t = open("template.html", encoding="utf-8").read()
def rep(a, b):
    global t
    assert a in t, a[:70]
    t = t.replace(a, b, 1)

# preference: layout marking off by default
rep("const prefs = store._prefs || (store._prefs = { timer: false, showPaper: true, leftw: 50 });",
    "const prefs = store._prefs || (store._prefs = { timer: false, showPaper: true, leftw: 50 });\n"
    "if (prefs.markLayout === undefined) prefs.markLayout = false;")

# top-bar toggle
rep('  <button class="btn small toggle" id="timerBtn" hidden aria-pressed="false">Timer</button>',
    '  <button class="btn small toggle" id="timerBtn" hidden aria-pressed="false">Timer</button>\n'
    '  <button class="btn small toggle" id="layoutBtn" hidden aria-pressed="false" title="When off, only the tax content is marked: any format is fine and communication marks are given automatically.">Mark layout</button>')
rep('$("#paperBtn").onclick = () => { prefs.showPaper = !prefs.showPaper; save(); applyLayout(); };',
    '$("#paperBtn").onclick = () => { prefs.showPaper = !prefs.showPaper; save(); applyLayout(); };\n'
    '$("#layoutBtn").onclick = () => { prefs.markLayout = !prefs.markLayout; save(); applyLayout(); if (view.paper) renderRight(); };')
rep('  $("#paperBtn").hidden = !inExam; $("#timerBtn").hidden = !inExam;',
    '  $("#paperBtn").hidden = !inExam; $("#timerBtn").hidden = !inExam; $("#layoutBtn").hidden = !inExam;\n'
    '  $("#layoutBtn").setAttribute("aria-pressed", String(!!prefs.markLayout));')

# note above the answer box
rep('    <textarea id="answer" spellcheck="true" placeholder="Start writing…">',
    '    ${prefs.markLayout ? "" : `<div class="hint" style="margin-bottom:6px">Content-only marking: write it any way you like (lines, bullets, shorthand). Layout isn\'t marked.</div>`}\n'
    '    <textarea id="answer" spellcheck="true" placeholder="Start writing…">')

# prompt
rep("- Communication/critical thinking marks (X1, Y1, etc.) are awarded only if the answer is well structured and argued as the required asks (e.g. memo format, a table layout).",
    "${prefs.markLayout ? `- Communication/critical thinking marks (X1, Y1, etc.) are awarded only if the answer is well structured and argued as the required asks (e.g. memo format, a table layout).` : `- CONTENT-ONLY MARKING (the student chose this): mark only the tax substance: the correct treatment, amounts, workings, sections and the reason for each item, and conclusions. Accept ANY format: plain lines, bullet points, shorthand, abbreviations, no tables, no columns, no headings, no letter/memo/report format. A short reason in any form counts as the reason. Never deduct for layout, presentation, structure or format, even if the required asks for a specific layout.\\n- Award communication/critical thinking/presentation marks (X1, Y1, etc.) in full automatically, as long as the answer makes a genuine attempt at the content.\\n- Do not mention layout, format or presentation anywhere in the feedback or the exam tip.`}")

open("template.html", "w", encoding="utf-8").write(t)
print("ok")

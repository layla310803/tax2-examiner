import zipfile, re, json, sys
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
import xml.etree.ElementTree as ET
def mtext(e):
    # flatten OMML to readable linear text: fractions as (num)/(den), sub/sup with _ ^
    tag = e.tag.replace(M, "m:").replace(W, "w:")
    if tag == "m:f":
        num = e.find(M + "num"); den = e.find(M + "den")
        return "(" + mtext(num) + ")/(" + mtext(den) + ")"
    if tag in ("m:sSub",): return mtext(e.find(M + "e")) + "_" + mtext(e.find(M + "sub"))
    if tag in ("m:sSup",): return mtext(e.find(M + "e")) + "^" + mtext(e.find(M + "sup"))
    if tag == "m:sSubSup": return mtext(e.find(M + "e")) + "_" + mtext(e.find(M + "sub")) + "^" + mtext(e.find(M + "sup"))
    if tag == "m:d": return "(" + "".join(mtext(c) for c in e if c.tag == M + "e") + ")"
    if tag == "m:rad": return "sqrt(" + mtext(e.find(M + "e")) + ")"
    if tag in ("m:t", "w:t"): return e.text or ""
    return "".join(mtext(c) for c in e if not c.tag.endswith("Pr"))
def para_text(p):
    out = []
    for c in p.iter():
        pass
    def walk(e):
        for c in e:
            if c.tag == M + "oMath" or c.tag == M + "oMathPara": out.append(" " + mtext(c) + " ")
            elif c.tag == W + "t": out.append(c.text or "")
            elif c.tag == W + "tab": out.append(" ")
            elif c.tag in (W + "r", W + "hyperlink", W + "ins", W + "smartTag", W + "sdt", W + "sdtContent"): walk(c)
    walk(p)
    return re.sub(r"\s+", " ", "".join(out)).strip()
def extract(path, doc_label):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body"); secs = []; path_h = {}; cur = None
    def new(title, lvl):
        nonlocal cur
        path_h[lvl] = title
        for k in list(path_h):
            if k > lvl: del path_h[k]
        cur = {"d": doc_label, "h": " > ".join(path_h[k] for k in sorted(path_h)), "x": []}; secs.append(cur)
    for el in body:
        if el.tag == W + "p":
            st = el.find(f"{W}pPr/{W}pStyle"); st = st.get(W + "val") if st is not None else ""
            t = para_text(el)
            if not t: continue
            m = re.match(r"Heading(\d)", st) or (re.match(r"Title", st) and re.match(r"(.)", "1"))
            if m and st.startswith("Heading") and int(m.group(1)) <= 3: new(t, int(m.group(1)))
            else:
                if cur is None: new(doc_label, 1)
                cur["x"].append(t)
        elif el.tag == W + "tbl":
            if cur is None: new(doc_label, 1)
            for tr in el.iter(W + "tr"):
                cells = [" ".join(para_text(p) for p in tc.iter(W + "p")).strip() for tc in tr.iter(W + "tc")]
                cur["x"].append(" | ".join(c for c in cells if c))
    return [{"d": s["d"], "h": s["h"], "x": "\n".join(s["x"])} for s in secs if s["x"]]
if __name__ == "__main__":
    out = []
    for a in sys.argv[2:]:
        p, label = a.split("=>"); out += extract(p, label)
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "sections,", sum(len(s["x"]) for s in out), "chars")
    for s in out[:6]: print(" ", s["h"][:80], len(s["x"]))
    import collections; print(collections.Counter(s["d"] for s in out))

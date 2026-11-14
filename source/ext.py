import pymupdf, sys
def extract(path):
    d=pymupdf.open(path); out=[]
    for pi,p in enumerate(d):
        ws=p.get_text("words")
        ws.sort(key=lambda w:((w[1]+w[3])/2,w[0]))
        lines=[]
        for w in ws:
            yc=(w[1]+w[3])/2
            if lines and abs(lines[-1][0]-yc)<3.5: lines[-1][1].append(w)
            else: lines.append([yc,[w]])
        out.append(f"--- page {pi+1} ---")
        for yc,l in lines:
            l.sort(key=lambda w:w[0]); s=""; px=None
            for w in l:
                if px is not None: s+= "  |  " if w[0]-px>14 else " "
                s+=w[4]; px=w[2]
            out.append(s)
    return "\n".join(out)
for a in sys.argv[2:]:
    import os
    open(os.path.join(sys.argv[1],os.path.basename(a)[:-4]+".txt"),"w",encoding="utf-8").write(extract(a))

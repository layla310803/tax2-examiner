import re, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
S = HERE if os.path.isdir(os.path.join(HERE, "t2")) else os.path.dirname(HERE)
T2 = os.path.join(S, "t2")
T3 = os.path.join(S, "t3")
TOOLS = HERE
GEN = os.path.join(HERE, "generated")

# ---- command line: build.py OUT.html [--edition full|ylp] ----
_args = sys.argv[1:]
EDITION = "full"
if "--edition" in _args:
    _i = _args.index("--edition"); EDITION = _args[_i + 1]; del _args[_i:_i + 2]
assert EDITION in ("full", "ylp"), "edition must be full or ylp"
OUT = _args[0]

def finish(tpl, courses_json):
    """Inject the courses and the edition. /*FULL{*/ ... /*}FULL*/ marks code only the full edition keeps."""
    if EDITION == "full":
        tpl = tpl.replace("/*FULL{*/", "").replace("/*}FULL*/", "")
    else:
        tpl = re.sub(r"/\*FULL\{\*/.*?/\*\}FULL\*/", "", tpl, flags=re.S)
    assert "/*__COURSES__*/null" in tpl and '/*__EDITION__*/"full"' in tpl
    tpl = tpl.replace('/*__EDITION__*/"full"', json.dumps(EDITION)).replace("/*__COURSES__*/null", courses_json)
    open(OUT, "w", encoding="utf-8").write(tpl)
    print("wrote", OUT, EDITION, os.path.getsize(OUT))

if EDITION == "ylp":
    # Content-free edition: no built-in courses, and none of the course content folders are read.
    finish(open(os.path.join(TOOLS, "template.html"), encoding="utf-8").read(), "[]")
    sys.exit(0)

def load(name, d=None):
    return open(os.path.join(d or T2, name + ".txt"), encoding="utf-8").read().split("\n")

def clean(lines):
    out = []
    for l in lines:
        s = l.strip()
        if re.match(r"^--- page \d+ ---$", s): continue
        if s.startswith("©20"): continue
        if re.search(r"lOMoAR|Downloaded by|Studocu|studocu|Scan to open", s): continue
        if s.startswith("ACC3004W") or s.startswith("Suggested Solution") or s.startswith("Total marks") or s in ("Question 1","Question 2","October Exam"): continue
        if re.fullmatch(r"\d{1,2}", s): continue
        if re.fullmatch(r"(Available|Maximum|Limited|Limited to|Available marks|Maximum marks)(\s*\|.*)?", s) and False: continue
        out.append(s)
    return "\n".join(out).strip()

def find(lines, pat, start=0):
    r = re.compile(pat)
    for i in range(start, len(lines)):
        if r.search(lines[i]): return i
    raise SystemExit(f"pattern not found: {pat}")

def cut(lines, start_pat, end_pat=None, start=0):
    a = find(lines, start_pat, start)
    b = find(lines, end_pat, a + 1) if end_pat else len(lines)
    return clean(lines[a:b])

def memo_split(lines, markers):
    idx = []
    pos = 0
    for pid, pat in markers:
        i = find(lines, pat, pos); idx.append((pid, i)); pos = i + 1
    res = {}
    for k, (pid, i) in enumerate(idx):
        j = idx[k + 1][1] if k + 1 < len(idx) else len(lines)
        res[pid] = clean(lines[i:j])
    return res

# ---------- tax tables ----------
n25 = load("2025 November Final Exam")
TABLES_2025 = cut(n25, r"^MONETARY CHANGES")
n24 = load("2024 November Final Exam")
TABLES_2024 = cut(n24, r"^MONETARY CHANGES")

papers = []

# ================= NOV 2025 =================
m = load("2025 November Final Exam Solution")
memo = memo_split(m, [("1.1", r"^1\.1 Item"), ("1.2", r"^1\.2 On the date"), ("1.3", r"^1\.3 Amy"),
                      ("1.4", r"^1\.4 Item"), ("2.1", r"^Question 2"), ("2.2", r"^2\.2 VAT"),
                      ("2.3", r"^2\.3 VAT"), ("2.4", r"^2\.4 To:"), ("2.5", r"^2\.5 Ethical")])
papers.append({
  "id": "nov2025", "title": "November 2025 Final Exam", "short": "Nov 2025", "marks": 113, "yoa": "2025",
  "memoNote": "Official UCT suggested solution (no per-line mark allocation shown).",
  "tables": TABLES_2025,
  "questions": [
    {"id": "Q1", "title": "Question 1 — Sheldon & Amy Cooper", "marks": 56,
     "scenario": cut(n25, r"^QUESTION 1\s+\|", r"^REQUIRED - QUESTION 1"),
     "parts": [
       {"id": "1.1", "marks": 30, "required": "Calculate, with brief reasons, the employees' tax that would have been withheld by Big Bang (Pty) Ltd from Sheldon Cooper's salary for the month of December 2024.", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 7, "required": "Discuss, with supporting calculations, the income tax consequences for Sheldon Cooper on the date of his death in relation to:\n• His family home in Cape Town and\n• His apartment in Johannesburg\n(6 marks + 1 communication mark: clarity of expression)", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 12, "required": "Advise Amy Cooper, with supporting calculations, on the tax consequences relating to the apartments purchased and rented out and related costs for her year of assessment ended 28 February 2025.\n(11 marks + 1 communication mark: critical thinking)", "memo": memo["1.3"]},
       {"id": "1.4", "marks": 7, "required": "Calculate the Estate Duty that would be payable on Sheldon Cooper's death.", "memo": memo["1.4"]},
     ]},
    {"id": "Q2", "title": "Question 2 — Pure Aura (Pty) Ltd", "marks": 57,
     "scenario": cut(n25, r"^QUESTION 2\s+\|", r"^REQUIRED - QUESTION 2"),
     "parts": [
       {"id": "2.1", "marks": 11, "required": "Discuss the normal tax consequences for Pure Aura (Pty) Ltd for the lease of the building for the 2025 year of assessment.\n(10 marks + 1 communication mark: logical argument)", "memo": memo["2.1"]},
       {"id": "2.2", "marks": 17, "required": "Discuss all the tax implications for Pure Aura (Pty) Ltd for its 2025 year of assessment in relation to the note \"Distribution Division\".\n(16 marks + 1 mark: integrative thinking)", "memo": memo["2.2"]},
       {"id": "2.3", "marks": 17, "required": "Calculate, with brief reasons, the VAT and normal tax consequences of the other transactions in point 3 for Pure Aura (Pty) Ltd for the year of assessment ended 31 December 2025.", "memo": memo["2.3"]},
       {"id": "2.4", "marks": 7, "required": "Draft a memo advising the management of Pure Aura (Pty) Ltd on the tax implications for Pure Aura (Pty) Ltd of the agreement with the social media content creators for its year ended 31 December 2025.\n(6 marks + 1 communication mark: logical argument, format and structure)", "memo": memo["2.4"]},
       {"id": "2.5", "marks": 5, "required": "Explain to the management of Pure Aura (Pty) Ltd any ethical concerns you have in relation to management's response to the incident detailed in the note relating to the \"New Product Launch\".", "memo": memo["2.5"]},
     ]},
  ]})

# ================= JAN 2026 =================
m = load("2026 January Supplementary Exam Solution")
memo = memo_split(m, [("1.1", r"^1\.1 Printer"), ("1.2", r"^1\.2 Factory"), ("1.3", r"^Bad debts written off"),
                      ("1.4", r"^1\.4 Demo"), ("1.5", r"^Insurance$"), ("2.1", r"^Question 2"),
                      ("2.2", r"^2\.2 Item"), ("2.3", r"^2\.3 Item"), ("2.4", r"^2\.4 Employees"),
                      ("2.5", r"^2\.5 The provision")])
q1 = open(os.path.join(TOOLS, "jan26_q1.txt"), encoding="utf-8").read().strip()
q2 = open(os.path.join(TOOLS, "jan26_q2.txt"), encoding="utf-8").read().strip()
papers.append({
  "id": "jan2026", "title": "January 2026 Supplementary Exam", "short": "Jan 2026", "marks": 113, "yoa": "2025",
  "memoNote": "Official UCT suggested solution (no per-line mark allocation shown). Question paper transcribed from the scanned PDF.",
  "tables": TABLES_2025,
  "questions": [
    {"id": "Q1", "title": "Question 1 — Brew & Bean (Pty) Ltd", "marks": 56, "scenario": q1,
     "parts": [
       {"id": "1.1", "marks": 15, "required": "Calculate, with supporting reasons, the VAT and normal tax consequences of the new multifunction printer for Brew & Bean (Pty) Ltd for the 2025 year of assessment.", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 11, "required": "Discuss, with supporting calculations, the VAT and normal tax consequences of the factory building for Brew & Bean (Pty) Ltd for the 2025 year of assessment.\n(10 marks + 1 communication mark)", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 10, "required": "Calculate, with supporting reasons, the VAT and normal tax consequences for Brew & Bean (Pty) Ltd relating to the allowance for doubtful debts and the bad debts expense for the 2025 year of assessment.", "memo": memo["1.3"]},
       {"id": "1.4", "marks": 10, "required": "Discuss, with supporting calculations, the VAT and normal tax consequences of the trading stock for Brew & Bean (Pty) Ltd for the 2025 year of assessment.\n(9 marks + 1 communication mark)", "memo": memo["1.4"]},
       {"id": "1.5", "marks": 10, "required": "Discuss, with supporting calculations, the VAT and normal tax consequences of the insurance note for Brew & Bean (Pty) Ltd for the 2025 year of assessment.\nIn answering this required, you do not need to deal with the capital allowances on the vehicle.\n(9 marks + 1 communication mark)", "memo": memo["1.5"]},
     ]},
    {"id": "Q2", "title": "Question 2 — Chiedza Bombe", "marks": 57, "scenario": q2,
     "parts": [
       {"id": "2.1", "marks": 16, "required": "Review the draft remuneration calculation prepared by the financial accountant and identify all errors and/or omissions. Assume that all amounts are arithmetically correct. Present your answer in the following format:\n\nError/Omission  |  Correct treatment\ne.g. Incorrect salary amount  |  The accountant used R100 as the monthly salary instead of R200\n\nCalculations are not required.\n(15 marks + 1 mark: critical thinking)", "memo": memo["2.1"]},
       {"id": "2.2", "marks": 20, "required": "Starting with remuneration, calculate with brief reasons, Chiedza's taxable income for the 2025 year of assessment.\nYou may assume that the remuneration (correctly calculated) is R1 000 000.", "memo": memo["2.2"]},
       {"id": "2.3", "marks": 8, "required": "Calculate the estate duty payable by Chiedza's estate after her death.", "memo": memo["2.3"]},
       {"id": "2.4", "marks": 6, "required": "For this question only, ignore Chiedza's death.\nDiscuss whether employees' tax should be withheld by Books4Bargain on amounts paid to Chiedza in the 2026 year of assessment. Assume that all legislation and case law applicable in the 2025 year of assessment will also apply in 2026.", "memo": memo["2.4"]},
       {"id": "2.5", "marks": 7, "required": "Discuss the VAT effects for VanHuys (Pty) Ltd of the right of use of the motor vehicle given to Chiedza for the two-month VAT period ended 28 February 2025.\n(6 marks + 1 mark: integrated thinking)", "memo": memo["2.5"]},
     ]},
  ]})

# ================= STACKED =================
sq = load("Stacked question-exam prep 3")
m = load("Stacked Suggested Solution")
memo = memo_split(m, [("1.1", r"^1,1 Steward"), ("1.2", r"^The Tips are received"), ("1.3", r"^1,3 Employees"),
                      ("1.4", r"^Olivia is deemed to have disposed"), ("1.5", r"^1,5 Primary Rebate"),
                      ("1.6", r"^1\.6\. Primary residence")])
papers.append({
  "id": "stacked", "title": "Stacked (Pty) Ltd — Exam Prep Scenario", "short": "Stacked", "marks": 66, "yoa": "2025", "unofficial": True,
  "memoNote": "Suggested solution from Studocu (has per-line marks). Not an official UCT memo, so it may contain errors. The marker is told to follow the law where the memo is clearly wrong.",
  "tables": TABLES_2025,
  "questions": [
    {"id": "Q1", "title": "Question 1 Part A — Stacked, Katherine Kaley & Olivia Battle", "marks": 66,
     "scenario": cut(sq, r"^STACKED", r"^REQUIRED:"),
     "parts": [
       {"id": "1.1", "marks": 11, "required": "Discuss, with supporting calculations, the tax consequences for both Steward Watson and Stacked (Pty) Ltd of the hamper awarded to the employee of the month for the 2025 year of assessment.\n(10 marks + 1 communication mark: clarity of expression)", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 6, "required": "Discuss the normal tax consequences of the tips for the waiters and Stacked (Pty) Ltd.\n(5 marks + 1 communication mark: clarity of expression)", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 20, "required": "Calculate, with reasons, the total employees' tax that was withheld from Katherine Kaley for the year of assessment ended 28 February 2025.", "memo": memo["1.3"]},
       {"id": "1.4", "marks": 11, "required": "Calculate the taxable capital gain that would be included in Olivia Battle's taxable income at the date of her death.", "memo": memo["1.4"]},
       {"id": "1.5", "marks": 11, "required": "Calculate, with reasons, the rebates that will be available to Olivia Battle in the determination of her normal tax for the 2025 year of assessment.", "memo": memo["1.5"]},
       {"id": "1.6", "marks": 7, "required": "Calculate the Estate Duty that would be payable to SARS due to Olivia Battle's death.\nIn answering this question, you may assume that the normal tax payable by Olivia at the date of her death was R420 000.", "memo": memo["1.6"]},
     ]},
  ]})

# ================= NOV 2024 =================
m = load("2024 November Final Exam Solution")
memo = memo_split(m, [("1.1", r"^To: The Financial Director"), ("1.2", r"^1\.2 Current"), ("1.3", r"^1\.3 Supply"),
                      ("1.4", r"^1\.4 Normal"), ("1.5", r"^1\.5 ClutterClear"), ("1.6", r"^Part B"),
                      ("1.7", r"^2 Item\s+\|\s+Reasons"), ("2.1", r"^Question 2"), ("2.2", r"^2\.2 Salary"),
                      ("2.3", r"^2\.3 Lease")])
papers.append({
  "id": "nov2024", "title": "November 2024 Final Exam", "short": "Nov 2024", "marks": 113, "yoa": "2024",
  "memoNote": "Official UCT suggested solution with per-line mark allocation.",
  "tables": TABLES_2024,
  "questions": [
    {"id": "Q1A", "title": "Question 1 Part A — ClutterClear Solutions (Pty) Ltd", "marks": 44,
     "scenario": cut(n24, r"^QUESTION 1\s+\|", r"^REQUIRED"),
     "parts": [
       {"id": "1.1", "marks": 8, "required": "Write a memorandum to the financial director of ClutterClear Solutions (Pty) Ltd discussing whether the recall and rebranding expenses will be deductible for ClutterClear Solutions (Pty) Ltd for its year of assessment ending 31 December 2024.\n(7 marks + 1 communication mark: layout and structure)", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 15, "required": "Calculate, with supporting reasons, the normal tax effects of the single cab delivery vehicle and the double cab light delivery vehicle for the year of assessment ending 31 December 2024.", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 7, "required": "Discuss the VAT consequences for ClutterClear Solutions (Pty) Ltd for the service provided to Amanda on the organising of her home.", "memo": memo["1.3"]},
       {"id": "1.4", "marks": 8, "required": "Discuss whether there will be normal tax and VAT consequences on the goods sold outside South Africa and the services provided outside South Africa for ClutterClear Solutions (Pty) Ltd.\nAdditionally, briefly explain to ClutterClear Solutions (Pty) Ltd whether there will be any difference on the VAT consequences if the company provides the services from South Africa or in Namibia.\nIn answering this question, you may assume that the 2024 legislation remains the same for the 2025 year of assessment. You can ignore any double tax agreements.\n(7 marks + 1 communication mark: logical argument)", "memo": memo["1.4"]},
       {"id": "1.5", "marks": 6, "required": "While ClutterClear Solutions (Pty) Ltd is a registered category B VAT vendor, discuss whether they would be allowed to, and whether they would want to, deregister for VAT purposes.\n(5 marks + 1 communication mark: logical argument)", "memo": memo["1.5"]},
     ]},
    {"id": "Q1B", "title": "Question 1 Part B — Tshifhiwa Malange (ignore VAT)", "marks": 28,
     "scenario": cut(n24, r"^Part B$", r"^REQUIRED"),
     "parts": [
       {"id": "1.6", "marks": 18, "required": "Discuss, with supporting calculations, the tax consequences of the items that Tshifhiwa Malange donated during the current year of assessment.\nIn answering this question, you do not have to include when the tax is payable. You can also assume that these are the only disposals she made in the current year.\n(17 marks + 1 communication mark: logical argument)", "memo": memo["1.6"]},
       {"id": "1.7", "marks": 10, "required": "Calculate, with supporting reasons, the Estate Duty that would be payable to SARS due to Tshifhiwa Malange's death.\nIn answering this question, you can ignore capital gains tax consequences.", "memo": memo["1.7"]},
     ]},
    {"id": "Q2", "title": "Question 2 — Saarah Williams / ModestChic Designs", "marks": 41,
     "scenario": cut(n24, r"^QUESTION 2\s+\|", r"^REQUIRED"),
     "parts": [
       {"id": "2.1", "marks": 7, "required": "Explain to Saarah Williams, using taxation legislation in the Income Tax Act No. 58 of 1962, whether the statement from her friend is true and whether or not she will be able to deduct those expenses.\n(6 marks + 1 communication mark: logical argument)", "memo": memo["2.1"]},
       {"id": "2.2", "marks": 22, "required": "Calculate, with reasons, Saarah Williams' taxable income for the 2024 year of assessment.", "memo": memo["2.2"]},
       {"id": "2.3", "marks": 12, "required": "Discuss, with supporting calculations, the normal tax effects of Saarah Williams entering into the lease agreement for the new property for her year of assessment ending 28 February 2025.\nIn answering this question, you may assume that the 2024 legislation remains the same for the 2025 year of assessment.\n(11 marks + 1 communication mark: logical argument)", "memo": memo["2.3"]},
     ]},
  ]})

# ================= JAN 2025 =================
j25 = load("2025 January Supplementary Exam")
m = load("2025 January Supplementary Exam Solution")
memo = memo_split(m, [("1.1", r"^1\.1 Disposal"), ("1.2", r"^1\.2 Cold"), ("1.3", r"^1\.3 Description"),
                      ("2.1", r"^Suggested Solution - Question 2"), ("2.2", r"^2,2 Right"),
                      ("2.3", r"^2\.3 Offshore"), ("2.4", r"^2\.4 Employees")])
papers.append({
  "id": "jan2025", "title": "January 2025 Supplementary Exam", "short": "Jan 2025", "marks": 113, "yoa": "2024",
  "memoNote": "Official UCT suggested solution with per-line mark allocation.",
  "tables": TABLES_2024,
  "questions": [
    {"id": "Q1", "title": "Question 1 — Cold Press Nation (Pty) Ltd", "marks": 50,
     "scenario": cut(j25, r"^QUESTION 1\s+\|", r"^REQUIRED – QUESTION 1"),
     "parts": [
       {"id": "1.1", "marks": 8, "required": "Discuss, with supporting calculations, the VAT consequences for Cold Press Nation (Pty) Ltd for transactions in notes 3 and 4 for the 2024 year of assessment.", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 9, "required": "Discuss the donations tax consequences for all the donations made by Cold Press Nation (Pty) Ltd during the 2024 year of assessment.\n(8 marks + 1 communication mark: logical argument)", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 33, "required": "Critically review the income tax expense calculation performed by the tax accountant of Cold Press Nation (Pty) Ltd for the year ended 31 July 2024.\nIn answering this question:\n• Indicate the line items that were treated correctly for income tax purposes and provide a brief reason therefor\n• Identify the errors in the calculation\n• Where there was an error, briefly discuss why this is an error AND provide the correct treatment\n• Where there was an omission, provide the correct treatment\nPresent your solution as:  Description  |  Error/Omission  |  Reason and/or working  |  Correct treatment\n(31 marks + 2 communication marks: layout and structure, logical argument)", "memo": memo["1.3"]},
     ]},
    {"id": "Q2", "title": "Question 2 — Lindela & Mhlengi Malange", "marks": 63,
     "scenario": cut(j25, r"^QUESTION 2\s+\|", r"^REQUIRED$"),
     "parts": [
       {"id": "2.1", "marks": 22, "required": "Calculate the employee's tax that will be withheld by Total Fitness for Lindela Malange for the month of January 2024.", "memo": memo["2.1"]},
       {"id": "2.2", "marks": 20, "required": "Discuss the tax consequences for Total Fitness for the transactions in Note 2 and 3 for the 2024 year of assessment.\n(19 marks + 1 communication mark: logical argument)", "memo": memo["2.2"]},
       {"id": "2.3", "marks": 16, "required": "Discuss the normal tax consequences for Lindela Malange for ALL the investments (refer to Investments) that she holds in the 2024 year of assessment.\n(15 marks + 1 communication mark: logical argument)", "memo": memo["2.3"]},
       {"id": "2.4", "marks": 5, "required": "Advise Mhlengi Malange whether the accounting firm is required to withhold employee's tax in relation to the amounts paid to him by the firm.", "memo": memo["2.4"]},
     ]},
  ]})


# ================= NOV 2021 (Studocu) =================
e21 = load("[studocu.com] - ACC3004H November Exam - Taxation II Assessment 2021", T3)
m = load("[studocu.com] - ACC3004H - Final Exam Suggested Solutions for November 2020", T3)
memo = memo_split(m, [("1.1", r"^1\.1$"), ("1.2", r"^1\.2 Trading"), ("1.3", r"^1\.3$"), ("1.4", r"^1\.4$"),
                      ("1.5", r"^1\.5 CT Glass"), ("2.1", r"^2\.1 Donations"), ("2.2", r"^2\.2 A donation"),
                      ("2.3", r"^2\.3$"), ("2.4", r"^2\.4$"), ("2.5", r"^2\.5 Estate")])
papers.append({
  "id": "nov2021", "title": "November 2021 Final Exam (ACC3004H)", "short": "Nov 2021", "marks": 120, "yoa": "2021", "unofficial": True,
  "memoNote": "Suggested solution from Studocu (filed as 'November 2020' but it matches this paper). Older legislation (2021 year of assessment): mark against the law and tables in this paper.",
  "tables": cut(e21, r"^MONETARY CHANGES"),
  "questions": [
    {"id": "Q1", "title": "Question 1 — CT Glass and Aluminium (Pty) Ltd", "marks": 65,
     "scenario": cut(e21, r"^QUESTION 1 \(65", r"^REQUIRED$"),
     "parts": [
       {"id": "1.1", "marks": 10, "required": "Discuss, with reference to legislation and case law, the normal tax consequences for CT Glass and Aluminium (Pty) Ltd during the current year of assessment relating to:\n• The medical costs paid to the employee (9)\n• The related legal costs paid to the lawyer (10)\n(+ 1 communication mark: logical argument)", "memo": memo["1.1"]},
       {"id": "1.2", "marks": 16, "required": "Discuss, with supporting calculations, the VAT consequences, if any, for CT Glass and Aluminium (Pty) Ltd of:\n• The purchase of trading stock from the Chinese supplier (6)\n• The Toyota Hilux double cab bakkie (4)\n• The building in Bellville (5)\n(+ 1 communication mark: logical argument)", "memo": memo["1.2"]},
       {"id": "1.3", "marks": 3, "required": "Discuss, with supporting calculations, the VAT consequences, if any, for the Toyota dealership of the Hilux double cab bakkie.", "memo": memo["1.3"]},
       {"id": "1.4", "marks": 27, "required": "Calculate, with reasons, the taxable income of CT Glass and Aluminium (Pty) Ltd for the year ended 31 March 2021.", "memo": memo["1.4"]},
       {"id": "1.5", "marks": 9, "required": "Discuss, with reference to legislation and case law, the normal tax consequences for:\n• CT Glass and Aluminium (Pty) Ltd of the payment to the government employee.\n• The government employee of the receipt of the payment. (5)\nIn addition, discuss any ethical concerns that you have with the above transactions. (3)\n(+ 1 communication mark: logical argument)", "memo": memo["1.5"]},
     ]},
    {"id": "Q2", "title": "Question 2 — Sibu Mpiti / Z Prop (Pty) Ltd", "marks": 55,
     "scenario": cut(e21, r"^QUESTION 2\s+\|\s+\(55", r"^REQUIRED$"),
     "parts": [
       {"id": "2.1", "marks": 7, "required": "Calculate, with reasons, the donations tax payable by Sibu Mpiti.\nIn answering this question, indicate when the donations tax would have been due to SARS.", "memo": memo["2.1"]},
       {"id": "2.2", "marks": 11, "required": "Discuss, with supporting calculations, the capital gains tax consequences of the donations Sibu Mpiti has made during the current year of assessment.", "memo": memo["2.2"]},
       {"id": "2.3", "marks": 21, "required": "Calculate with reasons Sibu Mpiti's normal tax payable to SARS for the 2021 year of assessment.", "memo": memo["2.3"]},
       {"id": "2.4", "marks": 6, "required": "Discuss the tax consequences for Z Prop (Pty) Ltd relating to the Macbook Pro laptop for the current year of assessment.\n(5 marks + 1 communication mark: logical argument)", "memo": memo["2.4"]},
       {"id": "2.5", "marks": 10, "required": "Calculate, with reasons, the estate duty payable due to Sibu Mpiti's death.", "memo": memo["2.5"]},
     ]},
  ]})


# ================= NotebookLM-generated memos =================
def gen(name):
    return open(os.path.join(GEN, name), encoding="utf-8").read().split("\n")
GEN_NOTE = "Memo generated with NotebookLM from your Tax 2 notebook. It is not an official solution, so check anything that looks off."

rq = load("Rockit Backpackers Ltd", T3)
memo = memo_split(gen("rockit_memo.txt"), [(str(i), rf"^Required {i}:") for i in range(1, 7)])
papers.append({"id": "rockit", "title": "Rockit Backpackers Ltd — VAT Scenario", "short": "Rockit", "marks": 41, "yoa": "2025", "unofficial": True,
  "memoNote": GEN_NOTE, "tables": TABLES_2025,
  "questions": [{"id": "Q1", "title": "Rockit Backpackers Ltd (VAT)", "marks": 41, "scenario": cut(rq, r"^Rockit Backpackers", r"^REQUIRED:"),
    "parts": [
      {"id": "1", "marks": 3, "required": "Briefly explain when a person should register as a VAT vendor.", "memo": memo["1"]},
      {"id": "2", "marks": 2, "required": "Briefly explain the difference between direct and indirect taxes, giving an example of each.", "memo": memo["2"]},
      {"id": "3", "marks": 6, "required": "Discuss, with supporting calculations, what the VAT consequences would be for Rockit Backpackers Ltd relating to the purchase of the two vehicles in Note 4.\n(5 marks + 1 communication mark: logical argument)", "memo": memo["3"]},
      {"id": "4", "marks": 16, "required": "Calculate, with reasons, the net VAT payable/receivable by Rockit Backpackers Ltd for the VAT period ending 31 October 2024 relating to notes 1 – 7.\nYour solution must also include an explanation for any item mentioned in the scenario that you have specifically excluded from your calculation.\nPresent it as:  Description  |  Reasons  |  VAT input  |  VAT output", "memo": memo["4"]},
      {"id": "5", "marks": 6, "required": "Discuss, with supporting calculations, what the VAT consequences would be for Rockit Backpackers Ltd during the November 2024 VAT period under review of the transactions detailed in Note 8.\n(5 marks + 1 communication mark: logical argument)", "memo": memo["5"]},
      {"id": "6", "marks": 8, "required": "Provide, with reasons, the correcting journal entries, if necessary, for the three journal entries the assistant accountant of Rockit Backpackers Ltd asked you to review.\nYour solution must also include an explanation for any transactions that do not require a correcting journal entry.", "memo": memo["6"]},
    ]}]})

gq = load("Gino Todd scenario-exam 5", T3)
memo = memo_split(gen("gino_memo.txt"), [("A", r"^PART A"), ("B", r"^PART B")])
papers.append({"id": "gino", "title": "Gino Todd — Individuals Scenario", "short": "Gino Todd", "marks": 34, "yoa": "2025", "unofficial": True,
  "memoNote": GEN_NOTE, "tables": TABLES_2025,
  "questions": [{"id": "Q1", "title": "Gino Todd / Market-It Ltd", "marks": 34, "scenario": cut(gq, r"^Gino Todd", r"^REQUIRED:"),
    "parts": [
      {"id": "A", "marks": 25, "required": "Calculate, providing reasons where appropriate, Gino's normal tax for the year of assessment ended 28 February 2025.", "memo": memo["A"]},
      {"id": "B", "marks": 9, "required": "Gino has been considering whether he should start up his own company, Gino's Consultancy (Pty) Ltd, and provide his services to Market-It through this company in order to minimize the amount of employee's tax he is paying.\nDiscuss whether the establishment of this company will in fact reduce his employee's tax.\n(8 marks + 1 communication mark: logic and expression)", "memo": memo["B"]},
    ]}]})

uq = load("Uhuru scenario exam 7", T3)
memo = memo_split(gen("uhuru_memo.txt"), [(f"1.{i}", rf"^Required 1\.{i}") for i in range(1, 5)])
papers.append({"id": "uhuru", "title": "Uhuru (Pty) Ltd — Employees' Tax Scenario", "short": "Uhuru", "marks": 37, "yoa": "2025", "unofficial": True,
  "memoNote": GEN_NOTE, "tables": TABLES_2025,
  "questions": [{"id": "Q1", "title": "Uhuru (Pty) Ltd / Nomveliso Zungu", "marks": 37, "scenario": cut(uq, r"^Uhuru\s+\|", r"^REQUIRED:"),
    "parts": [
      {"id": "1.1", "marks": 16, "required": "Calculate, with reasons, the employees' tax that would have been withheld by Uhuru (Pty) Ltd from Nomveliso Zungu for the 2025 year of assessment.", "memo": memo["1.1"]},
      {"id": "1.2", "marks": 12, "required": "Advise Nomveliso Zungu which of the two options relating to the restructuring of her remuneration package would be the most tax beneficial to her in the 2026 year of assessment.\n• Assume that the tax legislation applicable to the 2025 year of assessment will remain unchanged for the 2026 year of assessment.\n• Assume that each option will be in effect from 1 March 2025 for the whole year of assessment.", "memo": memo["1.2"]},
      {"id": "1.3", "marks": 5, "required": "Discuss the VAT consequences for Uhuru (Pty) Ltd:\n• On the amounts paid to Stuttafords Van Liners (Pty) Ltd relating to Nomveliso Zungu's move to Durban in November 2024; and\n• On the possible right of use of the Toyota Corolla granted to Nomveliso Zungu on 1 March 2025.", "memo": memo["1.3"]},
      {"id": "1.4", "marks": 4, "required": "Advise Takunda Bhezuzi on the South African normal tax consequences relating to the Westville property lease payments made by Uhuru (Pty) Ltd.", "memo": memo["1.4"]},
    ]}]})

sq2 = load("Stirology scenario-exam prep 2", T3)
memo = memo_split(gen("stirology_memo.txt"), [(f"1.{i}", rf"^Required 1\.{i}") for i in range(1, 5)])
papers.append({"id": "stirology", "title": "Stirology (Pty) Ltd — Company Scenario", "short": "Stirology", "marks": 56, "yoa": "2025", "unofficial": True,
  "memoNote": GEN_NOTE, "tables": TABLES_2025,
  "questions": [{"id": "Q1", "title": "Stirology (Pty) Ltd (Jan 2022 supp Q1)", "marks": 56, "scenario": cut(sq2, r"^QUESTION 1\s+\|\s+\(56", r"^REQUIRED$"),
    "parts": [
      {"id": "1.1", "marks": 9, "required": "Discuss whether Stirology (Pty) Ltd meets the requirements to be considered a 'small business corporation' as defined in the Income Tax Act (Act 58 of 1962).\n(8 marks + 1 communication mark: logical argument)\n\nIn answering the following questions, you may assume that Stirology (Pty) Ltd is and has always been a small business corporation.", "memo": memo["1.1"]},
      {"id": "1.2", "marks": 12, "required": "Discuss, with reference to case law and the Income Tax Act (Act 58 of 1962), whether the customer settlement outlined in Note 2 may be claimed as a deduction by Stirology (Pty) Ltd.\n(11 marks + 1 communication mark: logical argument)", "memo": memo["1.2"]},
      {"id": "1.3", "marks": 18, "required": "Calculate, with supporting reasons, all the VAT effects for Stirology (Pty) Ltd for the year ended 31 October 2025 relating to:\n• All employee benefits granted to the employees of Stirology (Pty) Ltd (Note 3)\n• All fixed assets, other income and expenditure of Stirology (Pty) Ltd (Note 4)", "memo": memo["1.3"]},
      {"id": "1.4", "marks": 17, "required": "Calculate, with supporting reasons, Stirology's taxable income for its year ended 31 October 2025.", "memo": memo["1.4"]},
    ]}]})


# sanity
for p in papers:
    tot = sum(pt["marks"] for q in p["questions"] for pt in q["parts"])
    print(p["id"], "parts total", tot, "declared", p["marks"])
    for q in p["questions"]:
        print("  ", q["id"], sum(pt["marks"] for pt in q["parts"]), "/", q["marks"], "scenario chars", len(q["scenario"]))
        for pt in q["parts"]:
            print("     ", pt["id"], "memo:", pt["memo"][:70].replace("\n", " / "), "...", pt["memo"][-50:].replace("\n", " / "))

tpl = open(os.path.join(TOOLS, "template.html"), encoding="utf-8").read()

# ================= topic tags (for "Practise by topic") =================
TOPICS = [
  ("ind", "Individuals: taxable income & normal tax"),
  ("emp", "Employees' tax (PAYE)"),
  ("loss", "Assessed losses"),
  ("ed", "Estate duty"),
  ("vat", "VAT"),
  ("cap", "Capital allowances & recoupments"),
  ("lease", "Leases: premiums & improvements"),
  ("fringe", "Fringe benefits (Seventh Schedule)"),
  ("co", "Companies: deductions & taxable income"),
  ("cgt", "Capital gains tax"),
  ("don", "Donations tax"),
  ("intl", "Residence & foreign income"),
  ("eth", "Ethics & tax avoidance"),
]
TAGS = {
  "nov2025": {"1.1": "emp fringe", "1.2": "cgt ind", "1.3": "ind vat loss", "1.4": "ed", "2.1": "co lease", "2.2": "vat co cap",
              "2.3": "vat co fringe", "2.4": "vat co don", "2.5": "eth"},
  "jan2026": {"1.1": "vat co cap", "1.2": "vat cap", "1.3": "vat co", "1.4": "vat co", "1.5": "vat co cap",
              "2.1": "emp fringe", "2.2": "ind", "2.3": "ed", "2.4": "emp", "2.5": "vat fringe"},
  "stacked": {"1.1": "fringe co", "1.2": "ind emp", "1.3": "emp fringe", "1.4": "cgt", "1.5": "ind", "1.6": "ed"},
  "nov2024": {"1.1": "co", "1.2": "cap", "1.3": "vat", "1.4": "intl vat co", "1.5": "vat", "1.6": "don cgt", "1.7": "ed",
              "2.1": "ind", "2.2": "ind", "2.3": "ind lease"},
  "jan2025": {"1.1": "vat", "1.2": "don", "1.3": "co cap", "2.1": "emp fringe", "2.2": "vat fringe co", "2.3": "ind intl", "2.4": "emp"},
  "nov2021": {"1.1": "co", "1.2": "vat", "1.3": "vat", "1.4": "co cap", "1.5": "co eth", "2.1": "don", "2.2": "cgt",
              "2.3": "ind loss", "2.4": "fringe vat co", "2.5": "ed"},
  "rockit": {k: "vat" for k in ["1", "2", "3", "4", "5", "6"]},
  "gino": {"A": "ind fringe", "B": "emp"},
  "uhuru": {"1.1": "emp fringe", "1.2": "fringe ind", "1.3": "vat fringe", "1.4": "intl"},
  "stirology": {"1.1": "co", "1.2": "co", "1.3": "vat fringe", "1.4": "co cap"},
}
_valid = {k for k, _ in TOPICS}
for _p in papers:
    for _q in _p["questions"]:
        for _pt in _q["parts"]:
            _tags = TAGS.get(_p["id"], {}).get(_pt["id"], "").split()
            assert _tags, f"untagged {_p['id']} {_pt['id']}"
            assert set(_tags) <= _valid, _tags
            _pt["topics"] = _tags

# ================= quick-quiz question bank =================
import sys
sys.path.insert(0, HERE)
from quiz_bank import BANK
assert set(BANK) <= _valid, set(BANK) - _valid
def _q(item):
    q, a, chk = item
    out = {"q": q, "a": a}
    if isinstance(chk, (int, float)): out["n"] = chk
    else:
        pats = [chk] if isinstance(chk, str) else list(chk)
        for pat in pats: re.compile(pat)
        out["k"] = pats
    return out
QUIZ_JSON = json.dumps({k: [_q(x) for x in v] for k, v in BANK.items()}, ensure_ascii=False).replace("</", "<\\/")
print("quiz bank:", {k: len(v) for k, v in BANK.items()}, "total", sum(len(v) for v in BANK.values()))

# ================= Banking (FTX4087S): papers are JSON files in source/banking =================
import glob, importlib.util
BANK_DIR = os.path.join(HERE, "banking")
B_TOPICS = [
  ("b-intro", "Introduction to banking & business models"),
  ("b-fin", "Bank financial statements & ratios"),
  ("b-val", "Bank valuation"),
  ("b-treas", "Corporate treasury & working capital"),
  ("b-mnc", "Multinational treasury (FX, hedging, netting)"),
  ("b-money", "Banks, money creation & monetary policy"),
  ("b-reg", "Bank regulation (Basel, capital, liquidity)"),
  ("b-fail", "Bank failures"),
  ("b-risk", "Risk overview, RAROC & operational risk"),
  ("b-credit", "Credit risk"),
  ("b-irr", "Interest rate risk (gap, duration)"),
  ("b-mkt", "Market risk (VaR, portfolio theory)"),
]
_bvalid = {k for k, _ in B_TOPICS}
_fs = os.path.join(BANK_DIR, "formula_sheet.txt")
B_FORMULAS = open(_fs, encoding="utf-8").read().strip() if os.path.exists(_fs) else ""
_KIND = {"test": 0, "exam": 1, "workshop": 2}
b_papers = []
for _f in sorted(glob.glob(os.path.join(BANK_DIR, "b-*.json"))):
    _p = json.load(open(_f, encoding="utf-8"))
    assert _p["id"].startswith("b-") and _p["kind"] in _KIND, _f
    _tot = 0
    for _bq in _p["questions"]:
        _bq.setdefault("scenario", "")
        _qt = 0
        for _pt in _bq["parts"]:
            assert _pt["required"].strip() and _pt["memo"].strip(), (_f, _pt["id"])
            _pt["topics"] = [t for t in _pt.get("topics", []) if t in _bvalid]
            assert _pt["topics"], f"untagged {_p['id']} {_pt['id']}"
            _qt += _pt["marks"]
        if _qt != _bq["marks"]: print("  note:", _p["id"], _bq["id"], "parts", _qt, "declared", _bq["marks"], "-> using parts total")
        _bq["marks"] = _qt; _tot += _qt
    assert len({pt["id"] for q in _p["questions"] for pt in q["parts"]}) == sum(len(q["parts"]) for q in _p["questions"]), f"duplicate part ids in {_f}"
    if _tot != _p["marks"]: print("  note:", _p["id"], "total", _tot, "declared", _p["marks"], "-> using parts total")
    _p["marks"] = _tot
    _p.setdefault("memoNote", "Memo from the course material.")
    _p["tables"] = B_FORMULAS
    b_papers.append(_p)
    print(_p["id"], _p["kind"], _p["marks"], "marks", sum(len(q["parts"]) for q in _p["questions"]), "parts")
# ---- Old interest rates: rates.json gives, per question, a current-rate version (Settings > Use current interest rates) and the notes ----
_rf = os.path.join(BANK_DIR, "rates.json")
B_RATES = None
if os.path.exists(_rf):
    _R = json.load(open(_rf, encoding="utf-8"))
    B_RATES = {"asAt": _R["asAt"], "repo": _R["repo"], "prime": _R["prime"]}
    _now = f"Today's rates (as at {_R['asAt']}): repo {_R['repo']}, prime {_R['prime']}."
    def _subs(txt, pairs, where):
        for a, b in pairs:
            assert txt.count(a) == 1, f"rates.json: {a!r} not found once in {where}"
            txt = txt.replace(a, b)
        return txt
    _byid = {p["id"]: p for p in b_papers}
    for it in _R["items"]:
        _p = _byid[it["paper"]]
        _pts = {pt["id"]: (q, pt) for q in _p["questions"] for pt in q["parts"]}
        if it.get("scenario"):
            _rq = next(q for q in _p["questions"] if q["id"] == it["question"])
            _rq["rates"] = {"scenario": _subs(_rq["scenario"], it["scenario"], f"{_p['id']} {_rq['id']} scenario")}
        for pid in it["parts"]:
            _pt = _pts[pid][1]
            cur = {f: _subs(_pt[f], pairs, f"{_p['id']} {pid} {f}") for f, pairs in it.get("sub", {}).get(pid, {}).items()}
            _pt["rates"] = {**cur,
                "notePaper": f"Paper's rates: this question uses {it['old']}. {_now} Turn on 'Use current interest rates' in Settings to see it with today's rates.",
                "noteNow": f"Current rates: this question has been updated to today's rates (as at {_R['asAt']}: repo {_R['repo']}, prime {_R['prime']}). The original paper used {it['old']}." + (" " + it["nowExtra"] if it.get("nowExtra") else "")}
    print("banking rates:", sum(len(it["parts"]) for it in _R["items"]), "parts with current-rate versions")
def _year(p):
    m = re.search(r"20\d\d", p["title"]); return -int(m.group()) if m else 0
b_papers.sort(key=lambda p: (_KIND[p["kind"]], _year(p), p["title"]))
b_quiz = {}
_qb = os.path.join(BANK_DIR, "quiz_bank.py")
if os.path.exists(_qb):
    _spec = importlib.util.spec_from_file_location("bank_quiz_bank", _qb); _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    assert set(_mod.BANK) <= _bvalid, set(_mod.BANK) - _bvalid
    b_quiz = {k: [_q(x) for x in v] for k, v in _mod.BANK.items()}
    for k, v in getattr(_mod, "HARD", {}).items():   # exam-level tier, appended so existing indices stay put
        assert k in _bvalid, k
        b_quiz.setdefault(k, []).extend(dict(_q(x), h=1) for x in v)
    print("banking quiz bank:", {k: len(v) for k, v in b_quiz.items()}, "total", sum(len(v) for v in b_quiz.values()))
b_cards = None
_fc = os.path.join(BANK_DIR, "flashcards.py")
if os.path.exists(_fc):
    _spec = importlib.util.spec_from_file_location("bank_flashcards", _fc); _fmod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_fmod)
    assert set(_fmod.CARDS) <= _bvalid, set(_fmod.CARDS) - _bvalid
    b_cards = {k: [[f.strip(), b.strip()] for f, b in v] for k, v in _fmod.CARDS.items()}
    print("banking flash cards:", {k: len(v) for k, v in b_cards.items()}, "total", sum(len(v) for v in b_cards.values()))
# ---- Banking exam scope (FTX4087S final, Nov 2026): lecturer guidance. Rules match the question / card front / required text only (not answers, which may mention VaR in passing) ----
B_SCOPE = {
  "notExaminedTopics": ["b-mkt"],
  "rules": [
    {"id": "market", "topics": ["b-risk", "b-irr", "b-credit", "b-reg"], "pattern": r"value at risk|\bVaR\b|market risk(?!\s*premium)", "reason": "Market risk is not examined (Huang)"},
    {"id": "operational", "topics": ["b-risk"], "pattern": r"operational risk|\bop(?:erational)?\.?\s*risk|event types?|internal fraud|external fraud", "reason": "Operational risk is not examined (Huang)"},
    {"id": "liquidity", "topics": ["b-risk"], "pattern": r"liquidity risk|funding liquidity|market liquidity", "reason": "Liquidity risk (Risk Management slides) is not examined (Huang)"},
    {"id": "durgap", "topics": ["b-irr"], "pattern": r"duration gap|leverage[- ]adjusted|immunis|market value of (the bank's )?equity|change in (the )?(bank's )?equity|MVE", "reason": "Not in the 2026 Risk Management slides (Huang): duration gap model"},
    {"id": "stress", "topics": ["b-risk", "b-credit", "b-irr"], "pattern": r"stress[- ]test", "reason": "Not in the 2026 Risk Management slides outside the excluded market risk pages (Huang): stress testing"},
    {"id": "ddm", "topics": ["b-val"], "pattern": r"dividend discount|\bDDM\b|gordon growth", "reason": "Dividend discount model slides are not examinable (Kruger)"},
  ],
  "focus": [
    "Know the slides and the workshop questions well (all three lecturers)",
    "Read \"Bank Governance Lessons Still Not Learned\" (De Jager, Amathuba 11 Nov)",
    "Everything else in Kruger's work, including Topic 5 Multinational Corporations, now fully examinable (Kruger, Amathuba 26 Oct)",
    "Prior-year exams are good practice, though not set by Huang (Huang, email)",
  ],
  "notExamined": [
    "Market risk, slide set 3 pages 18-36 (Huang, email)",
    "Liquidity risk, slide set 1 pages 13-17 (Huang, email)",
    "Operational risk, slide set 1 pages 7-9 (Huang, email)",
    "Duration gap model, and stress testing outside the excluded market risk pages: not in the 2026 Risk Management slides (checked against the slides)",
    "Dividend discount model slides in Topic 3 Bank Valuations (Kruger, Amathuba 26 Oct)",
    "L7 SARB report on Africa bank summary; PhD Lessons from South African bank failures; VBS Mutual Bank, The Great Bank Heist: the slides are enough (De Jager, Amathuba 11 Nov)",
  ],
  "background": [
    "A new framework for implementing Monetary Policy in South Africa (De Jager, Amathuba 11 Nov)",
    "Bank capital and RoE erroneous beliefs and financial instability (De Jager, Amathuba 11 Nov)",
  ],
  "format": "Final exam: 140 marks, 3 hours. Kruger 30 marks, De Jager 55, Huang 55.",
}
_NXT = set(B_SCOPE["notExaminedTopics"])
for _r in B_SCOPE["rules"]: _r["_re"] = re.compile(_r["pattern"], re.I); assert set(_r["topics"]) <= _bvalid
def _nx_reason(topics, text, full=None):
    full = text if full is None else full
    topics = set(topics)
    if topics and topics <= _NXT: return "Not examined (topic excluded)"
    for r in B_SCOPE["rules"]:
        if r["id"] == "market" and re.search(r"market value risk", text, re.I): continue   # interest rate risk (banking book), still examined
        if topics <= set(r["topics"]) and r["_re"].search(full if r["id"] == "ddm" else text): return r["reason"]   # DDM also matches in the answer: a question whose answer is the DDM is a DDM question
    return None
_nxc = {}
def _count(key): _nxc[key] = _nxc.get(key, 0) + 1
def _scope_filter(label, d, textof, fullof):
    before = {k: len(v) for k, v in d.items()}; out = {}
    for k, items in d.items():
        keep = []
        for it in items:
            why = _nx_reason([k], textof(it), fullof(it))
            if why: _count((label, k, why)); print("  excluded", label, k, "|", textof(it)[:110].replace("\n", " "), "|", why)
            else: keep.append(it)
        out[k] = keep
    print(label, "before/after by topic:", {k: (before[k], len(out[k])) for k in d if before[k] != len(out[k])})
    return out
_qb_before = {k: (sum(1 for x in v if not x.get("h")), sum(1 for x in v if x.get("h"))) for k, v in b_quiz.items()}
b_quiz = _scope_filter("quiz", b_quiz, lambda x: x["q"], lambda x: x["q"] + " " + x["a"])
print("quiz (quick, exam) before -> after:", {k: (_qb_before[k], (sum(1 for x in v if not x.get("h")), sum(1 for x in v if x.get("h")))) for k, v in b_quiz.items() if k in ("b-risk", "b-val", "b-mkt")})
if b_cards: b_cards = _scope_filter("card", b_cards, lambda x: x[0], lambda x: x[0] + " " + x[1])
_nxparts = {}
# Hand-checked scope decisions per part (scope_overrides.json): "nx" flags a part, "examined" clears a wrong regex flag.
_ovf = os.path.join(BANK_DIR, "scope_overrides.json")
_ov = json.load(open(_ovf, encoding="utf-8")) if os.path.exists(_ovf) else {}
_ovnx, _ovex = _ov.get("nx", {}), _ov.get("examined", {})
_ids = {p["id"]: {pt["id"] for q in p["questions"] for pt in q["parts"]} for p in b_papers}
for _k, _d in list(_ovnx.items()) + list(_ovex.items()):
    assert _k in _ids, f"scope_overrides: unknown paper {_k}"
    assert set(_d) <= _ids[_k], f"scope_overrides: unknown parts {set(_d) - _ids[_k]} in {_k}"
for _p in b_papers:
    for _bq in _p["questions"]:
        for _pt in _bq["parts"]:
            why = _nx_reason(_pt["topics"], _pt["required"])
            if _pt["id"] in _ovex.get(_p["id"], {}): why = None
            if _pt["id"] in _ovnx.get(_p["id"], {}): why = _ovnx[_p["id"]][_pt["id"]]
            if why: _pt["nx"] = why; _count(("part", _p["id"], why)); _nxparts.setdefault(_p["id"], []).append(_pt["id"])
print("papers, parts marked nx:", _nxparts)
print("excluded counts:", {" / ".join(k): v for k, v in sorted(_nxc.items())})
B_SCOPE["rules"] = [{k: v for k, v in r.items() if k != "_re"} for r in B_SCOPE["rules"]]
B_SCOPE_PUBLIC = {k: B_SCOPE[k] for k in ("notExaminedTopics", "rules", "focus", "notExamined", "background", "format")}
# Between the Lines notebooks (the student's annotated slides), linked by lecture from each section they cover.
# Links open the hosted app with the notebook id and page: #nb=<id>&page=<n>
BTL_APP = "https://ylp-games.github.io/Between-the-lines/"
B_BTL = [
  ("Bank Regulation & Failure Slides", "dmvy0wgdagt7z", [
    ("L1 Introduction", 2, 33, ["b-money", "b-reg"]),
    ("L2 Banks and money", 34, 62, ["b-money"]),
    ("L3 Monetary policy", 63, 90, ["b-money"]),
    ("L4 Introduction to bank regulation", 91, 123, ["b-reg"]),
    ("L5 Specifics of bank regulation", 124, 165, ["b-reg"]),
    ("L6 Introduction to bank failure", 166, 195, ["b-fail"]),
    ("L7 South African bank failures", 196, 228, ["b-fail"]),
    ("L8 SVB, Credit Suisse and conclusion", 229, 266, ["b-fail"]),
  ]),
]
b_books = [{"label": f"Between the Lines: {lec}, pages {p0} to {p1}", "url": f"{BTL_APP}#nb={nid}&page={p0}", "topics": tids}
           for _name, nid, lecs in B_BTL for lec, p0, p1, tids in lecs]
# The student's own notes (Word docs in Drive), split by heading; refresh with banking/extract_notes.py. Used for topic summaries.
_nf = os.path.join(BANK_DIR, "notes.json")
B_NOTES = json.load(open(_nf, encoding="utf-8")) if os.path.exists(_nf) else []
_ids = [p["id"] for p in papers + b_papers]
assert len(_ids) == len(set(_ids)), "paper ids must be unique across courses"

courses = [
  {"id": "tax2", "name": "Tax II", "code": "ACC3004W", "crumb": "ACC3004W past papers",
   "subject": "UCT ACC3004W Taxation II (South African tax) exam", "tablesLabel": "Tax tables", "minPerMark": 180 / 113,
   "formulaLabel": "2025 sheet (Nov 2025 & Jan 2026 exams)", "formulaSheet": next((p["tables"] for p in papers if p["id"] == "nov2025"), ""),
   "papers": papers, "topics": [{"id": k, "name": n} for k, n in TOPICS], "quiz": {k: [_q(x) for x in v] for k, v in BANK.items()}},
]
if b_papers:
    courses.append(
  {"id": "bank", "name": "Banking", "code": "FTX4087S", "crumb": "FTX4087S past tests, exams and workshops",
   "subject": "UCT FTX4087S Topics in Banking and Treasury Management test or exam", "tablesLabel": "Formula sheet", "minPerMark": 1.2,
   "papers": b_papers, "topics": [{"id": k, "name": n} for k, n in B_TOPICS], "quiz": b_quiz, "books": b_books, "scope": B_SCOPE_PUBLIC, "formulaLabel": "Formula sheet", "formulaSheet": B_FORMULAS, "formulaNotExamined": ["MARKET RISK AND PORTFOLIO THEORY"], "notes": B_NOTES, **({"cards": b_cards} if b_cards else {}), **({"rates": B_RATES} if B_RATES else {}),
   "topicGroups": [
     {"name": "Ryan Kruger", "note": "Intro to banking, financials, valuation and treasury · 30 exam marks", "topics": ["b-intro", "b-fin", "b-val", "b-treas", "b-mnc"]},
     {"name": "Philip De Jager", "note": "Money, regulation and bank failure · 55 exam marks", "topics": ["b-money", "b-reg", "b-fail"]},
     {"name": "Chun-Sung Huang", "note": "Risk management for banks · 55 exam marks", "topics": ["b-risk", "b-credit", "b-irr", "b-mkt"]}]})

data = json.dumps(courses, ensure_ascii=False).replace("</", "<\\/")
finish(tpl, data)

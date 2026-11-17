# Exam Desk

An interactive past-paper examiner for UCT courses (Taxation II, Banking & Treasury Management). Pick a paper, answer one required at a time, and get it marked against the memo. You see where you lost marks, the correct treatment and what to revise. You can then revise your answer and get it re-marked, or ask follow-up questions.

## Papers

| Paper | Memo |
|---|---|
| November 2025 Final | Official UCT suggested solution |
| January 2026 Supplementary | Official UCT suggested solution (question paper transcribed from scan) |
| Stacked (exam prep) | Studocu suggested solution |
| November 2024 Final | Official UCT suggested solution |
| January 2025 Supplementary | Official UCT suggested solution |
| November 2021 Final (ACC3004H) | Studocu suggested solution |
| Rockit Backpackers, Gino Todd, Uhuru, Stirology | **Generated with NotebookLM** from the Tax 2 notebook (not official, so check anything that looks off) |

## How marking works

- **On Vercel:** `index.html` calls `/api/mark` and `/api/chat`, which call the Gemini API with your key. The key is stored only in Vercel, never in the page.
- **Inside a Claude artifact:** the page uses Claude for marking instead.
- **Opened as a local file:** no automatic marking. You can self-mark against the memo.

## Deploy on Vercel

1. Import this repo in Vercel (Add New → Project → pick `tax2-examiner`). No build settings are needed.
2. In Project → Settings → Environment Variables, add:
   - `GEMINI_API_KEY`: a key from Google AI Studio (aistudio.google.com → Get API key).
   - `ACCESS_CODE` (recommended): any password. The site asks for it once per browser, so strangers can't use up your Gemini quota.
   - `GEMINI_MODEL` (optional): defaults to the newest Gemini Flash model your key can use. Use `gemini-2.5-pro` for stricter marking if your quota allows.
3. Redeploy. Open `/api/health` to check: `keySet` should be `true`.

The past papers are UCT/Studocu material. Keep this repo private, and don't share the Vercel URL publicly.

### Where the site deploys from

The code lives in two private repos:

- `layla310803/tax2-examiner` (remote `personal`): the full edition with the built-in Tax II and Banking courses. Vercel deploys from it. Push here: `git push personal HEAD:main`.
- `YLP-Games/ylp-exam-desk` (remote `origin`): the **content-free edition**. It has no built-in courses or course material; each user adds their own course and uploads their own notes, slides, past papers and memos, which stay in their browser. Don't push main to `origin`. After pushing to `personal`, run:

  ```bash
  bash tools/sync_ylp.sh
  ```

  It keeps a git worktree at `C:/Users/layo1/exam-desk-ylp` on a local branch `ylp`, copies every committed file from main except the course content (`source/t2`, `source/t3`, `source/banking`, `source/generated`, `source/jan26_q*.txt`, `source/quiz_bank.py`) and `index.html`, removes files main no longer has, builds `index.html` with `--edition ylp`, commits "Sync from tax2-examiner <sha>" and pushes `ylp` to `origin/main` (a normal fast-forward push).

## Editions

`python source/build.py index.html` builds the full edition. `python source/build.py index.html --edition ylp` builds with no built-in courses and doesn't read the content folders. The page gets an `EDITION` constant; code between `/*FULL{*/` and `/*}FULL*/` in `template.html` (the Tax II marking prompt, for example) is left out of the ylp edition.

## Your own source material

On a course's "Papers and sections" page (both editions), **Source material** takes PDF, Word (.docx), PowerPoint (.pptx) and text files, or pasted text, tagged as Notes, Slides, Past paper or Memo. The file readers (pdf.js, mammoth, JSZip) load from a CDN the first time they're needed.

- Notes and slides are split into sections (Word headings, one per slide, groups of PDF pages) and kept in the browser's IndexedDB. They become the course's notes, so **Summarise** on the Revisit page works from them.
- A past paper or memo is read into **Lay it out with AI** on a new paper.
- **Make flash cards and quiz from my material** has the AI write flash cards and quick-quiz questions for each section from the uploaded notes only (proposing sections from the headings if the course has none).
- The backup on the courses page includes the uploaded material.

## Section tests and weakest sections

Each section (Individuals, Employees' tax, Assessed losses, Estate duty, VAT, Capital allowances, Leases and the rest) has:

- **Quick quiz:** eight short type-in questions on the rules and how to apply them. They come from the question bank in `source/quiz_bank.py`, not from the past papers, and work without any AI. Numbers are marked automatically; you can overrule the marking on any question.
- **Longer questions, shortest first:** every past-paper required on that section, in order of marks.

The home page ranks your sections weakest first, from your quiz results and your best mark on each required.

The question bank uses the rates and thresholds for the 2025 and 2026 years of assessment. Update `source/quiz_bank.py` when they change, then rebuild.

## Rebuilding / adding papers

Paper content lives in `source/` (`build.py`, `template.html`, the extracted paper texts and the generated memos in `source/generated/`).

```bash
python source/build.py index.html
```

## Courses

The site opens on a course picker. Each course has its own papers, sections, quick quizzes and weakest-sections list; they share one page and one saved-progress store.

- **Tax II (ACC3004W)**: papers are defined in `source/build.py`, quiz questions in `source/quiz_bank.py`.
- **Banking (FTX4087S)**: everything is in `source/banking/`. One `b-*.json` file per paper (`kind` is `test`, `exam` or `workshop`), `formula_sheet.txt` (shown as the "Formula sheet" tab) and `quiz_bank.py`. To add a paper, drop in another JSON file with the same shape and rebuild.

Papers marked `"unofficial": true` have a memo that is partly from a student compilation or a suggested answer, not the lecturer. To add another course, add its entry to the `courses` list at the end of `source/build.py`; paper and section ids must be unique across courses.

# Tax II Examiner

An interactive past-paper examiner for UCT ACC3004W Taxation II. Pick a paper, answer one required at a time, and get it marked against the memo. You see where you lost marks, the correct treatment and what to revise. You can then revise your answer and get it re-marked, or ask follow-up questions.

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

## Rebuilding / adding papers

Paper content lives in `source/` (`build.py`, `template.html`, the extracted paper texts and the generated memos in `source/generated/`).

```bash
python source/build.py index.html
```

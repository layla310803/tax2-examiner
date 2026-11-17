#!/usr/bin/env bash
# Publish the content-free edition of Exam Desk to the YLP repo (remote "origin", YLP-Games/ylp-exam-desk).
#
# The YLP repo gets every tracked file from this repo's committed HEAD except the course content
# (source/t2, source/t3, source/banking, source/generated, the Tax II quiz bank and paper texts) and
# index.html, which is rebuilt there with --edition ylp (no built-in courses).
# It works in a git worktree on the local branch "ylp" (created from origin/main the first time),
# commits "Sync from tax2-examiner <sha>" and pushes ylp to origin/main (a normal fast-forward push).
#
# Run from anywhere inside this repo:   bash tools/sync_ylp.sh
set -euo pipefail

MAIN="$(git rev-parse --show-toplevel)"
WT="${YLP_WORKTREE:-C:/Users/layo1/exam-desk-ylp}"
EXCLUDE='^(source/(t2|t3|banking|generated)/|source/jan26_q[0-9]+\.txt$|source/quiz_bank\.py$|index\.html$)'

if [ -n "$(git -C "$MAIN" status --porcelain --untracked-files=no)" ]; then
  echo "Note: uncommitted changes in $MAIN are not synced; only the committed HEAD is." >&2
fi
SHA="$(git -C "$MAIN" rev-parse --short HEAD)"

git -C "$MAIN" fetch -q origin
if [ ! -e "$WT/.git" ]; then
  if git -C "$MAIN" show-ref --verify --quiet refs/heads/ylp; then
    git -C "$MAIN" worktree add "$WT" ylp
  else
    git -C "$MAIN" worktree add -b ylp "$WT" origin/main
  fi
fi
[ "$(git -C "$WT" rev-parse --abbrev-ref HEAD)" = "ylp" ] || { echo "$WT is not on branch ylp" >&2; exit 1; }
# take in anything pushed to the YLP repo by someone else (fast-forward only)
if ! git -C "$WT" merge-base --is-ancestor origin/main HEAD; then
  git -C "$WT" merge --ff-only origin/main || { echo "ylp and origin/main have diverged; sort that out by hand." >&2; exit 1; }
fi

KEEP="$(mktemp)"; trap 'rm -f "$KEEP"' EXIT
git -C "$MAIN" ls-files | grep -Ev "$EXCLUDE" > "$KEEP"

# copy the committed version of every kept file
while IFS= read -r f; do
  mkdir -p "$WT/$(dirname "$f")"
  git -C "$MAIN" cat-file blob "HEAD:$f" > "$WT/$f"
done < "$KEEP"

# delete files in the YLP tree that main no longer has, or that are course content
HAVE="$(mktemp)"; trap 'rm -f "$KEEP" "$HAVE"' EXIT
git -C "$WT" ls-files > "$HAVE"
while IFS= read -r f; do
  [ "$f" = "index.html" ] && continue
  grep -Fxq -- "$f" "$KEEP" || git -C "$WT" rm -q -- "$f"
done < "$HAVE"

# build the content-free page
(cd "$WT" && PYTHONIOENCODING=utf-8 python source/build.py index.html --edition ylp)
if grep -q -e "Trident" -e "Taxation II" -e "FTX4087" "$WT/index.html"; then
  echo "index.html still has course content in it; not pushing." >&2; exit 1
fi

git -C "$WT" add -A
if git -C "$WT" diff --cached --quiet; then
  echo "YLP is already up to date with $SHA."
else
  git -C "$WT" commit -q -m "Sync from tax2-examiner $SHA" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  echo "Committed $(git -C "$WT" rev-parse --short HEAD)."
fi
git -C "$WT" push origin ylp:main

# Deploy the YLP site (ylp-exam-desk.vercel.app) from the worktree with the Vercel CLI.
# The worktree is linked to the Vercel project ylp-exam-desk (.vercel/, git-ignored). Set SKIP_DEPLOY=1 to skip.
if [ -z "${SKIP_DEPLOY:-}" ] && [ -f "$WT/.vercel/project.json" ]; then
  (cd "$WT" && npx --yes vercel@latest deploy --prod --yes >/dev/null) && echo "Deployed to https://ylp-exam-desk.vercel.app" || { echo "Vercel deploy failed (run 'npx vercel login' if logged out)." >&2; exit 1; }
fi

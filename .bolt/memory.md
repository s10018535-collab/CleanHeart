# Project memory

## Product intent & audience

- CLEAN HEARTS: a report submission and officer portal application.
- Python/Streamlit version intended for local VS Code use, separate from the web version.
- Users: community members submitting reports; officers reviewing/managing them.
- Data is local-only (SQLite), does not sync with the web version.

## Brand personality & voice

- Clean, news-style presentation with a defining quote displayed.
- Trustworthy, civic, community-focused tone.

## Visual design & UX direction

- Card-based layout; each post/update is a single bordered card.
- Consistent theme applied via a shared Streamlit theme module.
- Shared display helpers reused across pages.
- Pages: news-style feed/updates view, report form, officer portal.
- Officer portal enforces department-only access to relevant reports.

## Decisions, constraints & rationale

- Stack: Python, Streamlit, SQLite, sentence-transformers (local).
- App lives in `python_app/` folder, separate from web app.
- Password stored as salted hash; plaintext never in code.
- Report routing uses sentence-transformers semantic model (~90 MB, first-run download).
- Reports matching no department route to General Services by default.
- Officer status updates validated against department.
- README provides setup/run instructions for VS Code.

## Open questions & assumptions

- App could not be launched or routing model tested in this environment; user must run once in VS Code to confirm functionality.
- First-run model download behavior and latency unverified here.
- No `.bolt/prompt` authoritative instructions present; memory seeded from this turn only.
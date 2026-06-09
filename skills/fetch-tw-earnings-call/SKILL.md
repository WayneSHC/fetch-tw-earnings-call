---
name: fetch-tw-earnings-call
description: Download Taiwan-listed companies' earnings-call (法說會) presentations and transcripts (Chinese + English) by ticker. Use when the user wants to fetch 法說會/法人說明會 簡報 or 逐字稿 for a TWSE/TPEx ticker (e.g. 2891 中信金, 2330 台積電), or mentions 公開資訊觀測站/MOPS being blocked for crawling. Bypasses MOPS anti-crawling by hitting authoritative IR sources directly.
---

# Fetch Taiwan Earnings-Call Materials

Downloads 法說會 (investor conference) **presentations** and **transcripts** for a given
ticker, Chinese and English, into `data/<ticker>_<name>/` with a `manifest.json`
that carries source provenance (引用接地, R4).

## Why not MOPS scraping
公開資訊觀測站 (MOPS) blocks aggressive crawling. This skill instead hits **authoritative
sources**: the company's IR site via a per-vendor adapter (richer — zh+en + transcript when
published) plus the MOPS 法人說明會一覽表 as a generic base that works for any ticker.
Results merge and dedupe by content md5.

## Usage
Run the downloader (`scripts/fetch_earnings_call.py`, relative to this skill's directory):
```bash
python3 "$SKILL_DIR/scripts/fetch_earnings_call.py" \
    --ticker 2891 --from 2021 --to 2026
# output: data/2891_中信金控/<files>.pdf + manifest.json
```
where `$SKILL_DIR` is this skill's own directory (when installed as a plugin it lives under
the plugin cache; in a repo it's `.claude/skills/fetch-tw-earnings-call`).

Options: `--ticker` (required), `--from`/`--to` (year range, default 2021..current),
`--out` (default `data/<ticker>_<name>`).

## Output naming
`<ticker>_<yyyymmdd><L><nn>_<period>_concall_<doctype>.pdf`
- `yyyymmdd` = 法說會 held date (from PDF first page; falls back to source listing date)
- `L` = `M` (中文) / `E` (英文); `nn` = per (ticker, date, lang) sequence from 01
- `period` = `YYYYQn`; `doctype` = `presentation` | `transcript`
- e.g. `2891_20260519M01_2026Q1_concall_presentation.pdf`

## Coverage
Companies in the registry (`ec_companies.py`) with a vendor adapter get zh+en + transcript.
Other tickers fall back to the MOPS base (presentation only). To add a company, extend the
registry and (if a new IR vendor) add an adapter under `scripts/`.

## Notes
- Most TW companies do **not** publish transcripts; the skill fetches them only when present
  and notes their absence in the run summary. It never fabricates a manifest entry.
- This skill only downloads + writes a manifest. Parsing/chunking/embedding is R4 ingestion.

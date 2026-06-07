# fetch-tw-earnings-call

A Claude Code **plugin** that downloads Taiwan-listed companies' earnings-call (法說會 / 法人說明會)
**presentations** and **transcripts** — Chinese *and* English — by stock id, into
`data/<stock_id>_<name>/` with a provenance `manifest.json`.

It bypasses 公開資訊觀測站 (MOPS) anti-crawling by hitting **authoritative sources** directly:
a per-vendor IR adapter (richer: zh + en + transcript when published) plus the MOPS
法人說明會一覽表 as a generic base that works for any stock id. Results are merged by
`(fiscal_period, lang, doc_type)` and md5-deduped across sources.

## Install

```text
/plugin marketplace add WayneSHC/fetch-tw-earnings-call
/plugin install fetch-tw-earnings-call@wayne-tw-tools
```

Then just ask Claude to "抓 2891 中信金的法說會簡報", or run the script directly:

```bash
python3 skills/fetch-tw-earnings-call/scripts/fetch_earnings_call.py \
    --stock-id 2891 --from 2021 --to 2026
```

Options: `--stock-id` (required), `--from`/`--to` (year range, default `2021..current`),
`--out` (default `data/<stock_id>_<name>`).

## Output naming

`<ticker>_<yyyymmdd><L><nnn>_<period>_concall_<doctype>.pdf`

- `yyyymmdd` — 法說會 held date (PDF first page; falls back to the source listing date)
- `L` — `M` (中文) / `E` (英文); `nnn` — per `(ticker, date, lang)` sequence from `001`
- `period` — `YYYYQn`; `doctype` — `presentation` | `transcript`
- e.g. `2891_20260519M001_2026Q1_concall_presentation.pdf`

Each `manifest.json` entry carries `stock_id, company, doc_type, fiscal_period, lang,
event_date, date_source, source_url, source_page, fetched_at, md5, bytes` for full
source traceability.

## Coverage & extension

Companies in `scripts/ec_companies.py` with a vendor adapter get zh + en (and transcript
when published). Any other stock id falls back to the MOPS base (presentation, zh + en).
To add a company: extend `ec_companies.py`, and — if it uses a new IR vendor — add an
adapter module exposing `supports(stock_id, registry)` and
`fetch(stock_id, years, http_get, registry) -> list[Doc]`.

## Notes

- Most Taiwan companies do **not** publish transcripts; the skill fetches them only when
  present and notes their absence in the run summary — it never fabricates a manifest entry.
- This plugin only downloads + writes a manifest. Parsing / chunking / embedding is out of scope.
- The skill scripts are **stdlib-only** (no third-party runtime deps) and inject `http_get`,
  so the unit tests run against saved HTML fixtures with zero network.

## Develop / test

```bash
uv venv && uv pip install -e ".[dev]"   # or: pip install pytest ruff
uv run pytest -q
uv run ruff check skills/fetch-tw-earnings-call/scripts/
```

## How it works (sources)

| Layer | Source | Gives |
|---|---|---|
| Vendor adapter | Company IR site (e.g. TodayIR for 中信金) | zh presentation, transcript when published |
| Centralized base | MOPS 法人說明會一覽表 (`ajax_t100sb02_1`, GET) | zh + en presentation for any stock id |

PDFs from different sources for the same call are collapsed to one per
`(fiscal_period, lang, doc_type)`, preferring the company's own IR copy.

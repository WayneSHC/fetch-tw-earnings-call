# fetch-tw-earnings-call

A Claude Code **plugin** that downloads Taiwan-listed companies' earnings-call (法說會 / 法人說明會)
**presentations** and **transcripts** — Chinese *and* English — by ticker, into
`data/<ticker>_<name>/` with a provenance `manifest.json`.

It fetches directly from **authoritative sources**: a per-vendor IR adapter (richer:
zh + en + transcript when published) plus the 公開資訊觀測站 (MOPS) 法人說明會一覽表
public listing endpoint as a generic base that works for any ticker. Results are merged by
`(fiscal_period, lang, doc_type)` and md5-deduped across sources.

> **License:** free for noncommercial use under
> [PolyForm Noncommercial 1.0.0](LICENSE); **commercial use requires a paid
> license** — see [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

## Install

```text
/plugin marketplace add WayneSHC/fetch-tw-earnings-call
/plugin install fetch-tw-earnings-call@wayne-tw-tools
```

Then just ask Claude to "抓 2891 中信金的法說會簡報", or run the script directly:

```bash
python3 skills/fetch-tw-earnings-call/scripts/fetch_earnings_call.py \
    --ticker 2891 --from 2021 --to 2026
```

Options: `--ticker` (required), `--from`/`--to` (year range, default `2021..current`),
`--out` (default `data/<ticker>_<name>`).

## Output naming

`<ticker>_<yyyymmdd><L><nn>_<period>_concall_<doctype>.pdf`

- `yyyymmdd` — 法說會 held date (PDF first page; falls back to the source listing date)
- `L` — `M` (中文) / `E` (英文); `nn` — per `(ticker, date, lang)` sequence from `01`
- `period` — `YYYYQn`; `doctype` — `presentation` | `transcript`
- e.g. `2891_20260519M01_2026Q1_concall_presentation.pdf`

Each `manifest.json` entry carries `ticker, company, doc_type, fiscal_period, lang,
event_date, date_source, source_url, source_page, fetched_at, md5, bytes` for full
source traceability.

## Coverage & extension

Companies in `scripts/ec_companies.py` with a vendor adapter get zh + en (and transcript
when published). Any other ticker falls back to the MOPS base (presentation, zh + en) —
no registry entry needed; the company name is taken from the MOPS listing.
To add a company: extend `ec_companies.py`, and — if it uses a new IR vendor — add an
adapter module exposing `supports(ticker, registry)` and
`fetch(ticker, years, http_get, registry) -> list[Doc]`.

## Notes

- Most Taiwan companies do **not** publish transcripts; the skill fetches them only when
  present and notes their absence in the run summary — it never fabricates a manifest entry.
- When the MOPS subject line doesn't state a quarter (e.g. 台塑化's
  「說明近期營運概況」), the fiscal period is inferred from the filename date as the most
  recently completed quarter (a May meeting reports Q1, a March meeting last year's Q4).
  A quarter stated explicitly in any subject for the same file always wins.
- A dead link doesn't abort the run: failed downloads are warned on stderr and skipped;
  everything else is still written.
- This plugin only downloads + writes a manifest. Parsing / chunking / embedding is out of scope.
- The plugin accesses public endpoints and public IR pages only. Downloaded documents
  remain the property of their issuers; MOPS information is governed by TWSE's
  information-usage regulations. Comply with each source's terms, keep request rates
  reasonable, and see [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) before any
  commercial use or redistribution of fetched data.
- The skill scripts are **stdlib-only** (no third-party runtime deps) and inject `http_get`,
  so the unit tests run against saved HTML fixtures with zero network.

## Develop / test

```bash
uv venv && uv pip install -e ".[dev]"   # or: pip install pytest ruff
uv run pytest -q
uv run ruff check skills/fetch-tw-earnings-call/scripts/
```

### Canonical source & sync

The skill code (scripts + tests + fixtures) is mirrored from the **polaris-desk** repo
(`.claude/skills/fetch-tw-earnings-call`), which is the canonical copy; its
`scripts/sync-plugin.sh` pushes changes here and verifies the two stay byte-identical.
If you fix something in *this* repo first, back-sync it to polaris-desk and re-run that
script before pushing either repo. `SKILL.md`, `README.md`, and the plugin packaging
files are maintained per-repo and never synced.

## How it works (sources)

| Layer | Source | Gives |
|---|---|---|
| Vendor adapter | Company IR site (e.g. TodayIR for 中信金) | zh presentation, transcript when published |
| Centralized base | MOPS 法人說明會一覽表 (`ajax_t100sb02_1`, GET) | zh + en presentation for any ticker |

PDFs from different sources for the same call are collapsed to one per
`(fiscal_period, lang, doc_type)`, preferring the company's own IR copy.

## License

- **Code** — [PolyForm Noncommercial 1.0.0](LICENSE): free for personal, academic,
  nonprofit, and government use. **Any commercial use** (including internal use inside a
  for-profit organization) **requires a separate paid license** — see
  [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) or contact <waynehuichi@gmail.com>.
- **Data** — not covered by any license here. Fetched PDFs belong to their issuers, and
  MOPS information is governed by TWSE's information-usage regulations
  (臺灣證券交易所資訊使用管理辦法). You are responsible for complying with each source's
  terms before storing, reusing, or redistributing fetched data; commercial redistribution
  of the data may require authorization from TWSE and/or the issuing companies.

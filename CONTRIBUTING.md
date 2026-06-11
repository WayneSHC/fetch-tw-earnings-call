# Contributing / 貢獻指南

感謝你的興趣！提交貢獻前請先閱讀以下條款。
Thanks for your interest! Please read the terms below before submitting.

## 貢獻授權條款 / Contribution license grant

本專案採「非商業免費（[PolyForm Noncommercial 1.0.0](LICENSE)）+
付費商業授權（[COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md)）」雙軌模式。
為了讓維護者能持續以此模式授權整個專案：

**當你提交任何貢獻（pull request、patch、issue 中的程式碼等），即表示你：**

1. 確認你擁有該貢獻的著作權，或已取得合法授權得為本條款之授予；
2. 授予維護者（Wayne SHC）一項**永久、全球、非專屬、不可撤銷、免權利金**
   之授權，得使用、重製、修改、散布、再授權（sublicense）你的貢獻，
   並得以**任何條款**（包括商業授權條款）對外授權含你貢獻之版本；
3. 你的貢獻依專案之 LICENSE 對你與其他使用者生效。

**By submitting any contribution (pull request, patch, code in an issue,
etc.), you confirm that you own the rights to it, and you grant the
maintainer (Wayne SHC) a perpetual, worldwide, non-exclusive, irrevocable,
royalty-free license to use, reproduce, modify, distribute, sublicense, and
relicense your contribution under any terms, including commercial license
terms.** Your contribution is available to you and other users under the
project LICENSE.

如果你無法同意上述條款，請改以 issue 描述問題，由維護者自行實作。
If you cannot agree to these terms, please describe the change in an issue
instead so the maintainer can implement it independently.

## 開發流程 / Development

```bash
uv venv && uv pip install -e ".[dev]"
uv run pytest -q
uv run ruff check skills/fetch-tw-earnings-call/scripts/
```

- Script 程式碼維持 **stdlib-only**（不得引入第三方執行期相依）。
- 本 repo 的 skill 程式碼（scripts + tests + fixtures）與 polaris-desk repo
  互為鏡像（詳見 README「Canonical source & sync」）；修改後請確認兩邊同步。
- 新增公司／IR vendor 的方式見 README「Coverage & extension」。

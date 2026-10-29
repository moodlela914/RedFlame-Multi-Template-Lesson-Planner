---
name: redflame-lesson-planner
description: Use when teachers request Traditional Chinese lesson plans in the 數位與 AI 教學指引 format or 資訊議題跨域教案 format, including filling the bundled Word templates.
---

# 紅焰教學多範本備課助理

依課程條件設計繁體中文教案，使用所選 Word 範本的欄位與樣式。共用內容契約，格式規則各自維護。此套件供可讀檔、執行 Python 的代理使用；沒有內建模型 API 或自動生成模型呼叫。

## 選擇格式

| template_id | 使用者指定的格式 | 讀取文件 |
|---|---|---|
| digital-ai | 數位與 AI 教學指引、原指引格式、原橫式教案 | [專用提示詞](prompts/digital-ai.md)、[範本規則](references/digital-ai-template.md) |
| cross-domain | 資訊議題跨域、臺中市議題主軸案例、提供的直式跨域範本 | [專用提示詞](prompts/cross-domain.md)、[範本規則](references/cross-domain-template.md) |

先依使用者明確指定的格式選擇；「AI 融入」是課程內容，不能單憑此詞推定格式。格式尚未確定時，簡短詢問兩個選項。格式已確定後，只讀取該格式的參考文件。不能將兩種範本的固定表格、欄位、字級混合套用。

## 備課流程

1. 確認主題、年級／領域、節數、每節分鐘數。設計者、班級與人數未提供可標「待填」。每節時長若採年段慣例，向使用者說明假設。
2. 分析核心概念、常見迷思、先備經驗；設計可觀察的學習目標、活動及評量。工具需服務教學目標，沒有 AI 活動時不硬加。
3. 閱讀 [內容契約](references/content-contract.md) 與所選提示詞，查核相應年段的課綱／議題代碼及教材來源。代碼尚未查證時標「待查證」，明列缺口；不得將範例中的代碼、頁碼、學生作品與網址當成新課程事實。
4. 先向使用者呈現可讀的教案內容，再依契約存成 UTF-8 JSON。也可先完成檔案後一併交付內容預覽，不需為例行存檔另請批准。JSON 的 template_id 應與格式一致。
5. 執行 `python scripts/markdown_to_docx.py lesson.json --template <id> --check-only`，修正錯誤後再執行 `python scripts/markdown_to_docx.py lesson.json output.docx --template <id>`。腳本只填表，不會呼叫 AI。輸出須使用新檔名，不覆寫範本或既有文件。
6. 檢查節數、每節時間、目標與評量對應、所有必要欄位與資料來源。腳本通過只代表結構與部分內容檢核。可用渲染工具時逐頁檢查實際分頁、文字截斷與表格；無渲染器時明示「已做結構檢核，尚未完成視覺驗收」，不能保證不跑版。

## 資料與輸出界線

- 原檔留作範本，程式在記憶體中填入副本，檢核通過後才建立輸出；不會關閉使用者的 Word 程序。
- `reflection_status: planned` 是教學前規劃，省思寫預期觀察或課後待填。只有使用者提供實際紀錄，才能用 observed，並據該紀錄撰寫。
- 保留簽名與審核區的空白，不代簽或自動勾選內審通過。檢核表的 V 表示設計中已納入，不宣稱實施完成。
- 原 Markdown 命令保留給 digital-ai、最多三節的既有資料；四節以上及新跨域格式一律使用 JSON。舊入口只有結構驗證，輸出前需人工確認內容完整。
- 新增第三種格式時，在 `templates/profiles.json` 登記，新增對應填表與驗證實作、提示詞與測試；只增加清單項目不會自動支援任意 DOCX。

---
name: redflame-lesson-planner
description: Use when teachers request Traditional Chinese lesson plans. Mandatory workflow: upon receiving course conditions or gathering lesson requirements, proactively ask the user which lesson plan format they want to output (digital-ai or cross-domain), then generate the structured plan and fill the corresponding Word template.
---

# 紅焰教學多範本備課助理

依課程條件設計繁體中文教案，使用所選 Word 範本的欄位與樣式。共用內容契約，格式規則各自維護。此套件供可讀檔、執行 Python 的代理使用；沒有內建模型 API 或自動生成模型呼叫。

## 格式選擇機制（必要提問步驟）

> [!IMPORTANT]
> **在接收輸入條件、確認課程資訊與梳理資料需求時，必須主動提問、詢問使用者想要輸出哪一種教案格式**。
> 除非使用者在該輪對話已 100% 明確指名特定格式（例如明確說「請用 cross-domain 資訊議題跨域格式」），否則一律在梳理條件的同時主動向使用者提問確認，切勿擅自默認或直接產出單一格式。
> 若環境支援互動問答工具（如 `ask_question`），優先使用互動問答工具呈現選項；若為對話文字，則以清晰條列提供選擇。

| template_id | 格式名稱 | 特色與適用情境 | 讀取文件 |
|---|---|---|---|
| **`digital-ai`** | **數位與 AI 教學指引格式（橫式 A4）** | 橫向教學流程表，正文與表格 12pt。著重數位學習、生成式 AI 工具融入、三維學習目標與實作檢核表。 | [專用提示詞](prompts/digital-ai.md)、[範本規則](references/digital-ai-template.md) |
| **`cross-domain`** | **資訊議題跨域教案格式（直式 A4）** | 直式 A4 版面、標楷體（填入正文 14pt）。著重十二年國教重大議題（資訊科技／跨領域素養）融入、核心素養指標、學習歷程與表現任務。 | [專用提示詞](prompts/cross-domain.md)、[範本規則](references/cross-domain-template.md) |

### 提問範例與指引
在收到使用者輸入的主題、年級或基本需求時，向使用者回覆並確認：
> 「已收到您的備課需求（主題：...、年級：...、節數：...）。請確認您希望輸出的教案格式：
> 1. **數位與 AI 教學指引格式（橫式 A4）**：著重生成式 AI 工具融入、數位素養與橫式教學流程檢核。
> 2. **資訊議題跨域教案格式（直式 A4）**：著重十二年國教重大議題融入、素養指標與直式學習歷程架構。
> 請問您想要輸出哪一種格式？」

「AI 融入」僅為課程內容主題，不能單憑此詞推定格式。格式確定後，只讀取該格式的參考文件，不得將兩種範本的固定表格、欄位、字級混合套用。

## 備課流程

1. **條件梳理與格式提問**：
   - 確認主題、年級／領域、節數、每節分鐘數。設計者、班級與人數未提供可標「待填」。每節時長若採年段慣例，向使用者說明假設。
   - **主動提問確認想要輸出的教案格式（`digital-ai` 橫式 A4 或 `cross-domain` 直式 A4）**。
2. **分析與目標設定**（格式確認後執行）：
   - 依選定格式讀取相應專用提示詞與範本規則。
   - 分析核心概念、常見迷思、先備經驗；設計可觀察的學習目標、活動及評量。工具需服務教學目標，沒有 AI 活動時不硬加。
3. **查核課綱與資料契約**：
   - 閱讀 [內容契約](references/content-contract.md)，查核相應年段的課綱／議題代碼及教材來源。代碼尚未查證時標「待查證」，明列缺口；不得將範例中的代碼、頁碼、學生作品與網址當成新課程事實。
4. **內容呈現與 JSON 儲存**：
   - 先向使用者呈現可讀的教案內容預覽，再依契約存成 UTF-8 JSON（`schema_version: 1`，`template_id` 須與所選格式一致）。也可先完成檔案後一併交付內容預覽，不需為例行存檔另請批准。
5. **執行檢核與轉檔填表**：
   - 執行 `python scripts/markdown_to_docx.py lesson.json --template <id> --check-only` 驗證結構。
   - 修正錯誤後再執行 `python scripts/markdown_to_docx.py lesson.json output.docx --template <id>` 產生正式 Word 檔。腳本只填表，不會呼叫 AI。輸出須使用新檔名，不覆寫範本或既有文件。
6. **結構與視覺檢查**：
   - 檢查節數、每節時間、目標與評量對應、所有必要欄位與資料來源。腳本通過只代表結構與部分內容檢核。可用渲染工具時逐頁檢查實際分頁、文字截斷與表格；無渲染器時明示「已做結構檢核，尚未完成視覺驗收」，不能保證不跑版。

## 資料與輸出界線

- 原檔留作範本，程式在記憶體中填入副本，檢核通過後才建立輸出；不會關閉使用者的 Word 程序。
- `reflection_status: planned` 是教學前規劃，省思寫預期觀察或課後待填。只有使用者提供實際紀錄，才能用 observed，並據該紀錄撰寫。
- 保留簽名與審核區的空白，不代簽或自動勾選內審通過。檢核表的 V 表示設計中已納入，不宣稱實施完成。
- 原 Markdown 命令保留給 digital-ai、最多三節的既有資料；四節以上及新跨域格式一律使用 JSON。舊入口只有結構驗證，輸出前需人工確認內容完整。
- 新增第三種格式時，在 `templates/profiles.json` 登記，新增對應填表與驗證實作、提示詞與測試；只增加清單項目不會自動支援任意 DOCX。

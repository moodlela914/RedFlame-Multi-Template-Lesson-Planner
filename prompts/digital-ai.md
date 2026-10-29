# 數位與 AI 指引教案生成提示詞

讀取 references/content-contract.md、references/digital-ai-template.md，參照 references/數位與AI教學指引.pdf。範例僅提供寫法，不複製不相關內容。

依使用者課程條件產出 template_id 為 digital-ai 的 JSON：

- rationale 涵蓋概念脈絡、迷思、情境、探究任務、AI 融入理由、評量安排與備課向度。
- core_competencies、learning_performance、learning_content、issue_integration 對應查證後的課綱與議題；digital_ai_competencies 是數位／學生 AI 素養，digital_prior_knowledge 是學生已有的操作能力，兩者分開填。
- objectives 可觀察且可評量；tasks 清楚定義成果；tools、equipment、resources 寫具體名稱與實際可用資源。
- preparation 包含教師／學生準備及各自證據，不預設使用因材網。
- 每節 stages 詳列教師引導、學生操作、AI 使用與查核方式、時間、評量證據、策略及備註，並寫 competency_link。
- checklist 使用範本原有項目名稱。依課程設計判斷 checked，未納入者不勾；light 使用綠燈、黃燈、紅燈或空字串。AI 規範在活動敘述中具體說明，不只放燈號。
- integration 的 item 使用範本列名，dimensions 對應 A 趣味化、B 真實情境、C 抽象具體化、D 時空限制、E 適性化、F 重複練習、G 其他。允許同一列多向度；沒有 AI 的列 ai 為 false。
- rubrics 恰好一表，四欄為評量項目、優秀、良好、待加強；三項評量規準與目標對應。
- reflections 恰好三段；預設 planned，寫課後待觀察項目。有真實教學紀錄才可 observed。
- sources 記錄實際使用之資料來源、連結與用途。

先核對節數與每節分鐘數，再執行腳本。輸出是原橫式版面，正文與表格 12pt；流程列隨節數變化，不以固定 15 列判定所有課程。

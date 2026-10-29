# 教案 JSON 內容契約

UTF-8 JSON，根節點為物件。兩個可執行範例見 examples/multi_template/。使用 Python 3.10 以上；依 requirements.txt 安裝 python-docx 與 lxml。

## 共用必要欄位

| key | 型別及規則 |
|---|---|
| schema_version | 整數 1 |
| template_id | digital-ai 或 cross-domain；須與 CLI 選項一致 |
| metadata | topic 主題、subject 科目、grade 年級、designer 設計者，皆非空字串；period_count 節數、minutes_per_period 每節分鐘數，皆正整數 |
| fields | 依格式選用下列語意欄位，值均為非空字串；可用換行表達清單 |
| periods | 每節一物件，陣列長度等於 period_count |
| rubrics | 至少一個評量規準物件 |
| reflection_status | planned 教學前規劃，或 observed 依實際紀錄 |
| reflections | 非空字串陣列；digital-ai 恰好三段 |

metadata 的 course_type 與 implementation 在 cross-domain 必填：分別為議題融入式課程／議題主題式課程、領域學習課程／彈性學習課程。digital-ai 可加 class_name、student_count，未提供填待填。

每個 period：title、competency_link 為非空字串；stages 為非空陣列。每個 stage：name、activity、assessment、strategy 為非空字串；minutes 為正整數；notes 為字串，可省略。每節 minutes 總和必須等於 minutes_per_period。

每個 rubric：title 非空字串，headers 非空字串陣列，rows 為字串的二維陣列，各列長度等於 headers。digital-ai 恰一表、四欄、三個資料列；cross-domain 依任務需求設計，不限制為三個等級或三個面向。

## fields 名稱

兩種都要：core_competencies 總綱核心素養、digital_prior_knowledge 學生數位先備經驗、learning_performance 領域學習表現、learning_content 領域學習內容、objectives 學習目標、resources 教學資源。

digital-ai 額外必填：rationale 設計理念、digital_ai_competencies 數位／學生 AI 素養、issue_integration 議題融入、connections 跨領域連結、tasks 學習任務、tools 工具／平台、equipment 設備。

cross-domain 額外必填：motivation 設計動機、learning_journey 預期學習歷程、competency_explanation 呼應核心素養說明、theme_structure 主題架構、subject_prior_knowledge 學科先備經驗、competency_dimensions 總綱面向、domain_competencies 領域核心素養、issue_competencies 議題核心素養、issue_themes 議題學習主題、issue_content 議題實質內涵、assessment_strategy 評量策略。

注意 core_competencies 與 domain_competencies 分屬總綱與領域欄；digital_prior_knowledge 與 digital_ai_competencies 分屬已有能力與本課培養素養，不能混填。未知課綱資料標待查證，不捏造代碼。查證與語意正確性由備課代理負責，腳本僅檢查資料結構。

## digital-ai 專用資料

preparation 物件含 teacher、student、teacher_evidence、student_evidence，皆非空字串。

checklist 陣列，每筆含 item 範本項目名稱、checked 布林值、light 字串（綠燈／黃燈／紅燈／空字串）。至少一筆，不得重複，不存在的項目拒絕輸出；其餘項目不勾選。

integration 陣列，每筆含 item 範本列名、ai 布林值、dimensions 物件。dimensions 的 key 為 A 至 G，value 是該向度融入說明。允許多向度。完整列名見 digital-ai-template.md。

## 共用選填資料

appendices 陣列，每筆含 title、text 非空字串。跨域格式附於附錄；原指引格式附於省思後。

sources 陣列，每筆含 title、used_for 非空字串及 url 字串。無網址可填空字串，例如使用者提供之教材。不得填虛構網址。可用性、權限、內容與課綱正確性由代理查核，腳本不連網。

## 命令

```bash
python scripts/markdown_to_docx.py --list-templates
python scripts/markdown_to_docx.py lesson.json --template cross-domain --check-only
python scripts/markdown_to_docx.py lesson.json output.docx --template cross-domain
```

省略 --template 時依 JSON 的 template_id；兩者矛盾時拒絕。--check-only 會執行資料、原範本結構與記憶體輸出檢核，不建立 DOCX。輸出已存在時拒絕，請用新檔名。格式不符或必要欄位缺少時不輸出。額外 fields 不會自動建立新欄位，請依所選 profile 準備資料。

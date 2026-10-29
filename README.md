# 紅焰教學多範本備課助理

在原 RedFlame-AI-Lesson-Planner 基礎上擴充，保留原數位與 AI 教學指引格式，新增使用者提供的資訊議題跨域格式。兩種格式使用各自的提示詞、Word 欄位映射與驗證規則。

| 格式代碼 | 範本 | 版面 |
|---|---|---|
| digital-ai | 指引教案格式.docx | 原橫式版面，正文與表格 12pt |
| cross-domain | 資訊議題跨域教案(空白).docx | 原直式 A4、標楷體，填入正文 14pt，保留標題樣式 |

## 使用方式

從 GitHub Releases 下載完整 Skill ZIP，解壓縮後將整個技能資料夾放入代理支援的技能目錄，例如 Codex 的 `~/.codex/skills/redflame-lesson-planner/`，保留 scripts、templates、prompts、references、examples 的相對位置。此工作區版本不會自動安裝或修改全域設定。

有 Python 3.10 以上的環境可安裝：

```bash
python -m pip install -r requirements.txt
```

在 Codex 已提供工作區執行環境時，優先使用其套件與 Python。載入 SKILL.md，直接提出主題、年級科目、節數、每節時間與格式，例如：

> 用資訊議題跨域格式，幫我設計五年級自然與資訊的資料查證課程，兩節、每節40分鐘，輸出 Word。

代理負責備課及查核來源，再將內容存成 JSON。腳本負責填表，不會自行呼叫模型或收取模型 API 費用。AntiGravity 可將 system_prompt.md 與 agent_config.yaml 作為設定參考；模型呼叫、變數注入與知識庫掛載仍由宿主提供，需由宿主確認支援方式。

## 直接操作程式

```bash
python scripts/markdown_to_docx.py --list-templates
python scripts/markdown_to_docx.py examples/multi_template/cross-domain.json --check-only
python scripts/markdown_to_docx.py examples/multi_template/cross-domain.json output/cross-domain.docx --template cross-domain
python scripts/markdown_to_docx.py examples/multi_template/digital-ai.json output/digital-ai.docx --template digital-ai
```

範例 JSON 示範資料格式與備課內容，不是經查核的正式課綱教案。正式使用前請依課程查證課綱代碼及教材，再逐頁檢視排版。檔案已存在時請換新檔名。

既有 Markdown 指令保留：

```bash
python scripts/markdown_to_docx.py examples/Grade_7_Geography/如何表現地形_數位與AI融入教案.md output/geography.docx
```

舊 Markdown 僅支援 digital-ai、最多三節，只有結構驗證；四節以上與新跨域格式使用 JSON。契約詳見 references/content-contract.md。JSON 支援任意正整數節數，實際頁數依內容而定；七節流程已納入測試。

## 檢核與維護

`templates/profiles.json` 是兩種格式清單及必填欄位來源。填表實作在 scripts/lesson_templates.py；prompts 下兩套提示詞與 references 下兩套規則獨立維護。增加第三種範本需要新增程式映射與測試，不能只替換 DOCX。

程式保留原範本、不關閉 Word、不覆寫既有檔案。JSON 路徑只更新 Word 套件中的 document.xml，其他套件成員內容不變。驗證必要欄位、時間、完整節數、表格結構與方向後才建立輸出。跨域主表列數為 18 + 節數；指引流程表列數為 12 + 節數，不再硬鎖三節。

結構驗證不等於課綱查核或視覺驗收。正式交付 Word 前，需檢查內容與逐頁排版；缺乏渲染器時明示尚未視覺驗收。教學省思預設課後待填，不代寫已實施成效；不代簽或勾選內審通過。

```bash
python -m unittest discover -s tests -v
```

## 授權 (License)

| 內容 | 授權 | 檔案 |
|---|---|---|
| 本 repo 的程式碼（`scripts/`、`tests/`、`*.py`、腳本與設定檔） | **MIT** | [LICENSE](LICENSE) |
| 本 repo 的文件與素材（`*.md`、技能提示詞、範本文檔、教學素材） | **CC BY-NC 4.0**（姓名標示、非商業性） | [LICENSE-docs.md](LICENSE-docs.md) |

fork 或轉載時請保留此授權規範。教師運用本 repo 產出之個人原創教學教案成果，可自由應用於學校課堂與教學公開分享。

原始來源：[moodlela914/RedFlame-AI-Lesson-Planner](https://github.com/moodlela914/RedFlame-AI-Lesson-Planner)。原作者署名與既有教材保留。擴充版儲存庫：[RedFlame-Multi-Template-Lesson-Planner](https://github.com/moodlela914/RedFlame-Multi-Template-Lesson-Planner)。

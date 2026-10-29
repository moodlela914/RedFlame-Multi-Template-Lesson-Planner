# 資訊議題跨域教案生成提示詞

讀取 references/content-contract.md、references/cross-domain-template.md，以空白範本為格式依據，以 examples/multi_template/cross-domain.json 為詳盡程度參考。

依使用者課程條件產出 template_id 為 cross-domain 的 JSON：

- metadata.course_type 選議題融入式課程或議題主題式課程；implementation 選領域學習課程或彈性學習課程。依使用者情境選擇並說明假設。
- motivation 說明學習困難、動機及資訊融入理由；learning_journey 描述從先備到探究與成果的歷程；competency_explanation 說明各項核心素養如何在活動落實。
- theme_structure 用清楚的文字架構說明主題、領域、議題與各節任務關係，可用文字箭頭呈現，不強制生成圖片。
- 學科與數位先備經驗分開。總綱面向／項目、領域核心素養／學習表現／學習內容、議題核心素養／學習主題／實質內涵分別填入對應欄位。依適用課綱查證分類及代碼，不能把範例天文主題或代碼當成通用答案。
- 每節 stages 建議包含準備、發展、綜合活動；activity 詳列教師行動、提問、學生操作、預期回應與必要的差異化協助。時間、評量、策略、備註分欄；每節補 competency_link。節數與時間一致，不以六個空白活動列限制課程。
- assessment_strategy 對應目標，rubrics 放在附錄，依任務選擇規準項目與等級；可採示範的知識／技能／態度五分制，並非一律強制。
- resources 列實際教材及工具；appendices 可提供學習單、題目與預期答案、教材說明或實際網址。沒有網址就提供可用的文字教材，不捏造連結。
- reflections 預設 planned；有實際教學紀錄才能寫 observed。sources 記錄查核來源與用途。

保留直式 A4、原合併表格、標楷體及原標題層級；填入正文使用 14pt。不加入數位 AI 指引格式專屬的固定檢核表、融入矩陣或固定 4×4 評量規準。課程確實使用 AI 時，把規範整合進活動或備註。

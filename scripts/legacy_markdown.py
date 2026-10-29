import os
import sys
import re
import docx
from docx.shared import Pt

# Reconfigure stdout to use UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def parse_markdown(md_path):
    """
    Parses markdown file, extracts tables, headings, and paragraphs.
    """
    if not os.path.exists(md_path):
        print(f"Error: Markdown file '{md_path}' does not exist.")
        return [], {}

    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    tables = []
    current_table = []

    sections = {}
    current_section = None
    section_content = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            # Heading found, save previous section content
            if current_section:
                sections[current_section] = section_content
            current_section = stripped
            section_content = []
            continue

        if stripped.startswith('|'):
            # Table row found
            parts = [p.strip() for p in line.split('|')[1:-1]]
            current_table.append(parts)
        else:
            # End of table check
            if current_table:
                clean_table = []
                for row in current_table:
                    # Ignore markdown table divider lines like |---|---|
                    if all(c == '' or set(c) <= {'-', ':', ' '} for c in row):
                        continue
                    clean_table.append(row)
                if clean_table:
                    tables.append(clean_table)
                current_table = []
            if stripped:
                section_content.append(stripped)

    # Append trailing table or section if exists
    if current_table:
        clean_table = []
        for row in current_table:
            if all(c == '' or set(c) <= {'-', ':', ' '} for c in row):
                continue
            clean_table.append(row)
        if clean_table:
            tables.append(clean_table)

    if current_section:
        sections[current_section] = section_content

    return tables, sections

def clean_key(text):
    return re.sub(r'[*_#`\s]', '', text).lower()

def extract_prep_from_bullets(sections):
    """
    Tries to extract teacher/student preparation from bullet lists under 課前準備 heading.
    """
    teacher_prep = []
    student_prep = []
    current_target = None # "teacher" or "student"

    # Find the section that contains "課前準備" in its heading
    prep_heading = None
    for heading in sections.keys():
        if "課前準備" in heading:
            prep_heading = heading
            break

    if prep_heading:
        for line in sections[prep_heading]:
            clean_line = line.replace('*', '').replace('-', '').strip()
            if "教師" in clean_line:
                current_target = "teacher"
                continue
            elif "學生" in clean_line:
                current_target = "student"
                continue

            # Match list items
            if current_target and (re.match(r'^\d+\.', clean_line) or clean_line.startswith('1.') or clean_line.startswith('2.')):
                if current_target == "teacher":
                    teacher_prep.append(clean_line)
                elif current_target == "student":
                    student_prep.append(clean_line)

    teacher_text = "\n".join(teacher_prep) if teacher_prep else ""
    student_text = "\n".join(student_prep) if student_prep else ""
    return teacher_text, student_text

def run_conversion(md_path, output_docx_path):
    print(f"\n--- Starting conversion for '{md_path}' -> '{output_docx_path}' ---")

    # Parse markdown
    tables, sections = parse_markdown(md_path)
    if not tables:
        print("Error: No tables parsed from markdown!")
        return False

    # Load blank template
    # Locate templates relative to the workspace root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    template_path = os.path.join(workspace_root, "templates", "指引教案格式.docx")
    if not os.path.exists(template_path):
        print(f"Error: Template '{template_path}' not found!")
        return False

    doc = docx.Document(template_path)

    # 1. Classify tables by searching headers/sizes
    table_0_md = None # Basic info
    checklist_md = None
    matrix_md = None
    rubrics_md = None
    activity_tables_md = []

    for t in tables:
        if not t or len(t) == 0:
            continue
        c0 = clean_key(t[0][0])

        # Table 0: Basic Info
        if "領域/科目" in c0 or "subject" in c0:
            table_0_md = t
        # Checklist Table
        elif "檢核項目" in c0:
            checklist_md = t
        # Matrix Table
        elif "科技融入" in c0 or "數位科技融入" in c0:
            matrix_md = t
        # Rubrics Table
        elif "評量項目" in c0:
            rubrics_md = t
        # Flow activities (Teacher/Student Prep or Periods)
        elif "教學重點" in c0 or "學習活動設計" in c0:
            activity_tables_md.append(t)

    # Helper function to find key-value from any parsed table
    def find_value_by_key(key_sub):
        key_sub = clean_key(key_sub)
        for t in tables:
            for row in t:
                for c_idx, cell in enumerate(row):
                    if key_sub in clean_key(cell):
                        if c_idx + 1 < len(row):
                            return row[c_idx + 1]
        return ""

    # 2. Populate Table 0 (基本資料與設計依據)
    print("Populating Table 0...")
    docx_t0 = doc.tables[0]

    # Subject
    docx_t0.cell(0, 2).text = find_value_by_key("領域/科目") or find_value_by_key("Subject")
    # Designer
    docx_t0.cell(0, 7).text = find_value_by_key("設計者") or find_value_by_key("Designer")

    # Extract Class profile details (Grade, Class, Students)
    class_profile = find_value_by_key("班級") or find_value_by_key("Classprofile")
    grade = ""
    cl = ""
    num = ""
    if class_profile:
        parts_cl = [p.strip() for p in re.split(r'[，,]', class_profile)]
        if len(parts_cl) >= 1:
            grade = parts_cl[0]
        if len(parts_cl) >= 2:
            cl = parts_cl[1]
        else:
            cl = class_profile
        nums = re.findall(r'\d+(?:-\d+)?', cl)
        num = nums[0] if nums else "待確認"

    docx_t0.cell(2, 2).text = grade or "待確認"
    docx_t0.cell(2, 3).text = cl or "待確認"
    docx_t0.cell(2, 4).text = num or "待確認"

    # Duration
    docx_t0.cell(2, 7).text = find_value_by_key("總節數") or find_value_by_key("Time")
    # Unit Name
    unit_name = find_value_by_key("單元名稱") or find_value_by_key("Unit")
    docx_t0.cell(3, 2).text = unit_name
    # Design Rationale
    docx_t0.cell(4, 2).text = find_value_by_key("設計理念") or find_value_by_key("DesignRationale")
    # Core competencies
    docx_t0.cell(7, 2).text = find_value_by_key("核心素養") or find_value_by_key("Corecompetency")
    # Digital and AI competencies
    docx_t0.cell(7, 5).text = find_value_by_key("數位素養") or find_value_by_key("學生AI素養") or find_value_by_key("數位與學生AI素養")
    # Learning performance
    docx_t0.cell(10, 2).text = find_value_by_key("學習表現") or find_value_by_key("Students'performance") or find_value_by_key("Students’performance")
    # Learning content
    docx_t0.cell(11, 2).text = find_value_by_key("學習內容") or find_value_by_key("Learningcontent")
    # Issue Integration
    docx_t0.cell(12, 2).text = find_value_by_key("議題融入") or find_value_by_key("Issueintegration")

    # 3. Populate Table 1 (教學規劃與流程)
    print("Populating Table 1...")
    docx_t1 = doc.tables[1]

    # Connections
    docx_t1.cell(0, 2).text = find_value_by_key("與其他領域") or find_value_by_key("連結") or find_value_by_key("Connectionstoothersubjects")
    # Learning goals
    docx_t1.cell(1, 2).text = find_value_by_key("學習目標")
    # Learning tasks
    docx_t1.cell(2, 2).text = find_value_by_key("學習任務")
    # AI tools
    docx_t1.cell(3, 2).text = find_value_by_key("使用的AI工具") or find_value_by_key("使用的 AI 工具") or find_value_by_key("使用的AI工具或學位學習平臺")
    # Equipment
    docx_t1.cell(4, 2).text = find_value_by_key("教學設備/資源") or find_value_by_key("教學設備") or find_value_by_key("Teachingaids/equipment")
    # Background
    docx_t1.cell(5, 2).text = find_value_by_key("學生數位學習背景") or find_value_by_key("學生數位背景") or find_value_by_key("digitallearningBackground")
    # Resources
    docx_t1.cell(6, 2).text = find_value_by_key("教學資源")

    # Extract activity content
    # Collect activities under headings/tables
    activities = {"教師準備": "", "學生自學": "", "第1節": "", "第2節": "", "第3節": ""}
    evidence = {"教師準備": "", "學生自學": "", "第1節": "", "第2節": "", "第3節": ""}

    # Extract preparation from bullets first
    bullet_teacher, bullet_student = extract_prep_from_bullets(sections)
    if bullet_teacher:
        activities["教師準備"] = bullet_teacher
        evidence["教師準備"] = find_value_by_key("因材網課程包指派") or "課前教材準備紀錄（待確認）"
    if bullet_student:
        activities["學生自學"] = bullet_student
        evidence["學生自學"] = find_value_by_key("因材網影片觀看") or "課前學習紀錄（待確認）"

    # Now look at activity tables in markdown
    current_period = None
    # We walk the markdown headers and match tables
    # For robust matching, let's map by headings in sections or simply look at the activity tables' text
    # Let's inspect each activity table and find what period it belongs to by looking at its rows
    for t_idx, act_t in enumerate(activity_tables_md):
        # Determine period from rows or headers
        # If any row has "課前準備"
        is_prep = False
        period_name = None
        for row in act_t:
            r0 = clean_key(row[0])
            if "課前準備" in r0 or "教師" in r0:
                is_prep = True
                break
            elif "第一節" in r0 or "第1節" in r0 or "1節" in r0:
                period_name = "第1節"
                break
            elif "第二節" in r0 or "第2節" in r0 or "2節" in r0:
                period_name = "第2節"
                break
            elif "第三節" in r0 or "第3節" in r0 or "3節" in r0:
                period_name = "第3節"
                break

        if is_prep:
            # Table has preparation text
            for row in act_t[1:]: # skip header
                r0 = clean_key(row[0])
                val_col = row[1] if len(row) > 1 else ""
                ev_col = row[2] if len(row) > 2 else ""

                if "教師" in r0 or "課前準備" in r0:
                    # If both exist in one cell, try to split
                    if "【學生自學】" in val_col or "【學生準備】" in val_col:
                        split_keyword = "【學生自學】" if "【學生自學】" in val_col else "【學生準備】"
                        teacher_txt, student_txt = val_col.split(split_keyword, 1)
                        activities["教師準備"] = teacher_txt.strip()
                        activities["學生自學"] = student_txt.strip()
                    else:
                        activities["教師準備"] = val_col

                    if ev_col:
                        if "課前測驗" in ev_col:
                            evidence["教師準備"] = "課前教材準備紀錄（待確認）"
                            evidence["學生自學"] = ev_col
                        else:
                            evidence["教師準備"] = ev_col
                elif "學生" in r0 or "課前練習" in r0:
                    activities["學生自學"] = val_col
                    if ev_col:
                        evidence["學生自學"] = ev_col
        else:
            # It is a period table. If period_name is not detected from Col 0, infer it
            if not period_name:
                # Infer by count of periods
                period_name = f"第{len([p for p in activities.keys() if p.startswith('第') and activities[p]]) + 1}節"

            # Collect rows
            p_activities = []
            p_evidences = []
            for row in act_t[1:]:
                # C0 is teaching point, C1 is activity, C2 is evidence
                c0 = row[0]
                c1 = row[1] if len(row) > 1 else ""
                c2 = row[2] if len(row) > 2 else ""

                # Combine Col 0 and Col 1
                if c0 and c1:
                    p_activities.append(f"{c0}\n{c1}" if not c1.startswith(c0) else c1)
                elif c1:
                    p_activities.append(c1)

                if c2 and c2 not in p_evidences:
                    p_evidences.append(c2)

            activities[period_name] = "\n".join(p_activities)
            evidence[period_name] = "\n".join(p_evidences)

    # Fill activity rows in docx Table 1
    docx_t1.cell(10, 1).text = activities["教師準備"]
    docx_t1.cell(10, 3).text = evidence["教師準備"] or "課前教材準備紀錄（待確認）"

    docx_t1.cell(11, 1).text = activities["學生自學"]
    docx_t1.cell(11, 3).text = evidence["學生自學"] or "- 線上概念檢測作答記錄。"

    docx_t1.cell(12, 1).text = activities["第1節"]
    docx_t1.cell(12, 3).text = evidence["第1節"]

    docx_t1.cell(13, 1).text = activities["第2節"]
    docx_t1.cell(13, 3).text = evidence["第2節"]

    docx_t1.cell(14, 1).text = activities["第3節"]
    docx_t1.cell(14, 3).text = evidence["第3節"]

    # 4. Populate Table 2 (檢核表)
    print("Populating Table 2 (檢核表)...")
    docx_t2 = doc.tables[2]
    if checklist_md:
        for md_row in checklist_md[1:]:
            item_name = clean_key(md_row[0])
            v_val = md_row[2] if len(md_row) > 2 else ""
            light = md_row[3] if len(md_row) > 3 else ""

            # Match item_name in docx checklist
            for docx_row_idx, docx_row in enumerate(docx_t2.rows):
                docx_item = clean_key(docx_row.cells[0].text)
                if item_name in docx_item or docx_item in item_name:
                    docx_t2.cell(docx_row_idx, 2).text = v_val
                    docx_t2.cell(docx_row_idx, 3).text = light
                    break
    else:
        print("Warning: No Checklist table parsed from markdown! Filling default ticks.")
        # Default fallback
        for r_idx in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18]:
            docx_t2.cell(r_idx, 2).text = ""

    # 5. Populate Table 3 (融入矩陣)
    print("Populating Table 3 (融入矩陣)...")
    docx_t3 = doc.tables[3]
    docx_t3.cell(0, 3).text = unit_name or "待確認"

    if matrix_md:
        for md_row in matrix_md[1:]:
            # MD Row structure: C0 Category (備課/活動), C1 subcategory (共同備課/引起動機...), C2 'V', C3-C9 dimensions
            if len(md_row) < 3:
                continue
            subcat = clean_key(md_row[1])
            is_checked = "V" in md_row[2].upper()

            # Find the checked dimension in MD row (C3 to C9)
            checked_col_idx = None
            checked_desc = ""
            for c_idx in range(3, len(md_row)):
                if md_row[c_idx] and md_row[c_idx] != "V":
                    checked_col_idx = c_idx
                    checked_desc = md_row[c_idx]
                    break

            # Find matching subcategory in docx Table 3
            for docx_row_idx, docx_row in enumerate(docx_t3.rows):
                docx_subcat = clean_key(docx_row.cells[1].text)
                if subcat in docx_subcat or docx_subcat in subcat:
                    if is_checked or checked_col_idx:
                        docx_t3.cell(docx_row_idx, 2).text = "V"
                    if checked_col_idx and checked_col_idx < 10:
                        docx_t3.cell(docx_row_idx, checked_col_idx).text = checked_desc
                    break

    # 6. DYNAMIC INSERTIONS: Rubrics and Reflections
    print("Locating dynamic insertion target paragraphs...")
    p_rubrics = None
    p_reflection = None

    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt == "學習評量規準":
            p_rubrics = p
        elif txt == "教師教學反思":
            p_reflection = p

    # Insert Rubrics table
    if p_rubrics:
        print("Inserting Rubrics Table...")
        # 4 rows, 4 columns
        docx_t_rubrics = doc.add_table(rows=4, cols=4)

        # Extract Rubrics from md
        rubrics_data = [
            ["評量項目", "優秀 (Excellent)", "良好 (Good)", "待加強 (Needs improvement)"],
            ["課程概念理解\n(認知面)", "", "", ""],
            ["學習任務實作\n(技能/探究面)", "", "", ""],
            ["學生 AI 素養與事實查核\n(素養/倫理面)", "", "", ""]
        ]

        # If parsed from md, overwrite rubrics_data values
        if rubrics_md:
            for r_idx in range(min(4, len(rubrics_md))):
                for c_idx in range(min(4, len(rubrics_md[r_idx]))):
                    rubrics_data[r_idx][c_idx] = rubrics_md[r_idx][c_idx]
        else:
            print("Warning: Rubrics table not found in markdown! Filling default placeholder.")

        for r in range(4):
            for c in range(4):
                docx_t_rubrics.cell(r, c).text = rubrics_data[r][c]

        p_rubrics._p.addnext(docx_t_rubrics._tbl)
    else:
        print("Warning: Paragraph '學習評量規準' not found in template!")

    # Insert Teacher Reflections
    if p_reflection:
        print("Inserting Teacher Reflection paragraphs...")
        reflection_texts = []
        # Look in sections for "教師教學反思"
        ref_heading = None
        for heading in sections.keys():
            if "教師教學反思" in heading or "教學反思" in heading:
                ref_heading = heading
                break

        if ref_heading:
            reflection_texts = [p.strip() for p in sections[ref_heading] if p.strip()]
        else:
            print("Warning: Reflections not found in markdown! Inserting defaults.")
            reflection_texts = [
                "課後待填：檢視學生概念理解的學習證據。",
                "課後待填：檢視任務操作與合作情形。",
                "課後待填：記錄時間安排及後續調整。"
            ]

        current = p_reflection
        for txt in reflection_texts:
            new_p = doc.add_paragraph(txt)
            current._p.addnext(new_p._p)
            current = new_p
    else:
        print("Warning: Paragraph '教師教學反思' not found in template!")

    # 7. FORMATTING: 12pt FONT SIZE
    print("Formatting all text runs to 12pt...")
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(12)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(12)

    # Save document
    print(f"Saving output to '{output_docx_path}'...")
    doc.save(output_docx_path)
    print("Saved successfully!")

    # Self-verification of table shapes
    print("Performing self-verification of output...")
    v_doc = docx.Document(output_docx_path)
    expected_shapes = [
        (13, 8),   # Table 0
        (15, 4),   # Table 1
        (4, 4),    # Table 2 (Rubrics)
        (19, 4),   # Table 3 (Checklist)
        (15, 10),  # Table 4 (Matrix)
    ]

    print(f"Total tables: {len(v_doc.tables)} (Expected: 5)")
    mismatches = 0
    for idx, t in enumerate(v_doc.tables):
        r_count = len(t.rows)
        c_count = len(t.columns)
        exp_r, exp_c = expected_shapes[idx] if idx < len(expected_shapes) else (0, 0)
        status = "PASS" if r_count == exp_r and c_count == exp_c else "FAIL"
        if status == "FAIL":
            mismatches += 1
        print(f"  Table {idx}: rows={r_count} (Expected: {exp_r}), cols={c_count} (Expected: {exp_c}) -> {status}")

    if mismatches == 0 and len(v_doc.tables) == 5:
        print("Verification: SUCCESS! Table structures are perfectly aligned.")
        return True
    else:
        print("Verification: FAILED! Table structures do not match the template layout.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_docx.py <input_markdown_file> [output_docx_path]")
        sys.exit(1)

    md_in = sys.argv[1]
    if len(sys.argv) >= 3:
        docx_out = sys.argv[2]
    else:
        docx_out = os.path.splitext(md_in)[0] + ".docx"

    success = run_conversion(md_in, docx_out)
    if not success:
        sys.exit(1)

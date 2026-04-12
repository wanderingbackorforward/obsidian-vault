"""
将 7.1_draft.md、7.2_draft.md、7.3_draft.md 合并并生成符合论文排版规范的 docx。
"""
import re
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

WORK = r"D:\mine\mynotes\obsidian-vault\wkspc"
FILES = ["7.1_draft.md", "7.2_draft.md", "7.3_draft.md"]
OUTPUT = f"{WORK}\\chapter7_final.docx"

# ── helpers ──────────────────────────────────────────────
def set_run_font(run, cn_font="宋体", en_font="Times New Roman", size_pt=12, bold=False):
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.name = en_font
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)

def set_paragraph_spacing(para, before_pt=0, after_pt=0, line_spacing_pt=None):
    pPr = para._element.get_or_add_pPr()
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:before'), str(int(before_pt * 20)))
    spacing.set(qn('w:after'), str(int(after_pt * 20)))
    if line_spacing_pt:
        spacing.set(qn('w:line'), str(int(line_spacing_pt * 20)))
        spacing.set(qn('w:lineRule'), 'exact')

def set_first_line_indent(para, chars=2):
    pPr = para._element.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:firstLineChars'), str(chars * 100))

def add_heading(doc, text, level):
    """level: 0=章标题, 1=一级(7.x), 2=二级(7.x.x or 一/二/三...)"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    if level == 0:  # 章标题：黑体 三号16pt 加粗 居中
        set_run_font(run, "黑体", "Times New Roman", 16, bold=True)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(para, before_pt=24, after_pt=18, line_spacing_pt=20)
    elif level == 1:  # 一级：黑体 小三15pt 不加粗 左对齐
        set_run_font(run, "黑体", "Times New Roman", 15, bold=False)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(para, before_pt=24, after_pt=6, line_spacing_pt=20)
    elif level == 2:  # 二级：黑体 四号14pt 不加粗 左对齐
        set_run_font(run, "黑体", "Times New Roman", 14, bold=False)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(para, before_pt=12, after_pt=6, line_spacing_pt=20)
    return para

def add_body(doc, text):
    """正文：宋体/TNR 小四12pt 首行缩进2字符 ~22pt行距"""
    para = doc.add_paragraph()
    # 处理加粗标记
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            r = para.add_run(part[2:-2])
            set_run_font(r, "宋体", "Times New Roman", 12, bold=True)
        else:
            r = para.add_run(part)
            set_run_font(r, "宋体", "Times New Roman", 12, bold=False)
    set_first_line_indent(para, 2)
    set_paragraph_spacing(para, before_pt=0, after_pt=0, line_spacing_pt=22)
    return para

def add_table_caption(doc, text):
    """表题：表上方 黑体 五号10.5pt 居中"""
    para = doc.add_paragraph()
    run = para.add_run(text.replace('**', ''))
    set_run_font(run, "黑体", "Times New Roman", 10.5, bold=False)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(para, before_pt=12, after_pt=6)
    return para

def add_figure_caption(doc, text):
    """图题：图下方 宋体 五号10.5pt 居中"""
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_run_font(run, "宋体", "Times New Roman", 10.5, bold=False)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(para, before_pt=6, after_pt=12)
    return para

def add_table_from_rows(doc, headers, rows):
    """插入格式化表格"""
    if not headers or not rows:
        return
    ncols = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=ncols)
    tbl.style = 'Table Grid'
    # header
    for i, h in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h.strip())
        set_run_font(r, "黑体", "Times New Roman", 10.5, bold=True)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # data
    for ri, row in enumerate(rows):
        for ci in range(ncols):
            cell = tbl.rows[ri + 1].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            val = row[ci].strip() if ci < len(row) else ""
            r = p.add_run(val)
            set_run_font(r, "宋体", "Times New Roman", 10.5, bold=False)
    # 设置表格内段落行距
    for row in tbl.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                set_paragraph_spacing(p, line_spacing_pt=16)

# ── parse markdown ───────────────────────────────────────
def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

def is_table_sep(line):
    return bool(re.match(r'^\s*[-:]+[-|\s:]+$', line.strip()))

def is_table_border(line):
    return bool(re.match(r'^\s*-{5,}', line.strip()))

def preprocess_lines(lines):
    """合并被 Pandoc 拆断的续行，但保留表格区域原样。
    表格区域定义：以 **表7-x 标题** 开始，到最后一个 ----- 边框结束。"""
    # 第一步：标记表格区域
    # 找到所有 ----- 边框行的位置
    border_indices = []
    for idx, l in enumerate(lines):
        if re.match(r'^\s*-{5,}', l.strip()):
            border_indices.append(idx)

    # 将边框配对（每个表格有3个边框：顶部、分隔、底部）
    table_ranges = []
    i = 0
    while i < len(border_indices) - 1:
        start = border_indices[i]
        # 找到连续的边框组（属于同一个表格）
        # 一个表格至少有2个边框（顶部+底部），通常3个（+分隔线）
        end = border_indices[i]
        j = i + 1
        while j < len(border_indices) and border_indices[j] - border_indices[j-1] < 30:
            end = border_indices[j]
            j += 1
        # 往上找表格标题
        caption_start = start
        for k in range(start - 1, max(start - 3, -1), -1):
            if re.match(r'^\*\*表\d+-\d+', lines[k].strip()):
                caption_start = k
                break
        table_ranges.append((caption_start, end))
        i = j

    # 标记表格行
    table_flags = [False] * len(lines)
    for s, e in table_ranges:
        for idx in range(s, e + 1):
            table_flags[idx] = True

    # 第二步：非表格区域内，合并连续非空非特殊行
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        stripped = line.strip()

        # 表格区域行直接保留
        if table_flags[i]:
            result.append(line)
            i += 1
            continue

        # 特殊行直接保留
        if (not stripped or
            stripped.startswith('#') or
            re.match(r'^!\[', stripped)):
            result.append(line)
            i += 1
            continue

        # 普通文本行：向前看合并续行
        merged = stripped
        i += 1
        while i < len(lines):
            if table_flags[i]:
                break
            next_stripped = lines[i].strip()
            if (not next_stripped or
                next_stripped.startswith('#') or
                re.match(r'^!\[', next_stripped)):
                break
            merged += next_stripped
            i += 1
        result.append(merged)

    return [l + '\n' for l in result]

def process_lines(doc, lines):
    lines = preprocess_lines(lines)
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        stripped = line.strip()

        # skip empty
        if not stripped:
            i += 1
            continue

        # skip image lines (![...](...)...)  -- we'll add caption separately
        if re.match(r'^!\[', stripped):
            # extract caption text
            m = re.match(r'!\[(.*?)\]', stripped)
            if m:
                cap = m.group(1)
                add_figure_caption(doc, cap)
            i += 1
            continue

        # headings
        if stripped.startswith('#'):
            m = re.match(r'^(#+)\s+(.*)', stripped)
            if m:
                hashes = len(m.group(1))
                text = m.group(2).strip()
                if hashes == 1:  # # 第7章
                    add_heading(doc, text, 0)
                elif hashes == 2:  # ## 7.x
                    add_heading(doc, text, 1)
                elif hashes >= 3:  # ### 二级
                    # 去掉 "一、" 这种前缀中的中文数字序号格式不变，直接用
                    add_heading(doc, text, 2)
            i += 1
            continue

        # table caption (bold line like **表7-1 xxx**)
        if re.match(r'^\*\*表\d+-\d+', stripped):
            add_table_caption(doc, stripped)
            i += 1
            continue

        # pandoc-style table (lines of dashes)
        if is_table_border(stripped):
            # collect table block
            i += 1  # skip top border
            if i >= len(lines):
                break
            # read header line(s)
            header_lines = []
            while i < len(lines) and not is_table_border(lines[i].strip()) and not is_table_sep(lines[i].strip()):
                header_lines.append(lines[i].rstrip('\n'))
                i += 1
            # skip separator
            if i < len(lines):
                # parse column positions from the separator/border
                sep_line = lines[i].rstrip('\n')
                # find column boundaries from spaces in separator
                col_ranges = []
                in_col = False
                start = 0
                for ci, ch in enumerate(sep_line):
                    if ch == '-' and not in_col:
                        in_col = True
                        start = ci
                    elif ch == ' ' and in_col:
                        in_col = False
                        col_ranges.append((start, ci))
                if in_col:
                    col_ranges.append((start, len(sep_line)))
                i += 1

            if not col_ranges:
                # fallback: try space-split
                col_ranges = None

            def extract_cols(text_line, ranges):
                if ranges:
                    cols = []
                    for s, e in ranges:
                        end = min(e, len(text_line))
                        cols.append(text_line[s:end].strip() if s < len(text_line) else "")
                    return cols
                else:
                    return text_line.split()

            # parse headers
            headers = extract_cols(header_lines[0] if header_lines else "", col_ranges)

            # read data rows until bottom border
            data_rows = []
            current_row = None
            while i < len(lines):
                dl = lines[i].rstrip('\n')
                if is_table_border(dl.strip()):
                    if current_row:
                        data_rows.append(current_row)
                    i += 1
                    break
                if not dl.strip():
                    i += 1
                    continue
                cols = extract_cols(dl, col_ranges)
                # check if this is a continuation (first col empty)
                if cols and cols[0] == '' and current_row:
                    # merge into current row
                    for ci in range(len(cols)):
                        if ci < len(current_row) and cols[ci]:
                            current_row[ci] = (current_row[ci] + " " + cols[ci]).strip()
                else:
                    if current_row:
                        data_rows.append(current_row)
                    current_row = cols
                i += 1
            if current_row:
                data_rows.append(current_row)

            add_table_from_rows(doc, headers, data_rows)
            continue

        # regular body paragraph - may span multiple lines until empty line or heading
        para_text = stripped
        i += 1
        # don't merge next lines, each non-empty non-special line is its own paragraph in md
        # Actually in these drafts, paragraphs are single long lines
        # Clean markdown artifacts
        para_text = re.sub(r'\{#fig:\S+\}', '', para_text)
        para_text = para_text.replace('------', '——')
        add_body(doc, para_text)
        continue

    return doc

# ── main ─────────────────────────────────────────────────
def main():
    doc = Document()

    # 页面设置 A4
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2.5)

    for fname in FILES:
        path = f"{WORK}\\{fname}"
        lines = parse_md(path)
        process_lines(doc, lines)

    doc.save(OUTPUT)
    print(f"Done → {OUTPUT}")

if __name__ == "__main__":
    main()

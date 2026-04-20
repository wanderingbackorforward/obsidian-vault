"""
将 .docx 文档高保真转换为单个 Markdown 文件。
图片提取到资源目录，其余所有内容（标题、正文、表格、链接、图片引用）
全部收敛到一个 .md 文件中。
"""
import argparse
import os
import re
import zipfile
from pathlib import Path
from lxml import etree

from docx import Document
from docx.oxml.ns import qn

NS = {
    'w':  'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'v':  'urn:schemas-microsoft-com:vml',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}

# font-size (EMU) -> heading level, derived from format_chapter7.py
SIZE_HEADING_MAP = {
    203200: 1,   # 16pt  章标题
    190500: 2,   # 15pt  一级节标题 (7.x)
    177800: 3,   # 14pt  二级节标题 (一、二、...)
}
BODY_SIZE = 152400       # 12pt
CAPTION_SIZE = 133350    # 10.5pt


# ── image extraction ────────────────────────────────────

def extract_images(docx_path: str, assets_dir: str) -> dict:
    """从 docx 的 zip 中提取所有 media/ 图片，返回 {原始路径: 导出路径}。"""
    os.makedirs(assets_dir, exist_ok=True)
    mapping = {}
    with zipfile.ZipFile(docx_path, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('word/media/'):
                fname = os.path.basename(name)
                out_path = os.path.join(assets_dir, fname)
                with zf.open(name) as src, open(out_path, 'wb') as dst:
                    dst.write(src.read())
                mapping[name] = out_path
    return mapping


def build_rel_image_map(doc: Document, image_files: dict, assets_dir: str, md_dir: str) -> dict:
    """建立 rId -> markdown 相对路径 的映射。"""
    rel_map = {}
    for rel_id, rel in doc.part.rels.items():
        if 'image' in str(rel.reltype):
            target = f'word/{rel.target_ref}'
            if target in image_files:
                abs_path = image_files[target]
                rel_path = os.path.relpath(abs_path, md_dir).replace('\\', '/')
                rel_map[rel_id] = rel_path
    return rel_map


# ── paragraph-level helpers ─────────────────────────────

def _get_font_size(run_elem):
    """从 run XML 获取字号 (EMU)，优先 w:sz。"""
    rPr = run_elem.find('w:rPr', NS)
    if rPr is not None:
        sz = rPr.find('w:sz', NS)
        if sz is not None:
            half_pt = int(sz.get(qn('w:val')))
            return half_pt * 6350  # half-point -> EMU
    return None


def _detect_heading_level(para) -> int:
    """根据字号和加粗判断标题级别，返回 0 表示非标题。"""
    if not para.text.strip():
        return 0
    first_size = None
    first_bold = False
    for run in para.runs:
        if not run.text.strip():
            continue
        size = run.font.size
        if size is None:
            size = _get_font_size(run._element)
        if size is not None:
            first_size = size
            first_bold = bool(run.bold)
            break
    if first_size in SIZE_HEADING_MAP:
        return SIZE_HEADING_MAP[first_size]
    return 0


def _is_caption(para) -> bool:
    """判断是否为图题/表题（10.5pt 居中）。"""
    text = para.text.strip()
    if not text:
        return False
    if re.match(r'^[图表]\d+-\d+', text):
        return True
    for run in para.runs:
        size = run.font.size
        if size is None:
            size = _get_font_size(run._element)
        if size == CAPTION_SIZE:
            return True
        break
    return False


def _extract_images_from_para(para_elem, rel_map: dict) -> list:
    """从段落 XML 中提取所有图片引用，返回 [(rel_path, alt_text), ...]。"""
    images = []
    for drawing in para_elem.findall('.//w:drawing', NS):
        blip = drawing.find(f'.//{{{NS["a"]}}}blip')
        if blip is not None:
            embed = blip.get(qn('r:embed'))
            if embed and embed in rel_map:
                # 尝试获取 alt text
                doc_pr = drawing.find(f'.//{{{NS["wp"]}}}docPr')
                alt = ''
                if doc_pr is not None:
                    alt = doc_pr.get('descr', '') or doc_pr.get('name', '')
                images.append((rel_map[embed], alt))
    # VML 格式图片 (兼容旧版)
    for imagedata in para_elem.findall(f'.//{{{NS["v"]}}}imagedata'):
        rid = imagedata.get(qn('r:id'))
        if rid and rid in rel_map:
            images.append((rel_map[rid], ''))
    return images


def _para_has_hyperlinks(para_elem) -> bool:
    return len(para_elem.findall('w:hyperlink', NS)) > 0


def _build_inline_text(para, rel_map: dict, doc_rels: dict) -> str:
    """将段落的 runs + hyperlinks 组装为 Markdown 行内文本，保留加粗/斜体/链接。"""
    parts = []
    for child in para._element:
        tag = etree.QName(child.tag).localname

        if tag == 'hyperlink':
            rid = child.get(qn('r:id'))
            url = ''
            if rid and rid in doc_rels:
                url = doc_rels[rid]
            link_text = ''.join(
                t.text or '' for t in child.findall('.//w:t', NS)
            )
            if url:
                parts.append(f'[{link_text}]({url})')
            else:
                parts.append(link_text)

        elif tag == 'r':
            from docx.text.run import Run
            run = Run(child, para)
            text = run.text
            if not text:
                continue
            bold = run.bold
            italic = run.italic
            if bold and italic:
                parts.append(f'***{text}***')
            elif bold:
                parts.append(f'**{text}**')
            elif italic:
                parts.append(f'*{text}*')
            else:
                parts.append(text)

    return ''.join(parts)


# ── table conversion ────────────────────────────────────

def _cell_text(cell) -> str:
    """提取单元格纯文本，多段落用 <br> 连接。"""
    texts = []
    for p in cell.paragraphs:
        texts.append(p.text.strip())
    return '<br>'.join(t for t in texts if t)


def _table_has_merged_cells(table) -> bool:
    """检测表格是否有合并单元格。"""
    for row in table.rows:
        for cell in row.cells:
            tc = cell._element
            grid_span = tc.find('.//w:gridSpan', NS)
            v_merge = tc.find('.//w:vMerge', NS)
            if grid_span is not None:
                val = grid_span.get(qn('w:val'))
                if val and int(val) > 1:
                    return True
            if v_merge is not None:
                return True
    return False


def _table_to_md(table) -> str:
    """将 python-docx Table 转为 Markdown 表格或 HTML table。"""
    rows_data = []
    for row in table.rows:
        row_cells = [_cell_text(c) for c in row.cells]
        rows_data.append(row_cells)

    if not rows_data:
        return ''

    if _table_has_merged_cells(table):
        return _table_to_html(table)

    ncols = max(len(r) for r in rows_data)
    for r in rows_data:
        while len(r) < ncols:
            r.append('')

    # 去重相邻相同单元格（python-docx 对合并单元格会重复）
    for r in rows_data:
        seen = {}
        for ci in range(len(r)):
            if ci > 0 and r[ci] == r[ci - 1] and r[ci]:
                r[ci] = ''

    lines = []
    header = rows_data[0]
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('| ' + ' | '.join(['---'] * ncols) + ' |')
    for row in rows_data[1:]:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)


def _table_to_html(table) -> str:
    """复杂表格降级为 HTML。"""
    lines = ['<table>', '<thead>', '<tr>']
    first_row = True
    for row in table.rows:
        if not first_row:
            lines.append('<tr>')
        for cell in row.cells:
            tag = 'th' if first_row else 'td'
            text = _cell_text(cell)
            lines.append(f'  <{tag}>{text}</{tag}>')
        lines.append('</tr>')
        if first_row:
            lines.append('</thead>')
            lines.append('<tbody>')
            first_row = False
    lines.append('</tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


# ── main conversion ────────────────────────────────────

def convert(docx_path: str, output_path: str, assets_dir: str):
    docx_path = os.path.abspath(docx_path)
    output_path = os.path.abspath(output_path)
    assets_dir = os.path.abspath(assets_dir)
    md_dir = os.path.dirname(output_path)
    os.makedirs(md_dir, exist_ok=True)

    image_files = extract_images(docx_path, assets_dir)
    doc = Document(docx_path)
    rel_map = build_rel_image_map(doc, image_files, assets_dir, md_dir)

    # 收集 hyperlink rels
    doc_rels = {}
    for rel_id, rel in doc.part.rels.items():
        if 'hyperlink' in str(rel.reltype).lower():
            doc_rels[rel_id] = rel.target_ref

    body = doc.element.body
    md_lines = []
    img_counter = 0

    # 按 body 子元素顺序遍历，保持文档原始顺序
    para_index = 0
    table_index = 0

    for child in body:
        tag = etree.QName(child.tag).localname

        if tag == 'p':
            para = doc.paragraphs[para_index]
            para_index += 1
            text = para.text.strip()

            # 提取段落中的图片
            images = _extract_images_from_para(child, rel_map)
            if images:
                for img_path, alt_text in images:
                    img_counter += 1
                    alt = alt_text if alt_text else f'image_{img_counter:03d}'
                    md_lines.append(f'![{alt}]({img_path})')
                    md_lines.append('')
                if not text:
                    continue

            if not text:
                continue

            # 判断标题
            heading_level = _detect_heading_level(para)
            if heading_level > 0:
                prefix = '#' * heading_level
                md_lines.append(f'{prefix} {text}')
                md_lines.append('')
                continue

            # 判断图题/表题
            if _is_caption(para):
                md_lines.append(f'*{text}*')
                md_lines.append('')
                continue

            # 普通段落：组装行内格式
            inline = _build_inline_text(para, rel_map, doc_rels)
            md_lines.append(inline)
            md_lines.append('')

        elif tag == 'tbl':
            table = doc.tables[table_index]
            table_index += 1
            md_lines.append(_table_to_md(table))
            md_lines.append('')

    # 清理多余空行（连续 3 个以上空行合并为 2 个）
    result = []
    blank_count = 0
    for line in md_lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                result.append('')
        else:
            blank_count = 0
            result.append(line)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result).strip() + '\n')

    img_count = len([f for f in os.listdir(assets_dir)]) if os.path.isdir(assets_dir) else 0
    print(f'Done -> {output_path}')
    print(f'Images -> {assets_dir} ({img_count} files)')


def main():
    parser = argparse.ArgumentParser(
        description='将 .docx 文档转换为单个 Markdown 文件'
    )
    parser.add_argument('--input', required=True, help='输入 .docx 文件路径')
    parser.add_argument('--output', default=None, help='输出 .md 文件路径')
    parser.add_argument('--assets-dir', default=None, help='图片资源输出目录')
    args = parser.parse_args()

    docx_path = args.input
    if not os.path.isfile(docx_path):
        print(f'Error: file not found: {docx_path}')
        return

    stem = Path(docx_path).stem
    out_dir = os.path.join(os.path.dirname(docx_path) or '.', 'output')
    output_path = args.output or os.path.join(out_dir, f'{stem}.md')
    assets_dir = args.assets_dir or os.path.join(os.path.dirname(output_path), 'images')

    convert(docx_path, output_path, assets_dir)


if __name__ == '__main__':
    main()

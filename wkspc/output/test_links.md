<a id="section_1"></a>
# 第1节 测试文档概述

本文档用于测试 docx_to_md.py 对链接与跳转的处理能力。

请访问 [OpenAI 官网](https://openai.com/) 了解更多信息。

相关资源：[GitHub](https://github.com/)、[Python 文档](https://docs.python.org/3/)、[Stack Overflow](https://stackoverflow.com/)。

关于链接测试的详细内容，请参见[第2节 外部超链接测试](#section_2)。

关于书签测试，请参见[第3节](#section_3)。

<a id="section_2"></a>
## 第2节 外部超链接测试

本节测试外部超链接在转换后是否保留为 Markdown 链接格式。

这是一个**加粗文本**后面紧跟[一个链接](https://example.com/test)的混排段落。

<a id="section_3"></a>
## 第3节 内部书签跳转测试

本节测试内部书签跳转（w:anchor）在转换后的处理。

点击可以跳回[第1节 测试文档概述](#section_1)。

<a id="important_mark"></a>
这里有一个重要标记。

从这里跳转到[重要标记位置](#important_mark)。

<a id="section_4"></a>
## 第4节 交叉引用与域代码测试

本节测试 Word 域代码（field code）形式的交叉引用。

如[第2节 外部超链接测试](#section_2)所述，外部链接应保留完整 URL。

另见[重要标记位置](#important_mark)中的说明。

## 第5节 表格与链接混合

| 名称 | 链接 |
| --- | --- |
| Python | [python.org](https://www.python.org/) |
| Rust | [rust-lang.org](https://www.rust-lang.org/) |

返回[文档开头](#section_1)。

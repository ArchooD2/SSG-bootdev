import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<p>This is <b>bolded</b> paragraph "
                "text in a p tag here</p>"
                "<p>This is another paragraph with "
                "<i>italic</i> text and "
                "<code>code</code> here</p>"
                "</div>"
            ),
        )

    def test_codeblock(self):
        md = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```"
        )

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div><pre><code>"
                "This is text that _should_ remain\n"
                "the **same** even with inline stuff\n"
                "</code></pre></div>"
            ),
        )

    def test_heading(self):
        node = markdown_to_html_node(
            "## This is a **heading**"
        )

        self.assertEqual(
            node.to_html(),
            "<div><h2>This is a <b>heading</b></h2></div>",
        )

    def test_quote(self):
        md = """> This is a quote
> with **bold text**"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div><blockquote>"
                "This is a quote with <b>bold text</b>"
                "</blockquote></div>"
            ),
        )

    def test_quote_without_spaces(self):
        md = """>First line
>Second line"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div><blockquote>"
                "First line Second line"
                "</blockquote></div>"
            ),
        )

    def test_unordered_list(self):
        md = """- First item
- Second **bold** item
- Third item"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div><ul>"
                "<li>First item</li>"
                "<li>Second <b>bold</b> item</li>"
                "<li>Third item</li>"
                "</ul></div>"
            ),
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second _italic_ item
3. Third item"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div><ol>"
                "<li>First item</li>"
                "<li>Second <i>italic</i> item</li>"
                "<li>Third item</li>"
                "</ol></div>"
            ),
        )

    def test_multiple_block_types(self):
        md = """# Heading

This is a paragraph.

- Item one
- Item two

> A quote"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<h1>Heading</h1>"
                "<p>This is a paragraph.</p>"
                "<ul>"
                "<li>Item one</li>"
                "<li>Item two</li>"
                "</ul>"
                "<blockquote>A quote</blockquote>"
                "</div>"
            ),
        )

    def test_empty_document(self):
        node = markdown_to_html_node("")

        self.assertEqual(
            node.to_html(),
            "<div></div>",
        )


if __name__ == "__main__":
    unittest.main()
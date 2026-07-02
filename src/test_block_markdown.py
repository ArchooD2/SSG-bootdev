import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                (
                    "This is another paragraph with _italic_ text "
                    "and `code` here\n"
                    "This is the same paragraph on a new line"
                ),
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_blank_lines(self):
        md = """
First block



Second block




Third block
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """

   First block   

   
Second block

"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
            ],
        )

    def test_single_block(self):
        blocks = markdown_to_blocks(
            "This is one paragraph\nwith two lines"
        )

        self.assertEqual(
            blocks,
            [
                "This is one paragraph\nwith two lines",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(
            markdown_to_blocks("\n\n   \n\n"),
            [],
        )

    def test_heading_paragraph_and_list(self):
        md = """# Heading

This is a paragraph.

- Item one
- Item two"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "- Item one\n- Item two",
            ],
        )


if __name__ == "__main__":
    unittest.main()
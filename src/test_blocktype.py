import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_multiline_paragraph(self):
        block = (
            "This is the first line.\n"
            "This is the second line."
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_one(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_heading_six(self):
        self.assertEqual(
            block_to_block_type("###### Small heading"),
            BlockType.HEADING,
        )

    def test_heading_too_many_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Not a heading"),
            BlockType.PARAGRAPH,
        )

    def test_heading_without_space(self):
        self.assertEqual(
            block_to_block_type("##Not a heading"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_multiline_code(self):
        block = (
            "```\n"
            "def hello():\n"
            "    print('hello')\n"
            "```"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_without_opening_newline(self):
        block = "```print('hello')```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unclosed_code(self):
        block = "```\nprint('hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote(self):
        block = "> This is a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_without_space(self):
        block = ">This is also a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_multiline_quote(self):
        block = (
            "> First line\n"
            ">Second line\n"
            "> Third line"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = (
            "> First line\n"
            "Second line"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = (
            "- First item\n"
            "- Second item\n"
            "- Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = (
            "- First item\n"
            "Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list_without_space(self):
        block = (
            "-First item\n"
            "-Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = (
            "1. First item\n"
            "2. Second item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        block = (
            "2. First item\n"
            "3. Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_wrong_sequence(self):
        block = (
            "1. First item\n"
            "3. Third item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_without_space(self):
        block = (
            "1.First item\n"
            "2.Second item"
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
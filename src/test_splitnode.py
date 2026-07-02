import unittest

from splitnode import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode(
            "This has a **bold phrase** inside",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode(
            "This has an _italic phrase_ inside",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            result,
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" inside", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode(
            "Use `print()` and then `return`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            result,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" and then ", TextType.TEXT),
                TextNode("return", TextType.CODE),
            ],
        )

    def test_non_text_node_is_unchanged(self):
        bold_node = TextNode("Already bold", TextType.BOLD)

        result = split_nodes_delimiter(
            [bold_node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(result, [bold_node])
        self.assertIs(result[0], bold_node)

    def test_mixed_input_nodes(self):
        nodes = [
            TextNode("Start with `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode(" and more `code`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            result,
            [
                TextNode("Start with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("Already bold", TextType.BOLD),
                TextNode(" and more ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_unmatched_delimiter(self):
        node = TextNode(
            "This has an `unclosed code section",
            TextType.TEXT,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )

    def test_no_delimiter(self):
        node = TextNode(
            "This is ordinary text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(result, [node])

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**entirely bold**", TextType.TEXT)

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("entirely bold", TextType.BOLD),
            ],
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_one_image(self):
        node = TextNode(
            "Before ![image](https://example.com/image.png) after",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" after", TextType.TEXT),
            ],
            result,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another "
            "![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(
                    " and another ",
                    TextType.TEXT,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            result,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) after",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" after", TextType.TEXT),
            ],
            result,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Before ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            result,
        )

    def test_only_image(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            result,
        )

    def test_no_images(self):
        node = TextNode("Ordinary text", TextType.TEXT)

        result = split_nodes_image([node])

        self.assertListEqual([node], result)

    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)

        result = split_nodes_image([node])

        self.assertListEqual([node], result)
        self.assertIs(result[0], node)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_one_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) today",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" today", TextType.TEXT),
            ],
            result,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link "
            "[to boot dev](https://www.boot.dev) "
            "and [to youtube]"
            "(https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link ",
                    TextType.TEXT,
                ),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            result,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is useful",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" is useful", TextType.TEXT),
            ],
            result,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            result,
        )

    def test_only_link(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            result,
        )

    def test_no_links(self):
        node = TextNode("Ordinary text", TextType.TEXT)

        result = split_nodes_link([node])

        self.assertListEqual([node], result)

    def test_images_are_not_links(self):
        node = TextNode(
            "An ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual([node], result)

    def test_non_text_node_unchanged(self):
        node = TextNode(
            "Existing link",
            TextType.LINK,
            "https://example.com",
        )

        result = split_nodes_link([node])

        self.assertListEqual([node], result)
        self.assertIs(result[0], node)

class TestTextToTextNodes(unittest.TestCase):
    def test_all_markdown_types(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        result = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            result,
        )

    def test_plain_text(self):
        result = text_to_textnodes("Just plain text")

        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            result,
        )

    def test_multiple_same_types(self):
        result = text_to_textnodes(
            "**first** and **second** and `code one` plus `code two`"
        )

        self.assertListEqual(
            [
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code one", TextType.CODE),
                TextNode(" plus ", TextType.TEXT),
                TextNode("code two", TextType.CODE),
            ],
            result,
        )

    def test_markdown_at_boundaries(self):
        result = text_to_textnodes(
            "**bold** middle [link](https://example.com)"
        )

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
            result,
        )

    def test_unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            text_to_textnodes(
                "This has an **unclosed bold section"
            )

    def test_image_and_link_together(self):
        result = text_to_textnodes(
            "![cat](https://example.com/cat.png) "
            "[site](https://example.com)"
        )

        self.assertListEqual(
            [
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "https://example.com/cat.png",
                ),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "site",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
            result,
        )

if __name__ == "__main__":
    unittest.main()
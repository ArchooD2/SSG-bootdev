import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)")

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a string")
    
    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        self.assertEqual(node.url, "https://example.com")
    
    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.LINK, https://example.com)")
    
    def test_neq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, url="https://different.com")
        self.assertNotEqual(node, node2)
    
    def test_neq_with_url_and_text(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://example.com")
        node2 = TextNode("This is a different text node", TextType.LINK, url="https://example.com")
        self.assertNotEqual(node, node2)
    
    def test_neq_with_url_and_type(self):
        node = TextNode(
            "This is a text node",
            TextType.LINK,
            url="https://example.com",
        )
        node2 = TextNode(
            "This is a text node",
            TextType.IMAGE,
            url="https://example.com",
        )
        self.assertNotEqual(node, node2)
    
    def test_type_url_mismatch(self):
        for text_type in (
            TextType.TEXT,
            TextType.BOLD,
            TextType.ITALIC,
            TextType.CODE,
        ):
            with self.subTest(text_type=text_type):
                with self.assertRaises(ValueError):
                    TextNode(
                        "This is a text node",
                        text_type,
                        url="https://example.com",
                    )

    def test_url_required(self):
        for text_type in (TextType.LINK, TextType.IMAGE):
            with self.subTest(text_type=text_type):
                with self.assertRaises(ValueError):
                    TextNode("text", text_type)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(
            html_node.to_html(),
            "<code>print('hello')</code>",
        )

    def test_link(self):
        node = TextNode(
            "Click here",
            TextType.LINK,
            "https://example.com",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(
            html_node.props,
            {"href": "https://example.com"},
        )
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://example.com">Click here</a>',
        )

    def test_image(self):
        node = TextNode(
            "Example image",
            TextType.IMAGE,
            "https://example.com/image.png",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.png",
                "alt": "Example image",
            },
        )
        self.assertEqual(
            html_node.to_html(),
            (
                '<img src="https://example.com/image.png" '
                'alt="Example image"></img>'
            ),
        )

    def test_invalid_text_type(self):
        node = TextNode("Invalid", TextType.TEXT)
        node.text_type = "not a real text type"

        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_text_to_html(self):
        node = TextNode("raw text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
    
        self.assertEqual(html_node.to_html(), "raw text")


if __name__ == "__main__":
    unittest.main()
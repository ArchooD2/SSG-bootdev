import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>",
        )

    def test_leaf_to_html_link(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_raw_text(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_without_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("strong", "Bold text")
        self.assertIsNone(node.children)


if __name__ == "__main__":
    unittest.main()
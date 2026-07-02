import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_one_child(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])

        self.assertEqual(
            parent.to_html(),
            "<div><span>child</span></div>",
        )

    def test_to_html_with_multiple_children(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "More normal text"),
            ],
        )

        self.assertEqual(
            parent.to_html(),
            (
                "<p>"
                "<b>Bold text</b>"
                "Normal text"
                "<i>Italic text</i>"
                "More normal text"
                "</p>"
            ),
        )

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])

        self.assertEqual(
            parent.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        parent = ParentNode(
            "div",
            [LeafNode(None, "content")],
            {
                "class": "container",
                "id": "main",
            },
        )

        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main">content</div>',
        )

    def test_to_html_with_nested_props(self):
        child = ParentNode(
            "section",
            [LeafNode("p", "Hello")],
            {"class": "content"},
        )
        parent = ParentNode(
            "main",
            [child],
            {"id": "page"},
        )

        self.assertEqual(
            parent.to_html(),
            (
                '<main id="page">'
                '<section class="content">'
                "<p>Hello</p>"
                "</section>"
                "</main>"
            ),
        )

    def test_missing_tag(self):
        parent = ParentNode(
            None,
            [LeafNode("p", "Hello")],
        )

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_missing_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_empty_children(self):
        parent = ParentNode("div", [])

        self.assertEqual(
            parent.to_html(),
            "<div></div>",
        )

    def test_repr(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("div", [child], {"class": "box"})

        result = repr(parent)

        self.assertIn("tag=div", result)
        self.assertIn("children=", result)
        self.assertIn("class", result)

    def test_deeply_nested_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [
                                LeafNode("h1", "Title"),
                                LeafNode("p", "Body"),
                            ],
                        ),
                    ],
                ),
            ],
        )

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<section>"
                "<article>"
                "<h1>Title</h1>"
                "<p>Body</p>"
                "</article>"
                "</section>"
                "</div>"
            ),
        )


if __name__ == "__main__":
    unittest.main()
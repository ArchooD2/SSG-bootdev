import unittest

from markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestMarkdownExtract(unittest.TestCase):
    def test_extract_one_image(self):
        matches = extract_markdown_images(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        text = (
            "This is text with a "
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(text),
        )

    def test_extract_one_link(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://www.boot.dev)"
        )

        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev")],
            matches,
        )

    def test_extract_multiple_links(self):
        text = (
            "Visit [Boot.dev](https://www.boot.dev) "
            "and [YouTube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual(
            [
                ("Boot.dev", "https://www.boot.dev"),
                (
                    "YouTube",
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            extract_markdown_links(text),
        )

    def test_links_do_not_include_images(self):
        text = (
            "Here is ![an image](https://example.com/image.png) "
            "and [a link](https://example.com)"
        )

        self.assertListEqual(
            [("a link", "https://example.com")],
            extract_markdown_links(text),
        )

    def test_images_do_not_include_links(self):
        text = (
            "Here is ![an image](https://example.com/image.png) "
            "and [a link](https://example.com)"
        )

        self.assertListEqual(
            [("an image", "https://example.com/image.png")],
            extract_markdown_images(text),
        )

    def test_no_images(self):
        self.assertListEqual(
            [],
            extract_markdown_images("There are no images here."),
        )

    def test_no_links(self):
        self.assertListEqual(
            [],
            extract_markdown_links("There are no links here."),
        )

    def test_empty_alt_text(self):
        self.assertListEqual(
            [("", "https://example.com/image.png")],
            extract_markdown_images(
                "![](https://example.com/image.png)"
            ),
        )

    def test_empty_anchor_text(self):
        self.assertListEqual(
            [("", "https://example.com")],
            extract_markdown_links(
                "[](https://example.com)"
            ),
        )


if __name__ == "__main__":
    unittest.main()
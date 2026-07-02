from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: str | None = None,
    ):
        self.text = text
        self.text_type = text_type

        if text_type in (TextType.LINK, TextType.IMAGE) and url is None:
            raise ValueError(
                f"URL must be provided for {text_type.name} text type"
            )

        if text_type not in (TextType.LINK, TextType.IMAGE) and url is not None:
            raise ValueError(
                "URL should only be provided for LINK and IMAGE text types"
            )

        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode(
            "a",
            text_node.text,
            {"href": text_node.url},
        )

    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img",
            "",
            {
                "src": text_node.url,
                "alt": text_node.text,
            },
        )

    raise ValueError(f"Unsupported TextType: {text_node.text_type}")
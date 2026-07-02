from block_markdown import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from parentnode import ParentNode
from leafnode import LeafNode
from splitnode import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)

    return [
        text_node_to_html_node(text_node)
        for text_node in text_nodes
    ]


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    children = text_to_children(text)

    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    heading_level = 0

    while heading_level < len(block) and block[heading_level] == "#":
        heading_level += 1

    text = block[heading_level + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{heading_level}", children)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    quote_lines = []

    for line in lines:
        quote_lines.append(line[1:].lstrip())

    text = " ".join(quote_lines)
    children = text_to_children(text)

    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> ParentNode:
    list_items = []

    for line in block.split("\n"):
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    list_items = []

    for line in block.split("\n"):
        _, text = line.split(". ", 1)
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)


def code_to_html_node(block: str) -> ParentNode:
    code_text = block[4:-3]

    if not code_text.endswith("\n"):
        code_text += "\n"

    text_node = TextNode(code_text, TextType.TEXT)
    code_leaf = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [code_leaf])

    return ParentNode("pre", [code_node])


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)
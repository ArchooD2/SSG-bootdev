from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unmatched delimiter {delimiter!r}"
            )

        split_nodes = []

        for index, section in enumerate(sections):
            if section == "":
                continue

            if index % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

from textnode import TextNode, TextType
from markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)

        if not images:
            new_nodes.append(old_node)
            continue

        for alt_text, url in images:
            markdown = f"![{alt_text}]({url})"
            sections = remaining_text.split(markdown, 1)

            if sections[0]:
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(alt_text, TextType.IMAGE, url)
            )

            remaining_text = sections[1]

        if remaining_text:
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)

        if not links:
            new_nodes.append(old_node)
            continue

        for anchor_text, url in links:
            markdown = f"[{anchor_text}]({url})"
            sections = remaining_text.split(markdown, 1)

            if sections[0]:
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(anchor_text, TextType.LINK, url)
            )

            remaining_text = sections[1]

        if remaining_text:
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
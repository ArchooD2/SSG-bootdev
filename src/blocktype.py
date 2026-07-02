from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    # Heading: 1-6 # characters followed by a space.
    if block.startswith("#"):
        heading_parts = block.split(" ", 1)

        if len(heading_parts) == 2:
            hashes = heading_parts[0]

            if 1 <= len(hashes) <= 6 and all(
                character == "#" for character in hashes
            ):
                return BlockType.HEADING

    # Code: opening backticks plus newline, and closing backticks.
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Every line must begin with >.
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Every line must begin with "- ".
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Every ordered-list line must have the expected number.
    is_ordered_list = True

    for index, line in enumerate(lines, start=1):
        expected_prefix = f"{index}. "

        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
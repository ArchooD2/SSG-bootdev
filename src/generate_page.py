import os

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("Markdown document does not contain an h1 heading")


def generate_page(
    from_path: str,
    template_path: str,
    dest_path: str,
) -> None:
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    with open(from_path, "r", encoding="utf-8") as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)

    destination_directory = os.path.dirname(dest_path)

    if destination_directory:
        os.makedirs(destination_directory, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as output_file:
        output_file.write(page)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
) -> None:
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(source_path):
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
            )
            continue

        if not entry.endswith(".md"):
            continue

        destination_path = os.path.splitext(destination_path)[0] + ".html"

        generate_page(
            source_path,
            template_path,
            destination_path,
        )
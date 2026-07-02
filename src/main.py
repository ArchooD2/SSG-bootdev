import os
import shutil

from generate_page import generate_pages_recursive


def copy_directory(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination)
    copy_directory_contents(source, destination)


def copy_directory_contents(
    source: str,
    destination: str,
) -> None:
    for entry in os.listdir(source):
        source_path = os.path.join(source, entry)
        destination_path = os.path.join(destination, entry)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            print(f"Creating directory {destination_path}")
            os.makedirs(destination_path, exist_ok=True)
            copy_directory_contents(
                source_path,
                destination_path,
            )


def main() -> None:
    copy_directory("static", "public")

    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )


if __name__ == "__main__":
    main()
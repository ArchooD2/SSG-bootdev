from textnode import TextNode, TextType
def main():
    node = TextNode("Hello, world!", TextType.PLAIN)
    print(node)

if __name__ == "__main__":
    main()
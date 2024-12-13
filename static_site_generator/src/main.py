from src.textnode import TextNode
from src.textnode import TextType


def main() -> int:
    text_node = TextNode("This is text node",
                         TextType.ITALIC,
                         "www.test.com")
    print(text_node)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import pytest

from src.addapter import text_node_to_html_node
from src.textnode import TextType
from src.textnode import TextNode
from src.leafnode import LeafNode

VALID: list[tuple[str, TextType, str]] = [
    ("Normal text", TextType.NORMAL, ""),
    ("Bold text", TextType.BOLD, ""),
    ("Italic text", TextType.ITALIC, ""),
    ("Code text", TextType.CODE, ""),
    ("Url text", TextType.LINKS, "www.url.com"),
    ("Image text", TextType.IMAGES, "www.image.com"),

]
VALID_EXPECTED = [
    LeafNode(value="Normal text"),
    LeafNode(tag="b", value="Bold text"),
    LeafNode(tag="i", value="Italic text"),
    LeafNode(tag="code", value="Code text"),
    LeafNode(tag="a", value="Url text", props={"href": "www.url.com"}),
    LeafNode(tag="img", value="", props={"src": "www.image.com",
                                         "alt": "Image text"}),
]

Z_VALID = zip(VALID, VALID_EXPECTED)


@pytest.mark.parametrize("args", Z_VALID)
def test_valid(args):
    print(args)
    text, text_type, url = args[0]
    l1 = text_node_to_html_node(TextNode(text=text,
                                         text_type=text_type,
                                         url=url))
    expected_leaf = args[-1]
    assert l1 == expected_leaf, (f"Expected func to return"
                                 f" {expected_leaf}, got {l1}")


def test_invalid():
    with pytest.raises(TypeError):
        text_node_to_html_node(TextNode("test invalid",
                                        (1, 2),
                                        "www.dummy.com"))


def test_raises():
    with pytest.raises(TypeError, match="Cannon't convert None to HTMLNode."):
        text_node_to_html_node(None)

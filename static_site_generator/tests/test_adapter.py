import pytest

from src.adapter import text_node_to_html_node
from src.adapter import split_nodes_delimiter
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


def test_split_node():
    t1 = TextNode("This is text with a `code block` word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([t1], "`", TextType.CODE)
    assert len(new_nodes) == 3, ("Expected to get 3 new nodes,"
                                 f" got {len(new_nodes)}")
    assert new_nodes[0] == TextNode("This is text with a ", TextType.NORMAL)
    assert new_nodes[1] == TextNode("code block", TextType.CODE)
    assert new_nodes[2] == TextNode(" word", TextType.NORMAL)


def test_no_delimiter():
    t1 = TextNode("This is a text node with no delimiter", TextType.NORMAL)
    new_node = split_nodes_delimiter([t1], "*", TextType.BOLD)
    assert len(new_node) == 1, ("Expected len of new node to be 1,"
                                f" got {len(new_node)}")
    assert new_node[0] == t1, ("Expected old node and new node to be the same."
                               f"Old node is {t1}, new node is {new_node[0]}")


def test_only_one_delimiter():
    t1 = TextNode("This is text with a `code block word", TextType.NORMAL)
    new_node = split_nodes_delimiter([t1], "`", TextType.CODE)
    assert len(new_node) == 1, ("Expected len of new node to be 1,"
                                f" got {len(new_node)}")
    assert new_node[0] == t1, ("Expected old node and new node to be the same."
                               f"Old node is {t1}, new node is {new_node[0]}")


TEST_INPUT = [
    [TextNode("This is normal text with **bold** inside it", TextType.NORMAL),
     "**",
     TextType.BOLD],
    [TextNode("This is normal text with *italic* inside it", TextType.NORMAL),
     "*",
     TextType.ITALIC],
    [TextNode("This is normal text with `code` inside it", TextType.NORMAL),
     "`",
     TextType.CODE],
]
EXPECTED_NODES = [
    [TextNode("This is normal text with ", TextType.NORMAL),
     TextNode("bold", TextType.BOLD),
     TextNode(" inside it", TextType.NORMAL)],
    [TextNode("This is normal text with ", TextType.NORMAL),
     TextNode("italic", TextType.ITALIC),
     TextNode(" inside it", TextType.NORMAL)],
    [TextNode("This is normal text with ", TextType.NORMAL),
     TextNode("code", TextType.CODE),
     TextNode(" inside it", TextType.NORMAL)]
]
Z_TEST_INPUT = zip(TEST_INPUT, EXPECTED_NODES)


@pytest.mark.parametrize("t_input, expected",
                         Z_TEST_INPUT)
def test_split_nodes(t_input, expected):
    new_nodes = split_nodes_delimiter([t_input[0]], t_input[1], t_input[2])
    assert len(new_nodes) == 3, ("Expected to get 3 new nodes,"
                                 f" got {len(new_nodes)}")
    assert new_nodes[0] == expected[0], (f"Expected {expected[0]},"
                                         f" got {new_nodes[0]}")
    assert new_nodes[1] == expected[1], (f"Expected {expected[1]},"
                                         f" got {new_nodes[1]}")
    assert new_nodes[2] == expected[2], (f"Expected {expected[2]},"
                                         f" got {new_nodes[2]}")

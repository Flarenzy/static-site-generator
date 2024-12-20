import pytest

from src.adapter import split_nodes_delimiter
from src.adapter import text_node_to_html_node
from src.adapter import text_to_textnodes
from src.adapter import markdown_to_blocks
from src.leafnode import LeafNode
from src.textnode import TextNode
from src.textnode import TextType

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


def test_text_to_textnode():
    text = ("This is **text** with an *italic* word"
            " and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            " and a [link](https://boot.dev)")
    expected = [
        TextNode("This is ", TextType.NORMAL),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.NORMAL),
        TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL),
        TextNode("link", TextType.LINKS, "https://boot.dev"),
    ]
    res = text_to_textnodes(text)
    assert res == expected


INVALID_TEXT = (
    5,
    5.0,
    0x34,
)


@pytest.mark.parametrize("num", INVALID_TEXT)
def test_invalid_text_to_text_node(num):
    with pytest.raises(TypeError):
        text_to_textnodes(num)


@pytest.mark.parametrize("num", INVALID_TEXT)
def test_invalid_markdown_to_text(num):
    with pytest.raises(TypeError):
        markdown_to_blocks(num)


INPUT_FILES = (
    "tests/inputs/just_text.md",
    "tests/inputs/valid_markdown.md",
    "tests/inputs/empty.md",
    "tests/inputs/only_newlines.md",
)

EXPECTED_FOR_FILES = (
    ['[Tekst pesme "Dam, dam, dam"]\n',
     '[Uvod]\nDam, dam, dam\nDa-da-da-da-da-dam\nDa-da-dam, dam, dam\nDa-da-da-da-da-dam\n',
     '[Strofa 1]\nNemoj, ma nemoj meni priče ove\nSvi ste u ponoć Kazanove\nA sutra niko da pozove\nNemoj da nudiš to što nećeš moći\nNemoj da lažeš me u oči\nJako si krenuo, prikoči\n',
     '[Pred-Refren]\nLogično da si muško, da ti treba samo jedno\nLogično bićeš najveći gospodin dok se lomim\nLogično, tebi je logično, a meni toksično\n',
     '[Refren]\nLepi moj, piši broj\nGrešim cifre namerno\nA ti misliš to je to\nVeć nas vidiš zajedno\nA ja znam, noćas kući ideš sam\nI dok tvoju igru igram\nTvoja jedina je briga da ti dam\n'
     ],
    ['# This is a heading\n',
     'This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n',
     '* This is the first list item in a list block\n* This is a list item\n* This is another list item\n',
     '1. This is a numbered list\n2. The second item\n3. The third item also has something in it\n'
     ],
    [],
    [],
)

MARKDOWN_TO_TEXT = zip(INPUT_FILES, EXPECTED_FOR_FILES)


@pytest.mark.parametrize("markdown_file, expected", MARKDOWN_TO_TEXT)
def test_markdown_to_text(markdown_file, expected):
    with open(markdown_file, "r") as f:
        text = f.read()
    res = markdown_to_blocks(text)
    assert res == expected

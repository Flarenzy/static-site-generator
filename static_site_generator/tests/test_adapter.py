import pytest

from src.adapter import block_to_block_type
from src.adapter import split_nodes_delimiter
from src.adapter import is_code
from src.adapter import is_quote
from src.adapter import is_heading
from src.adapter import is_unordered_list
from src.adapter import is_ordered_list
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
    "tests/inputs/no_newline.md",
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
    ["This is a text without a newline."],
)

MARKDOWN_TO_TEXT = zip(INPUT_FILES, EXPECTED_FOR_FILES)


@pytest.mark.parametrize("markdown_file, expected", MARKDOWN_TO_TEXT)
def test_markdown_to_text(markdown_file, expected):
    with open(markdown_file, "r") as f:
        text = f.read()
    res = markdown_to_blocks(text)
    assert res == expected


NOT_BLOCK = (
    5,
    5.0,
    ["yes", "no", "maybe"],
    ("yes", "no", "maybe"),
    complex(1, 2)
)


@pytest.mark.parametrize("not_block", NOT_BLOCK)
def test_not_string_block_to_blocks(not_block):
    with pytest.raises(TypeError):
        block_to_block_type(not_block)


IS_HEADING = (
    "This is not a valid heading.",
    "This is also not a valid ## heading",
    "####NotAValidHeading",
    "######## Not a heading",
    "####1 Not a heading",
    "### ",
    "###   \n",
    "# Heading 1",
    "## Heading 2",
    "### Heading 3",
    "#### Heading 4",
    "##### Heading 5",
    "###### Heading 6",
)

EXPECTED_IS_HEADING = (
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
)

Z_IS_HEADING = zip(IS_HEADING, EXPECTED_IS_HEADING)


@pytest.mark.parametrize("args", Z_IS_HEADING)
def test_is_heading(args):
    assert is_heading(args[0]) == args[1]


IS_CODE = (
    "```",
    "```2``",
    "```This is valid code```",
    "```Some code block.```",
    "Just text",
    "### Heading"
)

EXPECTED_IS_CODE = (
    False,
    False,
    True,
    True,
    False,
    False,
)

Z_IS_CODE = zip(IS_CODE, EXPECTED_IS_CODE)


@pytest.mark.parametrize("args", Z_IS_CODE)
def test_is_code(args):
    assert is_code(args[0]) == args[1]


IS_QUOTE = (
    "This is not a quote.",
    "This is not a quote > lets say",
    ">>By our definition this is",
    "> Yes"
)

EXPECTED_IS_QUOTE = (
    False,
    False,
    True,
    True
)

Z_IS_QUOTE = zip(IS_QUOTE, EXPECTED_IS_QUOTE)


@pytest.mark.parametrize("args", Z_IS_QUOTE)
def test_is_quote(args):
    assert is_quote(args[0]) == args[1]


IS_UNORDERED = (
    "This is not a list",
    "** this is not ",
    "",
    "* This is\n* an list\n* of items\n",
    "- this is also\n- an list of items\n",
    "- this should be\n* true\n- like\n* so true",
    "1. This is an ordered list\n2. Not an unordered one."
    )

EXPECTED_IS_UNORDERED = (
    False,
    False,
    False,
    True,
    True,
    True,
    False,
)

Z_IS_UNORDERED = zip(IS_UNORDERED, EXPECTED_IS_UNORDERED)


@pytest.mark.parametrize("args", Z_IS_UNORDERED)
def test_is_unordered(args):
    assert is_unordered_list(args[0]) == args[1]


IS_ORDERED = (
    "Not a list.",
    "* Unordered list\n2. Lets check\n",
    "1. List with wrong numbers\n3. Three\n2. Two",
    "1. One\n2. Two\n3. Three"
)

EXPECTED_IS_ORDERED = (
    False,
    False,
    False,
    True
)

Z_IS_ORDERED = zip(IS_ORDERED, EXPECTED_IS_ORDERED)


@pytest.mark.parametrize("args", Z_IS_ORDERED)
def test_is_ordered(args):
    assert is_ordered_list(args[0]) == args[1]


BLOCK_TO_BLOCK_TYPE = (
    "\n\n",
    "# Heading 1",
    "## Heading 2",
    "### Heading 3",
    "#### Heading 4",
    "##### Heading 5",
    "###### Heading 6",
    "```A code block```",
    "> I always liked this quote",
    "* Some item\n- that can't\n* be named",
    "1. Item one\n2. Item two\n3. Item three."
    "This is just some random text * - ### > ``"
)

EXPECTED_BLOCK_TO_BLOCK_TYPE = (
    "paragraph",
    "heading",
    "heading",
    "heading",
    "heading",
    "heading",
    "heading",
    "code",
    "quote",
    "unordered_list",
    "ordered_list",
    "paragraph",
)

Z_BLOCK_TO_BLOCK_TYPE = zip(BLOCK_TO_BLOCK_TYPE, EXPECTED_BLOCK_TO_BLOCK_TYPE)


@pytest.mark.parametrize("args", Z_BLOCK_TO_BLOCK_TYPE)
def test_block_to_block_type(args):
    assert block_to_block_type(args[0]) == args[1]

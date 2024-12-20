import pytest

from src.extracter import extract_markdown_images
from src.extracter import extract_markdown_links
from src.extracter import split_nodes_image
from src.extracter import split_nodes_link
from src.textnode import TextNode
from src.textnode import TextType


def test_extract_links():
    t = ("This is text with a link [to boot dev](https://www.boot.dev)"
         " and [to youtube](https://www.youtube.com/@bootdotdev)")
    expected = [
        ("to boot dev", "https://www.boot.dev"),
        ("to youtube", "https://www.youtube.com/@bootdotdev")
    ]
    res = extract_markdown_links(t)
    assert len(res) == 2
    assert res == expected, (f"Expected: {expected}, "
                             f"got {res}")


def test_extract_images():
    t = ("This is text with a "
         "![rick roll](https://i.imgur.com/aKaOqIh.gif) "
         "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    expected = [
        ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
    res = extract_markdown_images(t)
    assert len(res) == 2
    assert res == expected, (f"Expected: {expected}, "
                             f"got {res}")


def test_empty():
    res_img = extract_markdown_images("")
    res_link = extract_markdown_links("")
    assert res_img == [], f"Expected empty list value got {res_img}"
    assert res_link == [], f"Expected empty list value got {res_link}"


def test_plain_text():
    t = ("This is a text with no link or ! [image] (in) it.")
    res_img = extract_markdown_images(t)
    res_link = extract_markdown_links(t)
    assert res_img == [], f"Expected empty list value got {res_img}"
    assert res_link == [], f"Expected empty list value got {res_link}"


_INVALID_INPUT = (
    ("This is an invalid", "input"),
    {"invalid": "input"},
    ["Invalid", "input", "list"],
    5,
    10.2,
)


@pytest.mark.parametrize("inp", _INVALID_INPUT)
def test_invalid_input_image(inp):
    with pytest.raises(TypeError, match=("expected string or "
                                         "bytes-like object, "
                                         f"got '{type(inp).__name__}'")):
        extract_markdown_images(inp)


@pytest.mark.parametrize("inp", _INVALID_INPUT)
def test_invalid_input_link(inp):
    with pytest.raises(TypeError, match=("expected string or "
                                         "bytes-like object, "
                                         f"got '{type(inp).__name__}'")):
        extract_markdown_links(inp)


_INPUT_SPLIT_IMAGE = [
    TextNode(("![image1](https://www.youtube.com/@bootdotdev) "
             "this test images at the begining."),
             TextType.NORMAL),
    TextNode(("This test's for links at the end "
              "![image2](https://www.youtube.com/@bootdotdev)."),
             TextType.NORMAL),
    TextNode("![image3](https://www.youtube.com/@bootdotdev)",
             TextType.NORMAL),
    TextNode(("This is text with a link [image4+1](https://www.boot.dev)"
              " and [image4+2](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL),
    TextNode(("This is text with a link [to boot dev](https://www.boot.dev)"
              " and ![image5](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL)
]

_EXPECTED_SPLIT_IMAGES = [
    TextNode("image1", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"),
    TextNode(" this test images at the begining.", TextType.NORMAL),
    TextNode("This test's for links at the end ", TextType.NORMAL),
    TextNode("image2", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"),
    TextNode(".", TextType.NORMAL),
    TextNode("image3", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"),
    TextNode(("This is text with a link [image4+1](https://www.boot.dev)"
             " and [image4+2](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL),
    TextNode(("This is text with a link [to boot dev](https://www.boot.dev)"
              " and "),
             TextType.NORMAL),
    TextNode("image5", TextType.IMAGES, "https://www.youtube.com/@bootdotdev")
]


def test_split_nodes_iamge():
    res = split_nodes_image(_INPUT_SPLIT_IMAGE)
    assert res == _EXPECTED_SPLIT_IMAGES, ("Expected: "
                                           f"{_EXPECTED_SPLIT_IMAGES},"
                                           f" got {res}")


_INPUT_SPLIT_LINK = [
    TextNode(("[link1](https://www.youtube.com/@bootdotdev) "
             "this test links at the begining."),
             TextType.NORMAL),
    TextNode(("This test's for links at the end "
              "[link2](https://www.youtube.com/@bootdotdev)."),
             TextType.NORMAL),
    TextNode("[link3](https://www.youtube.com/@bootdotdev)",
             TextType.NORMAL),
    TextNode(("This is text with a image ![link4+1](https://www.boot.dev)"
              " and ![link4+2](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL),
    TextNode(("This is text with a image ![to boot dev](https://www.boot.dev)"
              " and [link5](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL)
]

_EXPECTED_SPLIT_LINKS = [
    TextNode("link1", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
    TextNode(" this test links at the begining.", TextType.NORMAL),
    TextNode("This test's for links at the end ", TextType.NORMAL),
    TextNode("link2", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
    TextNode(".", TextType.NORMAL),
    TextNode("link3", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),
    TextNode(("This is text with a image ![link4+1](https://www.boot.dev)"
             " and ![link4+2](https://www.youtube.com/@bootdotdev)"),
             TextType.NORMAL),
    TextNode(("This is text with a image ![to boot dev](https://www.boot.dev)"
              " and "),
             TextType.NORMAL),
    TextNode("link5", TextType.LINKS, "https://www.youtube.com/@bootdotdev")
]


def test_split_nodes_link():
    res = split_nodes_link(_INPUT_SPLIT_LINK)
    assert res == _EXPECTED_SPLIT_LINKS, ("Expected: "
                                          f"{_EXPECTED_SPLIT_LINKS},\n"
                                          f" got:\n {res}")


def test_empty_split():
    assert [] == split_nodes_image([])
    assert [] == split_nodes_link([])

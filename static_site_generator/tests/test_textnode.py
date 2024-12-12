import pytest

from src.textnode import TextNode
from src.textnode import TextType


def test_TextNode_eq():
    t1 = TextNode("This is a test node!", TextType.ITALIC, "www.test.com")
    assert t1.text == "This is a test node!"
    assert t1.text_type == TextType.ITALIC
    assert t1.url == "www.test.com"
    assert t1 == TextNode("This is a test node!",
                          TextType.ITALIC,
                          "www.test.com")


@pytest.mark.parametrize("args, error_message",
                         [
                            (
                                (None, None),
                                "TextNode.__init__() missing 2 required \
                                positional arguments: 'text' and 'text_type'"
                                ),
                            (
                                (None, TextType.BOLD),
                                "TextNode.__init__() missing 1 required \
                                positional arguments: 'text'"
                            ),
                            (
                                ("Some valid string", None),
                                "TextNode.__init__() missing 1 required \
                                positional arguments: 'text_type'"
                            ),
                         ])
def test_empty_TextNode(args, error_message):
    with pytest.raises(TypeError) as te:
        t1 = TextNode(*args)
    assert str(te.value) == error_message


@pytest.mark.parametrize("text, text_type",
                         [
                             ("Bold text type exists!", TextType.BOLD),
                             ("Italic text type exists!", TextType.ITALIC),
                             ("Images text type exists!", TextType.IMAGES),
                             ("Code text type exists!", TextType.CODE),
                             ("Links text type exists!", TextType.LINKS),
                             ("Normal text type exists!", TextType.NORMAL),

                         ])
def test_TextTypes(text, text_type):
    assert TextNode(text=text, text_type=text_type).text_type == text_type

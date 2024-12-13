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
        TextNode(*args)
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


@pytest.mark.parametrize("cls, value",
                         [
                             (int, 5),
                             (str, "5"),
                             (float, 5.0),
                         ])
def test_invalid_compare(cls, value):
    with pytest.raises(TypeError, match=("Cannon't compare TextNode with "
                                         f"{cls.__name__}")):
        TextNode("This is my text", TextType.ITALIC) == cls(value)


@pytest.mark.parametrize("text, text_type, url",
                         [
                             (
                                 "Repr test 1",
                                 TextType.BOLD,
                                 ""
                             )
                         ])
def test_repr(text, text_type, url):
    t1 = TextNode(text=text, text_type=text_type, url=url)
    expected = f"TextNode({text}, {text_type.value}, {url})"
    r = repr(t1)
    assert r == expected, f"Expected:\n {expected}\n Got{r}"

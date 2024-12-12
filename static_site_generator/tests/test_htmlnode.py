import pytest

from src.htmlnode import HTMLNode
from src.htmlnode import HTML_ELEMENTS


@pytest.mark.parametrize("tag", HTML_ELEMENTS)
def test_valid_tags(tag):
    h1 = HTMLNode(tag=tag)
    assert h1.tag == tag


@pytest.mark.parametrize("tag", 
                         ("sfas", "boban", ">", "&", "*")
                         )
def test_invalid_tag_input(tag):
    with pytest.raises(ValueError) as ve:
        HTMLNode(tag=tag)
    assert str(ve.value) == f"Invalid HTML tag: {tag}"


@pytest.mark.parametrize("props, error_message", 
                         [
                             ({1: "something"},
                              "All keys and values in 'props' must be strings"
                              ),
                             ({("one", "one"): "yes"},
                              "All keys and values in 'props' must be strings"
                              ),
                             ({"valid": ["j", "l", ""]},
                              "All keys and values in 'props' must be strings"
                              ),
                             (["one", "two", "three"],
                              "'props' must be a dictionary, got list")
                         ])
def test_invalid_props_inpput(props, error_message):
    with pytest.raises((TypeError, ValueError)) as e:
        HTMLNode(props=props)
    assert str(e.value) == error_message


def test_empty_input():
    h1 = HTMLNode()
    assert h1.tag is None
    assert h1.value is None
    assert h1.children is None
    assert h1.props is None
    assert h1.props_to_html() == ""


@pytest.mark.parametrize("tag, value, props",
                         [
                             ("h1", "some random text",
                              {"href": "www.google.com", "class": "baseClass"}
                              ),
                             ("h2", "text is very good",
                              {"class": "not_a_class"}
                              )
                         ]
                         )
def test_repr(tag, value, props):
    h1 = HTMLNode(tag=tag, value=value, children=None, props=props)
    print(repr(h1))
    cmp_str = ""
    cmp_str += f"HTMLNode(tag={tag}, value={value}, "
    cmp_str += f"children=None, props={props})"
    assert repr(h1) == cmp_str

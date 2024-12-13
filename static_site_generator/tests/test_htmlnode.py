import pytest

from src.htmlnode import HTMLNode
from src.htmlnode import HTML_ELEMENTS


@pytest.mark.parametrize("tag", HTML_ELEMENTS)
def test_valid_tags(tag):
    h1 = HTMLNode(tag=tag, value="random value")
    assert h1.tag == tag


@pytest.mark.parametrize("tag", 
                         ("sfas", "boban", ">", "&", "*")
                         )
def test_invalid_tag_input(tag):
    with pytest.raises(ValueError) as ve:
        HTMLNode(tag=tag, value="random value")
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
        HTMLNode(tag="h1", props=props)
    assert str(e.value) == error_message


def test_empty_input():
    with pytest.raises(ValueError) as ve:
        HTMLNode()
    assert str(ve.value) == "HTMLNode must have either value or children."


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


def test_not_implemented():
    with pytest.raises(NotImplementedError):
        HTMLNode(value="some value").to_html()


def test_no_props_to_html():
    h1 = HTMLNode(value="no props to htmk")
    res = h1.props_to_html()
    assert res == "", f"Expected empty string got {res}"
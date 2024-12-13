import pytest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

PARENT_TAGS = ["div", "section", "div", "i", "a", "h1", "h2",
               "h3", "td", "tr"]
PARENT_TAGS = PARENT_TAGS[::-1]
PARENT_PROPS = [{"class": "container"},
                {"class": "section"},
                {"class": "para"},
                {"class": "italic"},
                {"href": "www.google.com"},
                None,
                None,
                None,
                None,
                {"class": "table"}
                ]
PARENT_PROPS = PARENT_PROPS[::-1]
RECURSION_ARGS = zip(PARENT_TAGS, PARENT_PROPS)


def test_deep_recursion():
    l1 = LeafNode("p", "The first leaf.")
    l2 = LeafNode("b", "The second leaf")
    current = ParentNode("div", children=[l1, l2])
    expected = ("<div class=\"container\"><section class=\"section\">"
                "<div class=\"para\">"
                "<i class=\"italic\"><a href=\"www.google.com\"><h1>"
                "<h2><h3><td>"
                "<tr class=\"table\"><div><p>The first leaf.</p>"
                "<b>The second leaf</b></div>"
                "</tr></td></h3></h2></h1></a></i></div></section></div>")
    for tag, prop in RECURSION_ARGS:
        current = ParentNode(tag=tag, children=[current], props=prop)
    assert current.to_html() == expected, (f"Got {current.to_html()}, "
                                           "but expected:\n {expected}")


def test_no_children():
    with pytest.raises(ValueError,
                       match="HTMLNode must have either value or children."):
        ParentNode("a", None)

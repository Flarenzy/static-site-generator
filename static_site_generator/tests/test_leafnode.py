import pytest

from src.leafnode import LeafNode


INPUT_TEST_CASES = [
    ("h1", "This is a header", None, {"class": "header", "color": "red"}, 
     False, None),
    ("h2", "This is an h2 header", "invalid input", None, True, TypeError),
    ("h3", "This is an h3 header", None, None, False, None),
    (None, None, None, None, True, ValueError),
]

TO_HTML_TEST_CASES = [
    (None, "Today is a good day", None, None,
     "Today is a good day"),
    ("a", "Click here!", None, {"href": "www.youtube.com", "class": "button"},
     "<a href=\"www.youtube.com\" class=\"button\">Click here!</a>"),
]


@pytest.mark.parametrize("tag, value, children, props, raises, err",
                         INPUT_TEST_CASES)
def test_input(tag, value, children, props, raises, err):
    if raises:
        with pytest.raises(err):
            LeafNode(tag, value, children, props)
    else:
        l1 = LeafNode(tag, value, children, props)
        assert l1.tag == tag
        assert l1.value == value
        assert l1.children == children
        assert l1.props == props


@pytest.mark.parametrize("tag, value, children, props, expected",
                         TO_HTML_TEST_CASES)
def test_to_html(tag, value, children, props, expected):
    l1 = LeafNode(tag, value, children, props)
    assert l1.to_html() == expected

from typing import Optional


HTML_ELEMENTS = (
    'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base',
    'bdi', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption',
    'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 
    'details',
    'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 
    'figcaption',
    'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head',
    'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 
    'label',
    'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav',
    'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'picture',
    'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 
    'section',
    'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary',
    'sup', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th',
    'thead',
    'time', 'title', 'tr', 'track', 'u', 'ul', 'var', 'video', 'wbr'
)


class HTMLNode:
    def __init__(self, tag: Optional[str] = None,
                 value: Optional[str] = None,
                 children: Optional[list['HTMLNode']] = None,
                 props: Optional[dict[str, str]] = None
                 ) -> None:
        if tag not in HTML_ELEMENTS and tag is not None:
            raise ValueError(f"Invalid HTML tag: {tag}")
        if props is not None and not isinstance(props, dict):
            raise TypeError(f"'props' must be a dictionary, "
                            f"got {type(props).__name__}")
        if props is not None:
            for k, v in props.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise TypeError("All keys and values in 'props' "
                                    "must be strings")
        if value is None and children is None:
            raise ValueError("HTMLNode must have either value or children.")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        props = [f"{k}=\"{self.props[k]}\"" for k in self.props]
        return " " + " ".join(props)

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
                f"children={self.children}, props={self.props})")

from typing import Optional

from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str] = None,
                 value: Optional[str] = None,
                 children: Optional[list['HTMLNode']] = None,
                 props: Optional[dict[str, str]] = None
                 ) -> None:
        if children is not None:
            raise TypeError("Leaf node cannot have children.")
        super().__init__(tag, value, children, props)

    def to_html(self) -> str:  # images can not have a value
        if self.value is None and self.tag != "img":
            print(f"Here is the problematic node {repr(self)}")
            raise ValueError("Value must be defined for all LeafNodes!")
        if not self.tag:
            return f"{self.value}"
        html = f"<{self.tag}>"
        if self.props:
            html = html.replace(">", self.props_to_html() + ">")
        html += self.value + f"</{self.tag}>"
        return html

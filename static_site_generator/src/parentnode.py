from typing import Optional
from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], 
                 props: Optional[dict[str, str]] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All ParentNode must have tags!")
        if not self.children:
            raise ValueError("All ParentNode must have children!")
        html = f"<{self.tag}>"
        if self.props:
            html = html.replace(">", self.props_to_html() + ">")
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

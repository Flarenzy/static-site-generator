from enum import Enum
from typing import Optional


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text: str, text_type: TextType,
                 url: Optional[str] = None) -> None:
        if text is None or text_type is None:
            raise TypeError("TextNode.__init__() missing 2 required \
                                positional arguments: 'text' and 'text_type'")
        if text_type not in TextType:
            raise TypeError("text_type must be an element"
                            " from the TextType enum.")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self: 'TextNode', other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self: 'TextNode') -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

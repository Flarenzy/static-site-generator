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
        if text is None and text_type is None:
            raise TypeError("TextNode.__init__() missing 2 required \
                                positional arguments: 'text' and 'text_type'")
        if text is None:
            raise TypeError("TextNode.__init__() missing 1 required \
                                positional arguments: 'text'")
        if text_type is None:
            raise TypeError("TextNode.__init__() missing 1 required \
                                positional arguments: 'text_type'")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: 'TextNode') -> bool:
        if not isinstance(other, TextNode):
            raise TypeError("Cannon't compare TextNode with "
                            f"{type(other).__name__}")
        return (self.text == other.text and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

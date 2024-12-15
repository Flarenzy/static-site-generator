from src.textnode import TextNode
from src.textnode import TextType
from src.leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not text_node:
        raise TypeError("Cannon't convert None to HTMLNode.")
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINKS:
            return LeafNode(tag="a",
                            value=text_node.text,
                            props={"href": text_node.url})
        case TextType.IMAGES:
            return LeafNode(tag="img", value="",
                            props={"src": text_node.url,
                                   "alt": text_node.text})
        case _:
            allowed = [tt.value for tt in TextType]
            raise TypeError(f"{text_node.text_type} "
                            f"must be one of {*allowed, }")


def split_nodes_delimiter(old_nodes: list[TextNode],
                          delimiter: str,
                          text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_node(node, delimiter, text_type))
    return new_nodes


def split_node(old_node: TextNode,
               delimiter: str,
               text_type: TextType) -> list[TextNode]:
    if delimiter not in old_node.text:
        return [old_node]
    lst = old_node.text.split(delimiter, maxsplit=2)
    if len(lst) != 3:
        return [old_node]
    new_nodes = [
        TextNode(lst[0], old_node.text_type, old_node.url),
        TextNode(lst[1], text_type, old_node.url),
        TextNode(lst[2], old_node.text_type, old_node.url)
    ]
    return new_nodes

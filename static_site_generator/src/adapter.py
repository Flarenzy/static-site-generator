from src.extracter import split_nodes_image
from src.extracter import split_nodes_link
from src.leafnode import LeafNode
from src.textnode import TextNode
from src.textnode import TextType
from src.parentnode import ParentNode
from src.parentnode import HTMLNode


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


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = ("`", "**", "*")
    text_type = (TextType.CODE, TextType.BOLD, TextType.ITALIC)
    inline = zip(delimiters, text_type)
    node = TextNode(text, TextType.NORMAL)
    nodes = [node]
    for delimiter, text_type in inline:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []
    blocks = []
    current_block = ""
    if "\n" not in markdown:
        return [markdown]
    print(markdown.split("\n"))
    for line in markdown.split("\n"):
        stripped = line.strip()
        if not stripped:
            if current_block:
                blocks.append(current_block)
                current_block = ""
            continue
        current_block += stripped + "\n"
    if current_block:  # in case there is no \n at the end
        blocks.append(current_block)
    return blocks


def is_heading(block: str) -> bool:
    if "#" not in block or not block.startswith("#") or " " not in block:
        return False
    parts = block.split()
    num_headings = parts[0].count("#")
    if not num_headings or num_headings > 6:
        return False
    if num_headings != len(parts[0]):
        return False
    if len(parts) < 2:
        return False
    return True


def is_code(block: str) -> bool:
    block = block.strip()
    return block.startswith("```") and block.endswith("```") \
        and len(block) >= 6


def is_quote(block: str) -> bool:
    return block.startswith(">")


def is_unordered_list(block: str) -> bool:
    block = block.strip()
    lines = block.split("\n")
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            return False
    return True


def is_ordered_list(block: str) -> bool:
    block = block.strip()
    i = 0
    lines = block.split("\n")
    for line in lines:
        i += 1
        if not line.startswith(f"{i}. "):
            return False
    return True


def block_to_block_type(block: str) -> str:
    if not isinstance(block, str):
        raise TypeError(f"Expected string, got {type(block).__name__}")
    if not block.strip():
        return "paragraph"
    if is_heading(block):
        return "heading"
    if is_code(block):
        return "code"
    if is_quote(block):
        return "quote"
    if is_unordered_list(block):
        return "unordered_list"
    if is_ordered_list(block):
        return "ordered_list"
    return "paragraph"


def block_type_to_html_tag(block: str, block_type: str) -> str | dict[str, str]:
    type_to_tag = {
        "paragraph": "p",
        "quote": "blockquote",
        "code": {"pre": "code"},
        "unordered_list": {"ul": "li"},
        "ordered_list": {"ol": "li"},
    }
    if block_type == "heading":
        num_heading = block.split()[0].count("#")
        return f"h{num_heading}"
    if block_type == "code":
        print("Hit")
    return type_to_tag[block_type]


def tag_to_htmlnode(tag: str | dict[str, str]) -> ParentNode:
    if isinstance(tag, str):
        return ParentNode(tag, [])
    if len(tag) != 1:
        raise ValueError("Dafaq")
    for k in tag:
        p1 = ParentNode(k, [ParentNode(tag[k], [])])
    return p1


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    new_nodes = []
    for node in nodes:
        new_nodes.append(text_node_to_html_node(node))
    return new_nodes


def remove_block_type(block: str, block_type: str) -> str:
    match block_type:
        case "paragraph":
            return block
        case "heading":
            return block.lstrip("#")
        case "quote":
            return block.lstrip(">")
        case "unordered_list":
            new_block = ""
            for line in block.split("\n"):
                new_block += line.lstrip("* ").lstrip("- ") + "\n"
            return new_block
        case "ordered_list":
            i = 1
            new_block = ""
            for line in block.split("\n"):
                new_block += line.lstrip(f"{i}.") + "\n"
                i += 1
            return new_block
        case "code":
            return block.strip().strip("```")
        case _:
            TypeError(f"Expected a block type got {block_type}")


def add_children(parent: ParentNode, children: list[HTMLNode]) -> ParentNode:
    new_parent = parent
    if not parent.children:
        new_parent.children = children
        return new_parent
    new_children = []
    for child in children:
        child.tag = parent.children[0].tag
        new_children.append(child)
    parent.children = new_children
    return new_parent


def markdown_to_html_node(text: str) -> ParentNode:
    blocks = markdown_to_blocks(text)
    root_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        html_tag = block_type_to_html_tag(block, block_type)
        block = remove_block_type(block, block_type)
        parent = tag_to_htmlnode(html_tag)
        children = []
        for line in block.split("\n"):
            if not line:
                continue
            children.extend(text_to_children(line))
        parent = add_children(parent, children)
        root_node.children.append(parent)
    return root_node

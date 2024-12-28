import re

from src.textnode import TextNode
from src.textnode import TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    if not text:
        return []
    regex = r"\!\[(.*?)\]\((.*?)\)"
    res = re.findall(regex, text)
    return res


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    if not text:
        return []
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"  # ?<! is syntax for the negative
    # lookbehind, by doing this we avoid matching images as links.
    res = re.findall(regex, text)
    return res


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    if not old_nodes:
        return []
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        for text, url in images:
            if f"![{text}]({url})" == node_text:
                new_nodes.append(TextNode(text, TextType.IMAGES, url))
                node_text = ""
                continue
            r = node_text.split(f"![{text}]({url})", maxsplit=1)
            if r[0]:
                new_nodes.append(TextNode(r[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.IMAGES, url))
            node_text = r[1]
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    if not old_nodes:
        return []
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        for text, url in links:
            if f"[{text}]({url})" == node_text:
                new_nodes.append(TextNode(text, TextType.LINKS, url))
                node_text = ""
                continue
            r = node_text.split(f"[{text}]({url})", maxsplit=1)
            if r[0]:  # the delimiter can be at the start of the text
                new_nodes.append(TextNode(r[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.LINKS, url))
            node_text = r[1]
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.NORMAL))
    return new_nodes


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise Exception("Missing title from markdown.")

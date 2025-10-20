import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(re.findall(re.escape(delimiter), node.text)) % 2 != 0:
            raise Exception("Error: invalid Markdown syntax found")
        parts = re.split(f"({re.escape(delimiter)})", node.text)
        is_inside = False

        for part in parts:
            if part == "" or part is None:
                continue  
            if part == delimiter:
                is_inside = not is_inside
            elif is_inside:
                new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        for alt_text, image_url in matches:
            pattern = f"!\\[{re.escape(alt_text)}\\]\\({re.escape(image_url)}\\)"
            parts = re.split(pattern, text, maxsplit=1)
            before = parts[0]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            text = parts[1] if len(parts) > 1 else ""

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for link_text, link_url in matches:
            pattern = f"\\[{re.escape(link_text)}\\]\\({re.escape(link_url)}\\)"
            parts = re.split(pattern, text, maxsplit=1)
            before = parts[0]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = parts[1] if len(parts) > 1 else ""

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes 

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

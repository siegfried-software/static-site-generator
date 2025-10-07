from enum import Enum 
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
 
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(self):
    match self.text_type:
        case TextType.TEXT:
            return LeafNode(None, self.text) 
        case TextType.BOLD:
            return LeafNode("b", self.text)
        case TextType.ITALIC:
            return LeafNode("i", self.text)
        case TextType.CODE:
            return LeafNode("code", self.text)
        case TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": self.url, "alt": self.text})
        case _:
            raise Exception("Error: text node cannot be coverted to html node")



from htmlnode import LeafNode, ParentNode


def convert_bold_text(text):
    # Remove the markdown syntax for bold
    content = text.strip("*")
    return LeafNode("b", content)


def convert_italic_text(text):
    # Remove the markdown syntax for italic
    content = text.strip("*")
    return LeafNode("i", content)


def convert_link_text(text):
    # Extract text and URL from the markdown link syntax
    parts = text.split("](")
    link_text = parts[0].strip("[")
    link_url = parts[1].strip(")")
    link_node = ParentNode("a", children=[LeafNode("text", link_text)])
    link_node.set_prop("href", link_url)
    return link_node


def create_html_node(block, block_type):
    if block_type.startswith("heading"):
        count_hashes = block.count("#", 0, block.index(" "))
        return ParentNode(
            f"h{count_hashes}", children=[LeafNode("text", block.strip("# ").strip())]
        )
    elif block_type == "code":
        code_content = block.strip("```")
        code_node = LeafNode("code", code_content)
        return ParentNode("pre", children=[code_node])
    elif block_type == "quote":
        quote_content = block.strip("> ")
        return ParentNode("blockquote", children=text_to_children(quote_content))
    elif block_type == "unordered_list":
        items = block.split("\n")
        list_items = [
            ParentNode("li", children=text_to_children(item.strip("*- ")))
            for item in items
            if item.strip()
        ]
        return ParentNode("ul", children=list_items)
    elif block_type == "ordered_list":
        items = block.split("\n")
        list_items = [
            ParentNode("li", children=text_to_children(item.split(" ", 1)[1]))
            for item in items
            if item.strip()
        ]
        return ParentNode("ol", children=list_items)
    elif block_type == "paragraph":
        return ParentNode("p", children=text_to_children(block))
    return ParentNode("p", children=text_to_children(block))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = create_html_node(block, block_type)
        html_children.append(html_node)

    parent_node = ParentNode("div", children=html_children)
    return parent_node

def text_to_children(text):
    children = []
    i = 0

    while i < len(text):
        if text[i : i + 2] == "**":  # Handle bold text
            end_bold = text.find("**", i + 2)
            if end_bold != -1:
                children.append(convert_bold_text(text[i : end_bold + 2]))
                i = end_bold + 2
            else:
                children.append(LeafNode("text", text[i:]))
                break
        elif text[i] == "*":  # Handle italic text
            end_italic = text.find("*", i + 1)
            if end_italic != -1:
                children.append(convert_italic_text(text[i : end_italic + 1]))
                i = end_italic + 1
            else:
                children.append(LeafNode("text", text[i:]))
                break
        elif text[i] == "[":  # Handle links
            end_link = text.find(")", i + 1)
            if end_link != -1:
                children.append(convert_link_text(text[i : end_link + 1]))
                i = end_link + 1
            else:
                children.append(LeafNode("text", text[i:]))
                break
        else:  # Handle normal text
            next_special = min(
                [
                    idx
                    for idx in [
                        text.find("**", i),
                        text.find("*", i),
                        text.find("[", i),
                    ]
                    if idx != -1
                ],
                default=len(text),
            )
            if next_special != i:
                children.append(LeafNode("text", text[i:next_special]))
                i = next_special
            else:
                i = next_special

        return children

def markdown_to_blocks(markdown):
    # A very simple markdown block splitter
    return markdown.split("\n\n")


def block_to_block_type(block):
    if block.startswith("### "):
        return "heading3"
    elif block.startswith("## "):
        return "heading2"
    elif block.startswith("# "):
        return "heading1"
    elif block.startswith("```"):
        return "code"
    elif block.startswith("> "):
        return "quote"
    elif block.startswith("* ") or block.startswith("- "):
        return "unordered_list"
    elif block[0].isdigit() and block[1:][:2] == ". ":
        return "ordered_list"
    else:
        return "paragraph"
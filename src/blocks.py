def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block).strip())

    return [block for block in blocks if block]


def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0].strip()

    if first_line.startswith("#"):
        count_hashes = 0
        for char in first_line:
            if char == "#":
                count_hashes += 1
            else:
                break
        if 1 <= count_hashes <= 6 and first_line[count_hashes] == " ":
            return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    if all(line.strip().startswith(">") for line in lines):
        return "quote"

    if all(
        line.strip().startswith(("*", "-")) and line.strip()[1] == " " for line in lines
    ):
        return "unordered_list"

    try:
        if all(
            line.strip().split(" ", 1)[0].rstrip(".").isdigit()
            and int(line.strip().split(" ", 1)[0].rstrip(".")) == i + 1
            for i, line in enumerate(lines)
        ):
            return "ordered_list"
    except (IndexError, ValueError):
        pass

    return "paragraph"

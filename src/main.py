import os
import shutil
from textnode import TextNode
from blocktohtml import markdown_to_html_node

print("Let's make this project properly!")

def clean_public_dir():
    public_dir = 'public'
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

def copy_static_files():
    static_dir = 'static'
    public_dir = 'public'
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

def generate_main_page():
    generate_page('content/index.md', 'template.html', 'public/index.html')


def extract_title(markdown):
    # Split the markdown content into lines
    lines = markdown.split('\n')
    # Iterate over each line
    for line in lines:
        # Check if the line starts with '# '
        if line.startswith('# '):
            # Strip the '# ' and any leading/trailing whitespace, and return
            return line.strip('# ').strip()
    # If no valid line is found, raise an exception
    raise ValueError("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Step 2: Read the markdown file
    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    
    # Step 3: Read the template file
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Step 4: Convert markdown to HTML
    # Assuming `markdown_to_html_node` and `.to_html()` are available
    html_node = markdown_to_html_node(markdown_content)  # This would depend on your markdown library
    html_content = html_node.to_html()
    
    # Step 5: Extract the title
    title = extract_title(markdown_content)
    
    # Step 6: Replace placeholders in the template
    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)

    # Step 7: Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final content to the destination file
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_content)
    
    print(f"Page generated successfully and written to {dest_path}")


def main():
    clean_public_dir()        # Step 1: Clean the public directory
    copy_static_files()       # Step 2: Copy static files
    generate_main_page()      # Step 3: Generate the main page


if __name__ == "__main__":
    main()

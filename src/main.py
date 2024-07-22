import os
import shutil
from textnode import TextNode
from blocktohtml import markdown_to_html_node

print("Let's make this project properly!")

def clean_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def copy_static_files(static_dir, public_dir):
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        print(f"Examining directory: {root}")  # Print current directory being examined
        for file_name in files:
            if file_name.endswith(".md"):
                from_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(from_path, dir_path_content)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')
                
                # Generate the page using the template
                print(f"Found markdown file: {from_path}, converting to: {dest_path}")  # Debugging statement
                generate_page(from_path, template_path, dest_path)


def main():
    static_dir = 'static'
    public_dir = 'public'
    content_dir = 'content'
    template_path = 'template.html'

    # Clean the public directory
    clean_dir(public_dir)
    
    # Copy static files to public directory
    copy_static_files(static_dir, public_dir)
    
    # Generate pages recursively for all markdown files in the content directory
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()
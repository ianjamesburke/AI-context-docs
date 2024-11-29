"""
A script for collecting all the python code in a project and writing it to a markdown file
for use in a LLM context window.

"""


import os

def collect_python_code(directory, output_file):
    current_file = os.path.basename(__file__)
    with open(output_file, 'w') as md_file:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and file != current_file:
                    file_path = os.path.join(root, file)
                    md_file.write(f'# {file}\n\n')
                    with open(file_path, 'r') as py_file:
                        code = py_file.read()
                        md_file.write('```python\n')
                        md_file.write(code)
                        md_file.write('\n```\n\n')

if __name__ == "__main__":
    project_directory = '/Users/ianburke/Documents/GitHub/temp'  # Replace with your project directory
    output_markdown_file = '/Users/ianburke/Documents/GitHub/temp/collected_code.md'
    collect_python_code(project_directory, output_markdown_file)

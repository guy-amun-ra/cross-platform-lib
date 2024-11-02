import sys
import os
import shutil

if len(sys.argv) != 4:
    print('Usage: python rename_project.py <current_name> <new_name> "<Author Name>"')
    sys.exit(1)

current_name = sys.argv[1]
new_name = sys.argv[2]
author_name = sys.argv[3]

# Update CMakeLists.txt
cmake_file_path = 'CMakeLists.txt'
if os.path.exists(cmake_file_path):
    with open(cmake_file_path, 'r') as file:
        data = file.read()
    data = data.replace(current_name, new_name)
    with open(cmake_file_path, 'w') as file:
        file.write(data)

# Update README.md
readme_file_path = 'README.md'
if os.path.exists(readme_file_path):
    with open(readme_file_path, 'r') as file:
        data = file.read()
    data = data.replace(current_name, new_name)
    with open(readme_file_path, 'w') as file:
        file.write(data)

# Update the author name
license_file_path = 'LICENSE'
if os.path.exists(license_file_path):
    with open(license_file_path, 'r') as file:
        data = file.read()
    data = data.replace('[Author Name]', author_name)
    with open(license_file_path, 'w') as file:
        file.write(data)

print(f'Project renamed from {current_name} to {new_name} and author set to {author_name}.')


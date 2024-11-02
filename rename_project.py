import sys
import os
import re

if len(sys.argv) != 4:
    print('Usage: python rename_project.py <current_name> <new_name> "<Author Name>"')
    sys.exit(1)

current_name = sys.argv[1]
new_name = sys.argv[2]
author_name = sys.argv[3]

def replace_in_file(file_path, old_string, new_string):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        data = data.replace(old_string, new_string)
        with open(file_path, 'w') as file:
            file.write(data)

def replace_all_variations(file_path, current_name, new_name):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        
        # Replace hyphenated version
        data = data.replace(current_name, new_name)
        
        # Replace underscore version
        current_name_underscore = current_name.replace('-', '_')
        new_name_underscore = new_name.replace('-', '_')
        data = data.replace(current_name_underscore, new_name_underscore)
        
        # Replace uppercase version
        data = data.replace(current_name.upper(), new_name.upper())
        data = data.replace(current_name_underscore.upper(), new_name_underscore.upper())
        
        with open(file_path, 'w') as file:
            file.write(data)

# Update CMakeLists.txt
replace_all_variations('CMakeLists.txt', current_name, new_name)

# Update README.md
replace_all_variations('README.md', current_name, new_name)

# Update the author name in LICENSE
replace_in_file('LICENSE', '[Author Name]', author_name)

# Update header and source files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.h', '.c')):
            file_path = os.path.join(root, file)
            replace_all_variations(file_path, current_name, new_name)

print(f'Project renamed from {current_name} to {new_name} and author set to {author_name}.')
print('All files updated with new project name variations.')
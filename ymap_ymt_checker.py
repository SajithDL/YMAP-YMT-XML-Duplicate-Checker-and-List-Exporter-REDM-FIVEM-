import os
import xml.etree.ElementTree as ET
from collections import Counter

# Set the directory where your XML files are
base_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output')
output_file = os.path.join(output_dir, 'output.xml')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# This will hold the name of each item across all files, without duplicates
global_item_names = set()

# This dictionary will hold the information for each file
file_info = {}

# Read each file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.xml'):
        file_path = os.path.join(input_dir, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract the name of the file (without the '.xml' part)
        file_name = filename[:-4]

        # Initialize counters for this file
        item_names = []
        file_info[file_name] = {
            "item_count": 0,
            "duplicate": 0,
            "item_counts": Counter()  # Initialize the Counter for item counts
        }

        # Iterate through each 'Item' in the file
        for item in root.findall('.//Item'):
            archetype_name = item.find('archetypeName').text if item.find('archetypeName') is not None else ''
            item_names.append(archetype_name)
            global_item_names.add(archetype_name)

        # Count the items and duplicates
        item_counter = Counter(item_names)
        file_info[file_name]["item_count"] = len(item_names)
        file_info[file_name]["duplicate"] = sum([count - 1 for count in item_counter.values() if count > 1])
        file_info[file_name]["item_counts"] = item_counter

# Count of all unique item names
unique_item_count = len(global_item_names)

# Write and print the information
with open(output_file, 'w') as file:
    for file_name, info in file_info.items():
        # Prepare the duplicates string with counts
        duplicates_str = ", ".join(f'{item} ({count - 1})' for item, count in info['item_counts'].items() if count > 1)

        output = (
            f'<!--{file_name}-->\n'
            f'  Item Count: {info["item_count"]}\n'
            f'  Duplicate Count: {info["duplicate"]}\n'
            f'  Duplicates: {duplicates_str}\n\n'
        )
        print(output)
        file.write(output)

    # Write and print the global unique item names and their count
    unique_items_output = (
        f'\n     <!--All Unique Item Names:--> ({unique_item_count})\n' +
        '\n'.join(global_item_names) 
        
    )
    print(unique_items_output)
    file.write(unique_items_output)

print('Processing complete. Check the output file for the results.')

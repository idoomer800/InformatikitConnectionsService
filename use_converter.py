from tnsnames_converter import TNSParser
import json

# Read your file
with open('tnsnames.ora', 'r') as file:
    tns_content = file.read()

# 1. Convert to Array of Dictionaries
parsed_array = TNSParser.tns_to_dicts(tns_content)

# View the dictionary structure
print(json.dumps(parsed_array, indent=2))

# 2. Convert back to tnsnames.ora format
new_tns_content = TNSParser.dicts_to_tns(parsed_array)

# Save to a new file
with open('new_tnsnames.ora', 'w') as file:
    file.write(new_tns_content)
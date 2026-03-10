import re

class TNSParser:
    @staticmethod
    def tns_to_dicts(tns_text):
        # 1. Strip comments
        tns_text = re.sub(r'(?m)#.*$', '', tns_text)
        
        # 2. Tokenize: Extract parentheses, equals signs, and strings
        tokens = re.findall(r'\(|\)|=|"[^"]*"|[^\s()=]+', tns_text)
        
        # 3. Group tokens into nested lists based on parentheses
        stack = [[]]
        for token in tokens:
            if token == '(':
                new_list = []
                stack[-1].append(new_list)
                stack.append(new_list)
            elif token == ')':
                if len(stack) > 1:
                    stack.pop()
            else:
                stack[-1].append(token)
        
        nested_list = stack[0]
        
        # 4. Helper to recursively turn nested lists into dictionaries
        def parse_node(node):
            if not isinstance(node, list) or len(node) < 3 or node[1] != '=':
                return {}
            
            key = node[0]
            val_items = node[2:]
            
            # Simple string value (e.g., PROTOCOL = TCP)
            if len(val_items) == 1 and isinstance(val_items[0], str):
                return {key: val_items[0]}
                
            # Complex block (e.g., DESCRIPTION = (...))
            sub_dict = {}
            for child in val_items:
                if isinstance(child, list):
                    child_dict = parse_node(child)
                    for k, v in child_dict.items():
                        # If key already exists (like multiple ADDRESS blocks), turn it into an array
                        if k in sub_dict:
                            if not isinstance(sub_dict[k], list):
                                sub_dict[k] = [sub_dict[k]]
                            sub_dict[k].append(v)
                        else:
                            sub_dict[k] = v
            return {key: sub_dict}

        # 5. Extract top-level connection blocks
        connections = []
        i = 0
        while i < len(nested_list):
            # A valid block looks like: ALIAS = [...]
            if i + 2 < len(nested_list) and nested_list[i+1] == '=' and isinstance(nested_list[i+2], list):
                connections.append({
                    "name": nested_list[i],
                    "config": parse_node(nested_list[i+2])
                })
                i += 3
            else:
                i += 1 # Naturally skips garbage headers like "LAST_CHANGE: ORIR"
                
        return connections

    @staticmethod
    def dicts_to_tns(connections):
        def format_node(key, val, indent=0):
            spaces = "  " * indent
            # Standard string property
            if isinstance(val, str):
                return f"{spaces}({key} = {val})"
            
            # Nested dictionary block
            if isinstance(val, dict):
                lines = [f"{spaces}({key} ="]
                for k, v in val.items():
                    if isinstance(v, list):
                        # Handle duplicate keys (e.g., array of ADDRESS blocks)
                        for item in v:
                            lines.append(format_node(k, item, indent + 1))
                    else:
                        lines.append(format_node(k, v, indent + 1))
                lines.append(f"{spaces})")
                return "\n".join(lines)
            return ""

        output = []
        for conn in connections:
            alias = conn["name"]
            config = conn["config"]
            
            conn_lines = [f"{alias} ="]
            for k, v in config.items():
                conn_lines.append(format_node(k, v, indent=1))
            output.append("\n".join(conn_lines))
            
        return "\n\n".join(output)
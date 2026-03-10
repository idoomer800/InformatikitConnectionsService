import requests
import os
from tnsnames_converter import TNSParser
from odbc_converter import odbc_to_dict, dict_to_odbc

# WebDAV Configuration
WEBDAV_URL = "http://webdav:80"  # 'webdav' resolves to the Nginx service in Docker
AUTH = ('informatikit', 'password')

PATHS = {
    'tns': "/oracle/network/admin/tnsnames.ora",
    'odbc': "/odbc/odbc.ini"
}

TEMP_ODBC_FILE = "/tmp/temp_odbc.ini"

def _get_file(conn_type: str) -> str:
    """Fetches the configuration file from WebDAV."""
    url = f"{WEBDAV_URL}{PATHS[conn_type]}"
    response = requests.get(url, auth=AUTH)
    response.raise_for_status()
    return response.text

def _put_file(conn_type: str, content: str):
    """Uploads the updated configuration file to WebDAV."""
    url = f"{WEBDAV_URL}{PATHS[conn_type]}"
    response = requests.put(url, auth=AUTH, data=content.encode('utf-8'))
    response.raise_for_status()

def add_connection(conn_type: str, conn_name: str, details: dict) -> bool:
    """Adds a new connection to the specified config file."""
    if conn_type == 'tns':
        content = _get_file('tns')
        parsed = TNSParser.tns_to_dicts(content)
        
        if any(c['name'] == conn_name for c in parsed):
            print(f"[-] TNS connection '{conn_name}' already exists.")
            return False
            
        parsed.append({"name": conn_name, "config": details})
        _put_file('tns', TNSParser.dicts_to_tns(parsed))
        print(f"[+] Successfully added TNS connection: {conn_name}")
        return True

    elif conn_type == 'odbc':
        content = _get_file('odbc')
        with open(TEMP_ODBC_FILE, "w", encoding="utf-8") as f: f.write(content)
        
        parsed = odbc_to_dict(TEMP_ODBC_FILE)
        if conn_name in parsed:
            print(f"[-] ODBC connection '{conn_name}' already exists.")
            return False
            
        parsed[conn_name] = details
        dict_to_odbc(parsed, TEMP_ODBC_FILE)
        
        with open(TEMP_ODBC_FILE, "r", encoding="utf-8") as f: new_content = f.read()
        _put_file('odbc', new_content)
        print(f"[+] Successfully added ODBC connection: {conn_name}")
        return True

def edit_connection(conn_type: str, conn_name: str, details: dict) -> bool:
    """Edits an existing connection in the specified config file."""
    if conn_type == 'tns':
        content = _get_file('tns')
        parsed = TNSParser.tns_to_dicts(content)
        
        found = False
        for c in parsed:
            if c['name'] == conn_name:
                c['config'] = details
                found = True
                break
                
        if not found:
            print(f"[-] TNS connection '{conn_name}' not found.")
            return False
            
        _put_file('tns', TNSParser.dicts_to_tns(parsed))
        print(f"[*] Successfully edited TNS connection: {conn_name}")
        return True

    elif conn_type == 'odbc':
        content = _get_file('odbc')
        with open(TEMP_ODBC_FILE, "w", encoding="utf-8") as f: f.write(content)
        
        parsed = odbc_to_dict(TEMP_ODBC_FILE)
        if conn_name not in parsed:
            print(f"[-] ODBC connection '{conn_name}' not found.")
            return False
            
        parsed[conn_name] = details
        dict_to_odbc(parsed, TEMP_ODBC_FILE)
        
        with open(TEMP_ODBC_FILE, "r", encoding="utf-8") as f: new_content = f.read()
        _put_file('odbc', new_content)
        print(f"[*] Successfully edited ODBC connection: {conn_name}")
        return True

def delete_connection(conn_type: str, conn_name: str) -> bool:
    """Deletes an existing connection from the specified config file."""
    if conn_type == 'tns':
        content = _get_file('tns')
        parsed = TNSParser.tns_to_dicts(content)
        initial_len = len(parsed)
        
        parsed = [c for c in parsed if c['name'] != conn_name]
        if len(parsed) == initial_len:
            print(f"[-] TNS connection '{conn_name}' not found.")
            return False
            
        _put_file('tns', TNSParser.dicts_to_tns(parsed))
        print(f"[-] Successfully deleted TNS connection: {conn_name}")
        return True

    elif conn_type == 'odbc':
        content = _get_file('odbc')
        with open(TEMP_ODBC_FILE, "w", encoding="utf-8") as f: f.write(content)
        
        parsed = odbc_to_dict(TEMP_ODBC_FILE)
        if conn_name not in parsed:
            print(f"[-] ODBC connection '{conn_name}' not found.")
            return False
            
        del parsed[conn_name]
        dict_to_odbc(parsed, TEMP_ODBC_FILE)
        
        with open(TEMP_ODBC_FILE, "r", encoding="utf-8") as f: new_content = f.read()
        _put_file('odbc', new_content)
        print(f"[-] Successfully deleted ODBC connection: {conn_name}")
        return True
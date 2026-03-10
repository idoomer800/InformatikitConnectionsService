from manager import add_connection, edit_connection, delete_connection, _get_file
import time

def print_file_states(step_name: str):
    """Helper function to print the current state of both files."""
    print(f"\n{'='*20} FILE STATES AFTER {step_name} {'='*20}")
    print("\n--- TNSNAMES.ORA ---")
    print(_get_file('tns'))
    print("\n--- ODBC.INI ---")
    print(_get_file('odbc'))
    print("="*60 + "\n")

def run_tests():
    print("="*50)
    print("🚀 STARTING CONNECTION MANAGER TESTS")
    print("="*50)

    # 1. ADD MOCK DATA
    print("\n>>> TESTING: ADD")
    tns_details = {
        "DESCRIPTION": {
            "ADDRESS": {"PROTOCOL": "TCP", "HOST": "mock-db.local", "PORT": "1521"},
            "CONNECT_DATA": {"SERVICE_NAME": "mock_service"}
        }
    }
    add_connection('tns', 'MOCK_TNS_DB', tns_details)

    odbc_details = {
        "Driver": "/usr/lib/odbc/mock.so",
        "Description": "Mock ODBC Database",
        "Servername": "mock.local",
        "Port": "5432",
        "Database": "mock_db"
    }
    add_connection('odbc', 'MOCK_ODBC_DB', odbc_details)
    
    time.sleep(1) # Small pause to let visual logs breathe
    print_file_states("ADD")

    # 2. EDIT MOCK DATA
    print("\n>>> TESTING: EDIT")
    # Change TNS Port
    tns_details["DESCRIPTION"]["ADDRESS"]["PORT"] = "1522" 
    edit_connection('tns', 'MOCK_TNS_DB', tns_details)

    # Change ODBC Port
    odbc_details["Port"] = "5433" 
    edit_connection('odbc', 'MOCK_ODBC_DB', odbc_details)

    time.sleep(1)
    print_file_states("EDIT")

    # 3. DELETE MOCK DATA
    print("\n>>> TESTING: DELETE")
    delete_connection('tns', 'MOCK_TNS_DB')
    delete_connection('odbc', 'MOCK_ODBC_DB')

    time.sleep(1)
    print_file_states("DELETE")

    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*50)

if __name__ == "__main__":
    run_tests()
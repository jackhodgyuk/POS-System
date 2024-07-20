# manager_codes.py

# Dictionary to store manager usernames and their respective passcodes
MANAGER_CODES = {
    'manager1': '2676555',
    'manager2': '1234567',
    'manager3': '7654321'
}

def is_valid_manager(username, passcode):
    """
    Validate if the provided username and passcode belong to a manager.
    
    Args:
    username (str): The manager's username.
    passcode (str): The manager's passcode.
    
    Returns:
    bool: True if valid manager, False otherwise.
    """
    return MANAGER_CODES.get(username) == passcode


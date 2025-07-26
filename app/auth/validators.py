import re

def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, ""

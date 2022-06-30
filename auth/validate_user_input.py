import re


def check_empty(input):
    if input == None or input == "":
        return True
    
    return False


def validate_email(email):
    if check_empty(email):
        return "Please enter a non-empty email"

    return None


def check_user_and_pass(username, password):
    if check_empty(username):
        return "Please enter a non-empty username"
    
    if check_empty(password):
        return "Please enter a non-empty password"


def validate_username(username):
    """
    Checks to see whether username
    follows good guidelines.
    """
    if check_empty(username):
        return "Please enter a non-empty username"
    
    return None


def validate_password(password):
    """
    Checks to see whether password
    follows good guidelines.
    """
    if check_empty(password):
        return "Please enter a non-empty password"
    
    if len(password) < 8 or len(password) > 30:
        return "Please enter a password of 8-30 characters"

    if bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', password))==False:
        return "Please use at least one lowercase letter, uppercase letter, digit, and special character"
    
    return None
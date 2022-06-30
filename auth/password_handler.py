"""
Python script that generates and
validates password hashes and salts.
"""

from passlib.context import CryptContext


def get_default_config():
    """
    Returns the default context
    for crytographic hashing of
    passwords.
    """
    context = CryptContext(schemes=['pbkdf2_sha256'], default='pbkdf2_sha256', pbkdf2_sha256__default_rounds=200000)

    return context


def generate_key(pwd):
    """
    Generates a key from
    a password (pwd) and salt
    with a certain number of
    iterations (default 100,000).
    """
    # generates hash
    context = get_default_config()

    return context.hash(pwd)


def validate_key(pwd, hash):
    """
    Validates a plaintext password (pwd) and
    salt against the actual key/hash.
    """
    # verifies hash with password
    context = get_default_config()

    return context.verify(pwd, hash)

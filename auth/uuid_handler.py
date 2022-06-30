"""
Python script intended to handle
UUID v4 and v5 generation.
"""


import uuid


def generate_uuid_v4():
    """
    Generates and returns
    a random V4 UUID.
    """
    return uuid.uuid4()


def generate_uuid_v5(namespace, name):
    """
    Generates and returns
    a V5 UUID, given a uuid namespace
    and a string name.
    """
    return uuid.uuid5(namespace, name)


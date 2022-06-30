"""
Python script intended to handle
parsing of strings relating to
file tree structures.
"""

from pathlib import Path
import platform

import venv
import configparser
import subprocess
from os.path import expanduser


OBJECT_SEP = "|--*:*--|"
HOME_FLAG = "#!#HOME#!#"


def validate_lists(list):
    """
    Ensures that lists have
    valid values.
    """
    if list == None:
        return False

    if len(list) == 0:
        return False
    
    return True


def parse_directory(path):
    """
    Given a path, return a list of
    all directories and subdirectories,
    and also return a list with
    all files and subfiles.
    """
    objects_list = []

    p = Path(path)
    
    for child in p.glob('**/*'):
        objects_list.append("{}{}{}".format(child.is_file(), OBJECT_SEP, child))

    return objects_list


def create_objects_section(objects_list):
    """
    Creates a string representing
    a config section for a list of
    files and directories (objects).
    """

    if validate_lists(objects_list) == False:
        return ""

    files_str = """
    [objects]
    objects_list={}
    """.format(",".join(objects_list))

    return files_str


def create_packages_section(packages):
    """
    Creates a string representing a
    config section for a list of
    packages.
    """
    if validate_lists(packages) == False:
        return ""

    packages_str = """
    [packages]
    packages_list={}
    """.format(",".join(packages))

    return packages_str


def create_config(objects_list, package_list):
    """
    Creates a config file content string
    from a directory list and a file
    list.
    """

    o_str = create_objects_section(objects_list)
    p_str = create_packages_section(package_list)

    return "\n".join([o_str, p_str])


def parse_config(str):
    """
    Obtains and returns a list of directories and objects
    and a list of packages from a config file styled
    string 'str'.
    """

    parser = configparser.ConfigParser()
    parser.read_string(str)

    if parser.has_section('objects') == False:
        obj_list = []
    else:
        # get list of directories
        obj_str = parser['objects']['objects_list']
        obj_list = [s.strip() for s in obj_str.split(",")]
    
    if parser.has_section('packages') == False:
        packages_list = []
    else:
        # get list of files
        packages_str = parser['packages']['packages_list']
        packages_list = [s.strip() for s in packages_str.split(",")]
    
    return {'objects': obj_list, 'packages': packages_list}


def populate_project(root, objects):
    """
    Populates project with files
    and directories.
    """
    if root.__contains__(HOME_FLAG):
        root = root.replace(HOME_FLAG, expanduser('~'))

    # ensures root folder exists
    root = Path(root)

    if root.exists() == False:
        root.mkdir()
    
    for object in objects:
        # obtains is_file flag (True = file)
        # and path of the object
        check, path = object.split(OBJECT_SEP)
        path = Path(path)

        # makes either file or directory
        if check == "True":
            with root.joinpath(path).open("w", encoding='utf-8'): pass
        else:
            root.joinpath(path).mkdir(parents=True, exist_ok=True)


def make_environment(venv_path, packages):
    # ensures that any home directory is properly
    # referenced
    if venv_path.__contains__(HOME_FLAG):
        venv_path = venv_path.replace(HOME_FLAG, expanduser('~'))
    
    # creates environment with venv_path and installs packages
    venv.create(venv_path, with_pip=True, upgrade_deps=True)

    folder = 'bin'

    if platform.system() == 'Windows':
        folder = 'Scripts'
    
    subprocess.call(['{}/{}/pip'.format(venv_path, folder), "install", *packages])


def create_project(root, venv_path, config_str, make_folders=True, make_env=True):
    """
    Makes a project with files and directories
    and/or packages.
    """
    # get directories/files and packages
    data_dict = parse_config(config_str)

    # makes files and directories
    if make_folders == True:
        populate_project(root, data_dict['objects'])

    # makes environment and packages
    if make_env == True:
        make_environment(venv_path, data_dict['packages'])


def make_config_file(name, config_str):
    """
    Turn config string into .ini file.
    """
    with open("{}.ini".format(name), mode="w", encoding="utf-8") as file:
        file.write(config_str)


def parse_config_file(file_name):
    """
    Read config file and convert contents to config string.
    """
    with open(file_name, encoding='utf-8') as file:
        config_str = file.read()

    return config_str

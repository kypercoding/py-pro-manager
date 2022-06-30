import tkinter as tk
from tkinter import filedialog

from parsers import parser as ps
from parsers.parser import HOME_FLAG


FILE_DIALOG = "#!#OPEN#!#"


main_prompt = """
NOTES:
-- If you want to use a file dialog
to choose a file or project folder,
then type "{}" whenever you
want to use the file dialog.
-- If you want to specify the
home directory, please use the
following: "{}", so that the
home directory is properly registered.
-- Type in "." for current directory.
-- Leave the desired project path empty
if you don't want to make a project.
-- Leave the desired environment path empty
if you don't want to make an environment.
-- Leave the config file path empty to
quit completely.

""".format(FILE_DIALOG, HOME_FLAG)


def get_path_from_dialog(get_folder=True):
    root = tk.Tk()
    root.withdraw()

    if get_folder == True:
        object_selected = filedialog.askdirectory()
    else:
        object_selected = filedialog.askopenfilename()
    
    if object_selected == None or len(object_selected) == 0:
        input("Please make sure to select a folder or file next time! Press ENTER to confirm.")
        exit(1)

    return object_selected


def main():
    print(main_prompt)

    # obtains config file path
    config_path = input("Please enter path of config file: ")

    if config_path == "#!#OPEN#!#":
        config_path = get_path_from_dialog(get_folder=False)

    if config_path == "":
        return

    # obtains project path
    path = input("Please enter desired path of project: ")

    if path == "#!#OPEN#!#":
        path = get_path_from_dialog()

    make_project = True
    if path == "":
        make_project = False

    # obtains virtual environment path
    venv_path = input("Please enter desired virtual environment path: ")

    if venv_path == "#!#OPEN#!#":
        venv_path = get_path_from_dialog()

    make_venv = True
    if venv_path == "":
        make_venv = False
    
    # makes projects and/or makes virtual environment
    config_str = ps.parse_config_file(config_path)
    ps.create_project(path, venv_path, config_str, make_project, make_venv)


if __name__ == "__main__":
    main()

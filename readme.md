# Python Project Manager

## Overview
Python Project Manager is a simple web application that allows users to store replicable templates for Python projects. The app gives users the ability to define file and directory structures for their apps as well as listing any necessary Python packages they would need for the project.

For example, a Python developer may define a Flask project with the following template:

```
|-- database
|---- __init__.py
|---- database.py
|-- backend
|---- __init__.py
|---- backend.py
|-- static
|-- templates
|-- server.py
|-- .gitignore
```

The web application saves this file tree configuration and gives developers the ability to download
the template, as well as define any Python packages necessary for the project.

## Installation

### Web Application:
The web application can be accessed in the following link: {LINK}

To launch the web application locally, here are some steps:
* Install Python 3.X.
* Install the necessary packages outlined in requirements.txt.
* Install current version of PostgreSQL and PostgreSQL Server.
* Run "python server.py -h" to get a list of necessary arguments, such as host, database name, user, and port.
* Provide the PostgreSQL password.
* The local Flask server should now be running.

### main.py:
In order to utilize the ability to generate local templates, the Python script ```main.py``` must be downloaded.
Users of Linux distributions (i.e. Ubuntu) may find it necessary to install tkinter for Python as well.

## Usage - Web Application


## Usage - main.py
In order to run the ```main.py``` script, simply call the script like you would any other Python script:

```python main.py```

The tool will now present you with the following prompt:
```
NOTES:
-- If you want to use a file dialog
to choose a file or project folder,
then type "#!#OPEN#!#" whenever you
want to use the file dialog.
-- If you want to specify the
home directory, please use the
following: "#!#HOME#!#", so that the
home directory is properly registered.
-- Type in "." for current directory.
-- Leave the desired project path empty
if you don't want to make a project.
-- Leave the desired environment path empty
if you don't want to make an environment.
-- Leave the config file path empty to
quit completely.

Do you want to build from the config file in the current directory (Y/N)?
```

If you answer 'Y' or 'y', the program will attempt to find a singular config file
(usually the name of your project appended with ".txt") to build your project from.

It will then ask:

```

```


## About
This web application is built using a three-tier stack: **HTML/CSS/JavaScript**, with some **jQuery/Ajax**; **Flask**,
a lightweight web application framework; and **PostgreSQL**, a relational database management system.
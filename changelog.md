# Version 0.0.2

## Features
* Validation functions ensuring that a user does not
have the ability to enter empty input values for
username, email and password for login/registration.

## Changes

### server.py:
* Removed password as command line argument, changed so that password
is required to be inputted after command line.

### main.py:
* Moved all parsers.parser functions to main.py so that the functions need not be separately packaged.
* Renamed main.py to build-template.py (to avoid common filename "main.py").

## Comments
* 

---
---

# Version 0.0.1

## Features
### Web Application:
* Basic account registration
* Basic account login
* Python template creation
* Python template saving
* Python template deletion
* Python template editing
* List of Python templates in homepage
* Download links for Python templates into text file
* Creation of testing server

### main.py:
* Template creation via both terminal use and dialog chooser

## Comments
* This is the first ever changelog of this repository!
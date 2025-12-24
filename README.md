# Blogging System (Course Project)
 
## Overview
This project implements a blogging system in Python by using the unittesting framework, CRUD operations file persistence, and a PyQt6 GUI.

## Features
- Login/logout
- Create, search, update, and delete blogs and posts.
- Persistence using DAO (JSON and Pickle storage)
- Graphical user interface in PyQt6
- Unittest testing

## Tech Stack
- Python 3.9.23
- Json
- Pickle
- PyQt6
- Unittest

## Installation
Clone repo and install required dependencies:

```bash
git clone https://github.com/atwoodg/SENG_265_A3-4-5.git
cd group078
pip install -r requirements.txt
```

## How to use
Running the system:
```bash
python -m blogging_gui
```

## Tests
From the project root folder (`group078/`):
```bash
#1
python -m unittest discover -s tests -p "*_test.py" -v

#2
python -m unittest -v ./tests/controller_test.py 
python -m unittest -v ./tests/integration_test.py

#3
python -m blogging gui

```
## Credits
Contributors: Gabriel Atwood, Michael Chen, Roberto Bittencourt
Course: SENG 265 (Software Development Methods)



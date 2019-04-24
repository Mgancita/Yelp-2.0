Search-Engine
================
This project implements the search engine module for yelp 2.0 project as part of BIA-660 coursework

Pre-requisite steps to setup:
==============================
1. This project was implemented in below python version.
$python
Python 3.7.0 (default, Jun 28 2018, 08:04:48) [MSC v.1912 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.

2.Create the project directory
$mkdir search_service && cd search_service
 
3.creates virtual enviroment named venv
search_service$ virtualenv --python=python3 venv search_service

4.Activate the virtual enviroment named venv
virtualenv --python=python3 venv
Windows:
virtualenv --python=<python_installed_directory>\python.exe venv

5.Activate virtual enviroment
activate venv


6.Install Django 
pip install Django==2.0.3

7.Install djangorestframework 
pip install djangorestframework

8. Create django project.
django-admin.py startproject api .


9.Create django app
django-admin.py startapp search

10.Sync database for the first time and create an initial user and set password for that user
python manage.py migrate

11. Execute below command with necessary user name and password
python manage.py createsuperuser --email admin@example.com --username admin

# FIT Accreditation Website

> Authors: Jason Myre, Joseph Ackerman, Jonathan Uss, Justyn Diaz

## Project Description

Website created using Django Web Framework to assist Florida Institute of Technology with their ABET accreditation reporting. This project is being developed by Jason Myre, Joseph Ackerman, Jonathon Uss, and Justyn Diaz as their computer science senior undergraduate project for Florida Institute of Technology.

## Contributor Instructions

###### INITIAL SET UP

1. Install Python 3.8

2. Create a Python environment in an external folder (not in the repository) using the command 'python -m venv (name)' and then cd into the folder that was created. Go to the Scripts folder and run './activate' to activate your environment. If it works properly, you will see environment name in parentheses to the left of your current path.

3. Return to the repository and run 'pip install -r requirements.txt' to set up your environment.

4. For now, this is all you should need. Once we implement Postgres for our database, there will be more steps here. 

###### INSTRUCTIONS TO RUN LOCAL

Because Django uses a secret key and this codebase is going to be publicly on GitHub, you will need to be given an additional file 'local.bat' in order to run your local server. Put it in the same folder as 'manage.py' and execute it in the command line with './local.bat runserver'. Other 'manage.py' functions can be executed with 'python manage.py' (shell_plus, migrate, makemigragtions, etc.).

###### IF CHANGES ARE MADE TO LOCAL.BAT

As we add more features to the website we may need to create more environment variables that cannot be public on GitHub. All contributors will be alterted if this happens, this README will be updated to list the most recent date 'local.bat' was changed.
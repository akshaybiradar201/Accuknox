# Getting Started

- Clone the project

- Create virtual enviroment : `python -m venv venv`

- Install requirements : `pip install -r requirements.txt`

- Run migrations : `python manage.py migrate`

- Create SuperUser: `python manage.py createsuperuser`

- Using the script, create more users:
    - `python manage.py shell_plus`
    - `from user_management.scripts import *`
    - `create_users()`

- Using the Api's send/accept/reject friend requests, while using postman use csrf token and sessionid as cookies and headers.


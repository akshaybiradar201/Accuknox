from .models import *

def create_users():
    for i in range(1,21):
        user = CustomUser(email=f'temp_{i}@gmail.com')
        user.is_staff = True
        user.is_superuser = True
        user.set_password('test')
        user.save()
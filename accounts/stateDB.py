import sqlite3 
from .models import EmployeeState

#データベースの場所の指定
a = 'user'
b = 1

c = EmployeeState(userID=a, EMPstate=b)
c.save()
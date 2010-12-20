import os
from sqlite3 import *

print os.getcwd()
conn = connect('../db/picturelogic.db')

cursor = conn.cursor()
cursor.execute('SELECT * from pictures')
print cursor.fetchall()
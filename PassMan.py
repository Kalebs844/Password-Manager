import sqlite3
from sqlite3.dbapi2 import Cursor
import hashlib
import os
import time
import base64


conn = sqlite3.connect('PassMan.db')                                               #Creating DB and Tables if not already made
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE Passwd (                                         
                        owner text,
                        app text,
                        user text,
                        paswd text
                        )''')
    cursor.execute('''CREATE TABLE users (
                       loginname text,
                       loginpass text
                        )''')
    conn.commit()
except:
    pass

#Password Hashing
def hashpass(pswd):
	setpass = bytes(pswd, 'utf-8')                                                #Convert string to UTF-8 byte
	hash_obj = hashlib.md5(setpass)                                               #Setting password to be MD5 
	md5hash = hash_obj.hexdigest()                                                #Converting to MD5
	return md5hash

#Auth
firstCom = input('Welcome to Password Manager\n[-----Login-----Signup-----]\n>')
if firstCom.lower() == 'signup':
    #Signup
    Signuser = input('Username: ')
    Signpass = input('Password: ')
    Signhash = hashpass(Signpass)
    cursor.execute('Select * From users Where loginname = ?;',(Signuser,))       #Checking Username availability 
    usercheck = cursor.fetchall()
    if len(usercheck) != 0:
        print('Username Not Avaliable')
        exit()
    signupquery = 'INSERT INTO users (loginname,loginpass) VALUES (?,?);'        #Adding Username and Password to database
    cursor.execute(signupquery, (Signuser,Signhash))
    conn.commit()
    owner = Signuser
    os.system('cls')
elif firstCom.lower() == 'login':
    #Login
    Loguser = input('Username: ')
    Logpass = input('Password: ')
    Loghash = hashpass(Logpass)
    cursor.execute('Select * From users Where loginname = ? AND loginpass = ?;',(Loguser,Loghash))
    logrows = cursor.fetchall()                                                  #Checking to see if user:pass pair is valid
    if len(logrows) == 1:
        owner = Loguser
        os.system('cls')
    else:
        print('Invalid Creds...')
        exit()
else:
    print('Invalid Option')
    exit()

#Home
while True:
    print(f'-------------------Password Manager-------------------\n')
    print('''1. Show all passwords
2. Search for a website
3. Add a password
4. Delete a password
5. Exit\n''' )
    op = input(f'{owner}> ')
    op = int(op)
    if op == 1:
        items = cursor.execute("Select app, user,paswd FROM Passwd Where owner =?;", (owner,))
        os.system('cls')
        for item in items:
            print(f'App: {item[0]}')
            print(f'Username: {item[1]}')
            print(f'Password: {item[2]}\n')
    elif op == 2:
        site = input('Enter Website or App: ')
        site = site.lower()
        cursor.execute('Select * from Passwd Where app = ? AND owner = ?;', (site,owner))
        rows = cursor.fetchall()
        print(len(rows))
        os.system('cls')
        for row in rows:
            print(f'App: {row[1]}')
            print(f'Username: {row[2]}')
            print(f'Password: {row[3]}\n')
    elif op == 3:
        wsite = input('Enter Website or App name: ')
        wuser = input('Enter Username: ')
        wpass = input('Enter Password: ')
        query = 'INSERT INTO Passwd (owner,app,user,paswd) VALUES (?,?,?,?);'
        cursor.execute(query, (owner,wsite,wuser,wpass))
        conn.commit()
        print('Data Added')
    elif op == 4:
        Dsite = input('Enter App to be Deleted: ')
        Dsite = Dsite.lower()
        cursor.execute('DELETE FROM Passwd Where app = ? AND owner = ?;', (Dsite,owner))
        conn.commit()
        print('Deleted')
        time.sleep(3)
        os.system('cls')
    elif op == 5:
        os.system('cls')
        print('Thank You for using my Password Manager')
        exit()
    else:
        print('\nInvalid option\n')
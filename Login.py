import bcrypt
import pandas as pd
import uuid

def Register():
    user_data = pd.read_csv('user_data.csv')
    
    
    user_name = input("Enter a username: ")
    user_pass = input("Enter a password: ")
    
    bytes = user_pass.encode('utf-8') 
     
    salt = bcrypt.gensalt() 
    print(salt) 
    
    user_password_hash = bcrypt.hashpw(bytes, salt) 
    
    print(user_password_hash)
    
    Flag = True
    while Flag:
        user_uuid = uuid.uuid4()
        if user_uuid not in user_data['UUID'].values:
            Flag = False
    
    
    new_user = {
        'Username': user_name,
        'Password': user_password_hash,
        'UUID': user_uuid,
        'Poke1': None,
        'Poke2': None,
        'Poke3': None,
        'Poke4': None,
        'Poke5': None,
        'Poke6': None
    }
    
    user_data = user_data.append(new_user, ignore_index=True)
    
    
def Login():
    
    user_data = pd.read_csv('user_data.csv')
    
    uname = input("Enter username: ")
    if uname in user_data['Username'].values:
        pwrd=input("Enter password: ")
        #Locate correct password from user data based on username
        correct_pass = user_data.loc[user_data['Username'] == uname, 'Password'].values
        correct_pass = correct_pass[0]

        print(correct_pass.encode('utf-8'))
        
        
        if bcrypt.checkpw(pwrd.encode('utf-8'), correct_pass.encode('utf-8')):
            print("Login Successful!")
        else:
            print("Incorrect password!")
    else:
        print("Username not found: Would you like to register?")
        choice = input("y/n:")
        if choice.lower() == 'y':
            Register()
        elif choice.lower() == 'n':
            pass
        
        
Register()
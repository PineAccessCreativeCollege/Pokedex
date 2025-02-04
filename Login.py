import bcrypt
import pandas as pd
import uuid

#def password_check(passwd):
     
    #SpecialSym =['$', '@', '#', '%']
    #val = True
     
    #if len(passwd) < 6:
        #pass_eror='length should be at least 6'
        #val = False, pass_eror
         
    #if len(passwd) > 20:
        #pass_eror='length should be not be greater than 8'
        #val = False, pass_eror
         
    #if not any(char.isdigit() for char in passwd):
        #pass_eror='Password should have at least one numeral'
        #val = False, pass_eror
         
    #if not any(char.isupper() for char in passwd):
        #pass_eror='Password should have at least one uppercase letter'
        #val = False, pass_eror
         
    #if not any(char.islower() for char in passwd):
        #pass_eror='Password should have at least one lowercase letter'
        #val = False, pass_eror
         
    #if not any(char in SpecialSym for char in passwd):
        #pass_eror='Password should have at least one of the symbols $@#'
        #val = False, pass_eror
    #if val:
        #return val, None
    
    
def Register():
    user_data = pd.read_csv('user_data.csv')
    
    
    try:
        user_name = input("Enter a username: ")
        if user_name in user_data['Username'].values:
            print("Username already exists!") 
        user_pass = input("Enter a password: ")
        
        
        if (not user_pass.isspace() or not len(user_pass) < 8 or not len(user_pass) > 20):
            print("Password is valid")
        else:
            print("Invalid Password!!")
            return
            
    except Exception as e:
        print("An error occurred:", e)
    
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
    
    user_password_hash = user_password_hash.decode('utf-8')
    
    new_user = {
        'Username': user_name,
        'Password': user_password_hash,
        'UUID': user_uuid,
        'Poke1': 1,
        'Poke2': 4,
        'Poke3': 7,
        'Poke4': 10,
        'Poke5': 13,
        'Poke6': 16
    }
    
    user_data.loc[len(user_data)] = new_user
    
    new_csv = user_data.to_csv('user_data.csv', index=False)
    
def Login(username, password):
    
    user_data = pd.read_csv('user_data.csv')
    
    uname = username
    if uname in user_data['Username'].values:
        pwrd=password
        #Locate correct password from user data based on username
        correct_pass = user_data.loc[user_data['Username'] == uname, 'Password'].values
        correct_pass = correct_pass[0]

        print(correct_pass.encode('utf-8'))
        
        
        if bcrypt.checkpw(pwrd.encode('utf-8'), correct_pass.encode('utf-8')):
            print("Login Successful!")
        else:
            print("Incorrect password!")
    else:
        print("Username not found, you can register?")
        
        
Register()
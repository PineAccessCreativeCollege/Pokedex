import bcrypt
import pandas as pd
import uuid
    
def Register(username, password):
    user_data = pd.read_csv('user_data.csv')
    
    user_name = str(username)
    user_pass = password
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
    
    return True, user_uuid

def Login(username, password):
    
    error=""
    user_data = pd.read_csv('user_data.csv')
    
    uname = str(username)
    if uname in user_data['Username'].values:
        pwrd=password
        #Locate correct password from user data based on username
        correct_pass = user_data.loc[user_data['Username'] == uname, 'Password'].values
        correct_pass = correct_pass[0]

        print(correct_pass.encode('utf-8'))
        
        
        if bcrypt.checkpw(pwrd.encode('utf-8'), correct_pass.encode('utf-8')):
            print("Login Successful!")
            user_uuid = user_data.loc[user_data['Username'] == uname, 'UUID'].values
            return True, user_uuid[0]
        else:
            error="Incorrect password"
            print("Incorrect password!")
            return False, error
    else:
        error="Username not found, you can register?"
        print("Username not found")
        return False, error
        
        
if __name__ == "__main__":  
    Register()
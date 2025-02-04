import bcrypt
import pandas as pd

def main():
    
    user_data = pd.read_csv('user_data.csv')
    
    uname = input("Enter username: ")
    if uname in user_data['Username'].values:
        pwrd=input("Enter password: ")
        user_row = user_data[user_data['Username'] == uname]
        print(user_row)
        encrypted_pwrd = user_data.loc[user_data['Username'] == uname, 'Password']
        print(encrypted_pwrd)
        if bcrypt.checkpw(pwrd.encode('utf-8'), encrypted_pwrd.encode('utf-8')):
            print("Login Successful!")
        else:
            print("Incorrect password!")
    
if __name__ == "__main__":
    main()
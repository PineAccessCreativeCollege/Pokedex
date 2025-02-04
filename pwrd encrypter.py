import bcrypt 
  
# example password 
password = 'Hey'
  
# converting password to array of bytes 
bytes = password.encode('utf-8') 
  
# generating the salt 
salt = bcrypt.gensalt() 
print(salt)  # this will be printed as a byte string  # example salt: b'$2b$12$V9f1g9hO383a95
  
# Hashing the password 
hash = bcrypt.hashpw(bytes, salt) 
print(hash.decode('utf-8')) # this will be printed as a byte string # example
  
print(hash)
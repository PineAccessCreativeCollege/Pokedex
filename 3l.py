data = ['H','e','l','l','o',' ','W','o','r','l','d']
for i in range(len(data)):
    print(data[i], end='')
    
for c in ['\nH','e','l','l','o',' ','W','o','r','l','d']: print(c, end='')

print(''.join(data))


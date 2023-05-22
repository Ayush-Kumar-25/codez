import random
wordlist = []
with open("file.txt","r") as ayush:
   python = ayush.readlines()
for line in python:
    words = line.split()
    for items in words:
        if len(items) > 5:
            wordlist.append(items.capitalize())
word = random.choice(wordlist)
spca = ['!','@','#','$','%','^','&']
spa = random.choice(spca)
num = str(random.randint(10,99))
passd = word + spa + num
print(passd)

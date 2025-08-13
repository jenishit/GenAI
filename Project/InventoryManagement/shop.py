import json
file_path = 'category.json'
Name = input('Please Provide your name: ')
print(f'Welcome {Name}, We have following Sections -')
with open(file_path, 'r') as file:
    Categories = json.load(file)
print(Categories)
for i, category in enumerate(Categories):
    print(f'{i+1} {category}')
    
ch = input()
while (True and ch):
    if ch == 1:
        content = Categories[category]
        for item in content:
                print(item)
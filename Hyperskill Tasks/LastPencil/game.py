import random

while 1:


    try:
        number_pencils = int(input('How many pencils'))
        if number_pencils < 0:
            raise ValueError
    except ValueError:
        print('The number of pencils should be numeric')
        continue
    if number_pencils == 0:
        print('The number of pencils should be positive')
        continue
    break

names = []
names.append('John')
names.append('Jack')
print("Who will be the first (" + names[0] +', ' + names[1] + ')')
while 1:
    name = input()
    if name not in names:
        print("Choose between '"  + names[0] + "' and '" + names[1] + "'")
        continue
    break

pencils_list = []
for _ in range(number_pencils):
    pencils_list.append('|')

for i in range(len(names)):
    if name == names[i]:
        round = i
        bot_number = (i+1)%2
while 1:
    player_number = round%2
    print(''.join(pencils_list))


    if player_number == 0:
        print((names[player_number] + "'s turn:"))
        while 1:
            try:
                pencils_to_take = int(input())
            except ValueError:
                print("Possible values: '1', '2' or '3'")
                continue

            if pencils_to_take not in (1,2,3):
                print("Possible values: '1', '2' or '3'")
                continue
            if pencils_to_take> len(pencils_list):
                print('Too many pencils were taken')
                continue

            break

    else:
        print((names[player_number] + "'s turn!"))
        pencils_remaining = len(pencils_list)
        if pencils_remaining%4 == 0:
            pencils_to_take = 3

        elif (pencils_remaining-3)%4 == 0:
            pencils_to_take = 2

        elif (pencils_remaining-2)%4 == 0 or pencils_remaining == 1:
            pencils_to_take = 1
        else:
            pencils_to_take = random.randint(1,3)
        print(pencils_to_take)

    for _ in range(pencils_to_take):
        pencils_list.pop()
    if bool(pencils_list):
        round += 1
        continue
    else:
        round += 1
        player_number = round % 2
        print(names[player_number] + " won!")
        break
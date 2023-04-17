# write your code here
#seq = input()

# initial state
seq = '_________'


seq = list(seq)
state=0
result = 'none'

print('---------')
for i in range(0,3):
    print('| ' + ' '.join(seq[i*3:i*3+3]) + ' |' )
print('---------')


while 1:

    player = state%2 + 1

    if player == 1:
        while 1:
            cords = input('X make a move').split()

            try:
                cords = [int(cord) for cord in cords]
            except ValueError:
                print('You should enter numbers!')
                continue

            cordy = cords[0]
            cordx = cords[1]

            if (cordy or cordx) not in [1,2,3]:
                print('Coordinates should be from 1 to 3!')
                continue


            if seq[(cordy-1)*3 + (cordx-1)] != '_':
                print("This cell is occupied! Choose another one!")
                continue

            break
        seq[(cordy-1)*3 + (cordx-1)] = 'X'

    if player == 2:
        while 1:
            cords = input('O make a move').split()

            try:
                cords = [int(cord) for cord in cords]
            except ValueError:
                print('You should enter numbers!')
                continue

            cordy = cords[0]
            cordx = cords[1]

            if (cordy or cordx) not in [1, 2, 3]:
                print('Coordinates should be from 1 to 3!')
                continue

            if seq[(cordy - 1) * 3 + (cordx - 1)] != '_':
                print("This cell is occupied! Choose another one!")
                continue

            break

        seq[(cordy - 1) * 3 + (cordx - 1)] = 'O'





    os_number = seq.count('O')
    x_number = seq.count('X')
    floor_number = seq.count('_')





    for i in range(0,3):
        if seq[i*3:i*3+3].count('O') == 3 or seq[i:i+7:3].count('O') == 3 or seq[2:7:2].count('O') == 3 or seq[0:9:4].count('O') == 3:
            result = 'O wins'
        if seq[i*3:i*3+3].count('X') == 3 or seq[i:i+7:3].count('X') == 3 or seq[2:7:2].count('X') == 3 or seq[0:9:4].count('X') == 3:
            result = 'X wins'


    if floor_number!=0 and not result in ('O wins', 'X wins'):
        #result = 'Game not finished'
        result = 'none'

    if floor_number == 0 and  result not in ('O wins', 'X wins'):
        result = 'Draw'

    if abs(os_number-x_number)>1 or (result == 'O wins' and x_number>os_number) or (result == 'X wins' and os_number>x_number):
        result = 'Impossible'



    print('---------')
    for i in range(0,3):
        print('| ' + ' '.join(seq[i*3:i*3+3]) + ' |' )
    print('---------')

    if result != 'none':
        print(result)
        break


    state +=1

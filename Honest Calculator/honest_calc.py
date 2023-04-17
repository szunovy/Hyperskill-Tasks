def check(v1, v2, v3):
    msg = ''

    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6

    if (v1 == 1 or v2 == 1) and v3 == '*':
        msg = msg + msg_7

    if (v1 == 0 or v2 == 0) and (v3 in ('*', '+', '-')):
        msg = msg + msg_8

    if msg != '':
        msg = msg_9 + msg
        print(msg)


def is_one_digit(v):
    if abs(v) < 10 and v.is_integer():
        return True
    else:
        return False


msg_0 = "Enter an equation"

msg_1 = "Do you even know what numbers are? Stay focused!"

msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"

msg_3 = "Yeah... division by zero. Smart move..."

msg_4 = "Do you want to store the result? (y / n):"

msg_5 = "Do you want to continue calculations? (y / n):"

msg_6 = " ... lazy"

msg_7 = " ... very lazy"

msg_8 = " ... very, very lazy"

msg_9 = "You are"

msg_10 = "Are you sure? It is only one digit! (y / n)"

msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"

msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
# write your code here

operations = ['+', "-", "/", "*"]

# accepting input until its correct

memory = 0


stop = 0
while stop == 0:
    [x, oper, y] = input(msg_0).split()

    if x == 'M':
        x = memory
    if y == 'M':
        y = memory

    try:
        x = float(x)
        y = float(y)
    except ValueError:
        print(msg_1)
        continue

    if oper not in operations:
        print(msg_2)
        continue

    check(x, y, oper)

    if oper == '+':
        result = x + y
    elif oper == '-':
        result = x - y
    elif oper == '*':
        result = x * y
    elif oper == '/' and y != 0:
        result = x / y
    elif oper == '/' and y == 0:
        print(msg_3)
        continue

    print(result)
    stop2 = 0
    while stop2 == 0:
        answer = input(msg_4)

        if answer == 'y':
            if is_one_digit(result):
                msg_index = 10
                while 1:
                    answer2 = input(locals()['msg_' + str(msg_index)])
                    if answer2 == 'y':
                        if msg_index < 12:
                            msg_index += 1
                        else:
                            memory = result
                            stop2 = 1
                            break
                    elif answer2 == 'n':
                        stop2 = 1
                        break
            else:
                memory = result
                break

         #   break
        elif answer == 'n':
            break

    while 1:
        answer = input(msg_5)

        if answer == 'y':
            break
        elif answer == 'n':
            stop = 1
            break

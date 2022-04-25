def zad1():
    a = int(input())
    b = int(input())
    n = int(input())

    if a > (b/n + bool(b%n)):
        print('Yes')
    else: print('No')


# ab = input()
# ac = input()
# bc = input()
#
# a=0
# b=0
# c=0
#
# str = 'abc'
#
# if ab == '>':
#     a += 1
# elif ab == '<':
#     b += 1
# elif ab == '=':
#     pass
#
# if bc == '>':
#     c -= 1
# elif bc == '<':
#     c += 1
# elif bc == '=':
#     pass
#
# if ac == '>':
#     a += 1
# elif ac == '<':
#     c += 1
# elif ac == '=':
#     pass
#
# print(a,b,c)


def zad2():
    ab = input()
    ac = input()
    bc = input()
    t = ''
    if ab == '<' and ac == '<':
        if bc == '>':
            t = 'acb'
        else:
            t = 'abc'
    elif ab == '>' and ac == '>':
        if bc == '>':
            t = 'cba'
        else:
            t = 'bca'
    elif ab == '<' and ac == '>':
        t = 'cab'
    elif ab == '>' and ac == '<':
        t = 'bac'
    elif ab == '=':
        if ac == '>':
            t = 'cba'
        else:
            t = 'abc'
    # elif ac == '=':
    #     if ab == '<':
    #         t = 'cab'
    #     else:
    #         t = 'bac'
    # elif bc == '=':
    #     if ac == '>':
    #         t = 'cba'
    #     else:
    #         t = 'abc'

    if ab == '=' or ac == '=' or bc == '=':
        temp_list = list(t)
        if ab == '=':
            temp_list[temp_list.index('a')] = 'b'
            temp_list[temp_list.index('b')] = 'a'
            print(t, ''.join(temp_list))
        elif ac == '=':
            temp_list[temp_list.index('a')] = 'c'
            temp_list[temp_list.index('c')] = 'a'
            print(t, ''.join(temp_list))
        elif bc == '=':
            temp_list[temp_list.index('b')] = 'c'
            temp_list[temp_list.index('c')] = 'b'
            print(t, ''.join(temp_list))
    else:
        print(t)

def zad3():
    n = int(input())
    x = 0
    while (n % 10 == 0):
        n /= 10
        x += 1
    print(x)


def zad4(n):
    mat = [[0 for j in range(n)] for i in range(n)]
    middle = n/2
    if n%2 != 0:
        middle += 0.5
    middle = int(middle)
    print(middle)
    for i in range(n):
        for j in range(n):
            if (j < middle):
                mat[i][j] = chr(ord('a') + j)
            else:
                mat[i][j] = chr(ord('a') + middle - j)


    for str in mat:
        print(str)


def zad5():
    inp_str = input().split(' ')
    n = int(inp_str[0])
    k = int(inp_str[1])

    s = []
    for i in range(n):
        s.append(i+1)

    p = [0 for _ in s]
    i = 1
    permutations = []
    permutations.append(list(s))

    while i < len(s):
        if p[i] < i:
            j = 0 if i % 2 == 0 else p[i]
            s[i], s[j] = s[j], s[i]
            p[i] += 1
            i = 1
            if s not in permutations:
                permutations.append(list(s))
        else:
            p[i] = 0
            i += 1
    ks = []
    for p in permutations:
        sum = 0;
        for i in range(p.__len__()):
            sum += p[i] * i
        ks.append(sum)
    res = 0
    for c in ks:
        if (c % k == 0):
            res += 1
    print(res)

def zad6():
    s = []
    n = 4
    for i in range(n):
        s.append(i + 1)

    p = [0 for _ in s]
    i = 1
    permutations = []
    permutations.append(list(s))

    while i < len(s):
        if p[i] < i:
            j = 0 if i % 2 == 0 else p[i]
            s[i], s[j] = s[j], s[i]
            p[i] += 1
            i = 1
            if s not in permutations:
                permutations.append(list(s))
        else:
            p[i] = 0
            i += 1
    print(permutations)
zad4(5)
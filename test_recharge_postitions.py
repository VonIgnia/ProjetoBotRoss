n = 0
while n < 14:
    x = 18.25 + int(n % 7) * 36.5
    y = 18.25 + int(n / 7) * 36.5
    print ("N: {}; ({},{})". format(n, x, y))
    n += 1
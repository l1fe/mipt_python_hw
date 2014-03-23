__author__ = 'inaumov'

import math

t = int(input())

while t:
    t -= 1
    k = int(input())
    row_p = float(((1 + 8 * k) ** 0.5 - 1) / 2.0)
    row = int(math.ceil(row_p))

    pos = int(k - (row * (row - 1)) / 2)

    a = int(row - pos + 1)

    if row % 2 == 0:
        print('TERM', k, 'IS', '/'.join((str(pos), str(a))))
    else:
        print('TERM', k, 'IS', '/'.join((str(a), str(pos))))
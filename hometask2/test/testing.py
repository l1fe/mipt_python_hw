__author__ = 'inaumov'

N = 5
a1 = [x for x in range(N) if x % 2 == 1]; s = set(a1); a2 = [x for x in s]
print(a1 == a2)
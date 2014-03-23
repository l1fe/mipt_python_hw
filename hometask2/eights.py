__author__ = 'inaumov'

l = []
ans = []
for i in range(1000):
    if (i**3 % 1000 == 888):
        l.append(i)

t = (int)(input())

for i in range(t):
    k = (int)(input())
    ans.append(l[(k - 1) % len(l)] + (k - 1) // len(l) * 1000)

for i in range(len(ans)):
    print(ans[i])
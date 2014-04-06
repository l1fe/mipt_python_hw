__author__ = 'inaumov'

for i in range(int(input())):
    parameters = [float(x) for x in input().split()]
    a = parameters[0]

    b = parameters[1] / parameters[2] * a
    c = parameters[1] / parameters[3] * a

    distance = (2/3 * (9 * (b / parameters[1] * c / 6) ** 2 - (a * a + b * b + c * c)) ** (1/2)).real

    print(round(3 * a * parameters[1] / 2, 3), round(distance, 3))

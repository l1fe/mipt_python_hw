__author__ = 'inaumov'

columns_num = (int)(input())
ans_list = []

while (columns_num):
    e_str = input()
    line_num = (int) (len(e_str) / columns_num)
    ans = ''
    z = 1
    for y in range(0, columns_num):
        #print(y, end = " ")
        ans += e_str[y]
        for z in range(1, line_num // 2 + 1):
            if (2 * z * columns_num - y - 1 < len(e_str)):
                #print(2 * z * columns_num - y - 1, end = " ")
                ans += e_str[2 * z * columns_num - y - 1]
            if (2 * z * columns_num + y < len(e_str)):
                #print(2 * z * columns_num + y, end = " ")
                ans += e_str[2 * z * columns_num + y]
            #print()
    ans_list.append(ans)
    columns_num = (int)(input())


print('\n'.join(ans_list))

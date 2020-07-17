# import re

# str = '\巴拉<1"!11【】>1*hgn/p:?|  \t \v '

# print(str[str.find('#')+1:])


# # 提取想要的字符
# # a = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',str,re.S)
# # a = re.findall('[a-zA-Z0-9]+',str,re.S)
# a = re.findall('[\u0030-\u0039]+', str, re.S)

# a = "".join(a)
# print(a)

# # 去除不想要的字符
# b = re.findall(r'[^\*"/:?\\|<>]', str, re.S)
# b = "".join(b)
# print(b)


# for i in range(len(str)):
#     if i == (len(str)-1):
#         break

#     ch = str[i]
#     ch_next = str[i+1]
#     if ch.isdigit():
#         if ch_next.isdigit():
#             wafer = f'{ch}{ch_next}'
#             i = i + 1
#             print(wafer)
#         else:
#             wafer = str[i]
#             print(wafer)

import functools

str1 = '#05#,06#,07#,08#~20#-25'
str1 = '#01,2,10_25'

is_add = False

waferlist = []


def my_compare(x, y):
    if int(x) > int(y):
        return 1
    elif int(x) < int(y):
        return -1
    return 0


for i in range(len(str1)):
    if i == (len(str1)-1):
        if not str1[i-1].isdigit():
            waferlist.append(str1[i])
        break

    if is_add:
        is_add = False
        continue

    if str1[i].isdigit():
        if str1[i+1].isdigit():
            wafer = f'{str1[i]}{str1[i+1]}'
            is_add = True
            # print(wafer)
            waferlist.append(wafer)
        else:
            wafer = str1[i]
            # print(wafer)
            waferlist.append(wafer)
    else:
        if str1[i] == '~' or str1[i] == '-' or str1[i] == '_':
            wafer = '$'
            waferlist.append(wafer)


# print(waferlist)
# numB = 0
# for i in range(len(waferlist)):
#     if waferlist[i+numB] == '$':
#         waferlist.remove('$')
#         if i == 0:
#             pass
#         else:
#             numB = int(waferlist[i]) - int(waferlist[i-1])-1
#             for j in range(int(waferlist[i-1])+1, int(waferlist[i])):
#                 waferlist.insert(i, f'{j}')


print(waferlist)
waferlist_new = []
# numB = 0
for i in range(len(waferlist)):
    if waferlist[i] == '$':
        # waferlist.remove('$')
        if i == 0:
            pass
        else:
            # numB = int(waferlist[i]) - int(waferlist[i-1])-1
            for j in range((int(waferlist[i-1])+1), int(waferlist[i+1])):
                waferlist_new.append(f'{j}')

waferlist.extend(waferlist_new)



print(waferlist)

# waferlist.sort(key=functools.cmp_to_key(my_compare))

# print(waferlist)

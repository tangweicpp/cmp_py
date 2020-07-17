import re

# Get list


def get_wafer_list(wafer_str):
    wafer_str_new = re.sub(r'[_~-]', ' _ ', wafer_str)
    pattern = re.compile(r'[A-Za-z0-9_]+')
    result1 = pattern.findall(wafer_str_new)

    # extend
    for i in range(1, len(result1)-1):
        if result1[i] == '_':
            if result1[i-1].isdigit() and result1[i+1].isdigit():
                bt = []
                if int(result1[i-1]) < int(result1[i+1]):
                    for j in range(int(result1[i-1])+1, int(result1[i+1])):
                        bt.append(f'{j}')
                else:
                    for j in range(int(result1[i-1])-1, int(result1[i+1]), -1):
                        bt.append(f'{j}')
                result1.extend(bt)

    # remove '_'
    result2 = sorted(set(result1), key=result1.index)

    if '_' in result2:
        result2.remove('_')
    # sort

    print(result2)


str1 = ' `#abc 123 45 6  7-20  a~5 10-'
str1 = '#1 2~5 5-10 ab c ABc'
get_wafer_list(str1)

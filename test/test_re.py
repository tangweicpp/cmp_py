import re


# phone = "2004-这是一个国外电话号959-559 # 这是一个国外电话号码"

# # 删除字符串中的python注释
# num = re.sub(r'#.*$', ",", phone)
# print("电话号码是：", num)


# pattern = re.compile(r'\w')   # 查找数字 \d

pattern = re.compile(r'[A-Za-z0-9_]+')
# pattern = re.compile(r'[A-Za-z0-9_]+')
# pattern = re.compile(r'[0-9_~]+')
result1 = pattern.findall('runoob 1,2 3 123 _4,8google 456')
result2 = pattern.findall('run88oob123google456', 0, 10)
result1 = pattern.findall('#5 _ 20,Aabc')
result1 = pattern.findall('ABCD 123 Aabc')


# print(result1)
# print(result2)

wafer_str = 'abc-123~456_789'
wafer_str = 'abc'

wafer_str_new = re.sub(r'[_~-]', ' - ', wafer_str)
# print(wafer_str_new)

wafer_str = 'abc-123 4 5 6 8  10~456_789'
wafer_str = '12 3 54 #5~20 30-40'
wafer_str_new = re.sub(r'[_~-]', ' _ ', wafer_str)
pattern = re.compile(r'[A-Za-z0-9_]+')
result1 = pattern.findall(wafer_str_new)
print(result1)

# extend
for i in range(1, len(result1)-1):
    if result1[i] == '_':
        if result1[i-1].isdigit() and result1[i+1].isdigit():
            bt = []
            if int(result1[i-1]) < int(result1[i+1]):
                for j in range(int(result1[i-1])+1, int(result1[i+1])):
                    bt.append(f'{j}')
            else:
                for j in range(int(result1[i+1])-1, int(result1[i-1]), -1):
                    bt.append(f'{j}')
            result1.extend(bt)

# remove '_'
result2 = sorted(set(result1), key=result1.index)
print(f'result1={result1}')
print(f'result2={result2}')
result2.remove('_')
print(f'result2new={result2}')

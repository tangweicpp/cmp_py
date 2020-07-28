from handle import delete_po_data
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl import load_workbook
from itertools import groupby

import xlrd




# def thans_col_row_from_string(s):
#     dict = {}
#     s = 'AB10'
#     ss = [''.join(list(g)) for k, g in groupby(s, key=lambda x: x.isdigit())]

#     dict['col'] = column_index_from_string(ss[0]) - 1
#     dict['row'] = int(ss[1]) - 1
#     return dict


# str1 = ['K1']
# dict1 = thans_col_row_from_string(str1)
# print(dict1)


# ```
# 13105
# 13106
# 13107
# 13108
# 13109
# ```

# test_dict = {"abc": 123, "bcd": 234}
# for item in test_dict:
#     print(item)


del_list = ['13884','13866']

for del_id in del_list:
    delete_po_data('2', del_id)
    print(f'{del_id}删除成功')


# Get cell value by openpyxl

# key_postion = 'K1'
# file_name = 'GULF20034KS 7.22.xls'
# # wb = load_workbook(file_name)
# # ws = wb.get_sheet_by_name(wb.sheetnames[0])
# # cell_val = ws[key_postion].value
# # print(cell_val)


# data = xlrd.open_workbook(file_name)
# table = data.sheets()[0]
# column_index_from_string('K')

# data = table.cell_value(1-1, column_index_from_string('K')-1)
# # data = table.row_values(0)
# print(data)

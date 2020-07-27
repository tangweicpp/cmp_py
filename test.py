from handle import delete_po_data

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


del_list = ['13813', '13777', '13814', '13827','13823','13815','13820']

for del_id in del_list:
    delete_po_data('2', del_id)
    print(f'{del_id}删除成功')

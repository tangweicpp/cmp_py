from handle import delete_po_data

# ```
# 13105
# 13106
# 13107
# 13108
# 13109
# ```

del_list = ['13732', '13707', '13662', '13768']

for del_id in del_list:
    delete_po_data('2', del_id)
    print(f'{del_id}删除成功')

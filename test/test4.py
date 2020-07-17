
lot_id = 'ABCD'
wafer_id = 0.5
sql = f'''
select * from mappingdatatest where lotid = '{lot_id}' and 
waferid = {wafer_id}
'''

print(sql)

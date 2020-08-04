'''
@File    :   handle_po_mgr.py
@Time    :   2020/07/31 15:50:12
@Author  :   Tony Tang
@Version :   1.0
@Contact :   wei.tang_ks@ht-tech.com
@License :   (C)Copyright 2020-2021
@Desc    :   customer po mgr
'''
import connect_db as conn
import time
import os
import send_email as se
import pandas as pd
import numpy as np
import json
import re
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl import load_workbook
from xlrd import open_workbook
from itertools import groupby


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# None to ''
def xstr(s):
    return '' if s is None else str(s).strip()


# Get po data
def get_po_data(po_query):
    json_data = []

    sql = f'''
        select a.customershortname,b.MPN_DESC,a.lotid,a.substrateid, CASE WHEN c.WAFERID IS null THEN 'N' ELSE 'Y' end,b.WAFER_VISUAL_INSPECT from mappingdatatest a
        INNER JOIN CUSTOMEROITBL_TEST b ON a.FILENAME = to_char(b.id) 
        left JOIN IB_WAFERLIST c ON a.SUBSTRATEID  = c.WAFERID  AND a.LOTID  = c.WAFERLOT 
        where a.lotid = '{po_query['cust_lot_id']}' 
        order by substrateid 
    '''
    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['cust_code'] = xstr(row[0])
        result['cust_pn'] = xstr(row[1])
        result['lot_id'] = xstr(row[2])
        result['wafer_id'] = xstr(row[3])
        result['is_worked'] = xstr(row[4])
        result['upload_id'] = xstr(row[5])

        json_data.append(result)
    return json_data

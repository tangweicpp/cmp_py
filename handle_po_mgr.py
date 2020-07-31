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

    sql = f"select customershortname,lotid,substrateid from mappingdatatest where lotid = '{po_query['cust_lot_id']}' order by substrateid "
    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['cust_code'] = xstr(row[0])
        result['lot_id'] = xstr(row[1])
        result['wafer_id'] = xstr(row[2])

        json_data.append(result)
    return json_data

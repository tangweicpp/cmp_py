'''
@File    :   handle.py
@Time    :   2020/07/09 15:30:00
@Author  :   Tang wei
@Version :   1.0
@Contact :   wei.tang_ks@ht-tech.com
@License :   (C)Copyright 2020-2021
@Desc    :   None
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


user_progress = {}
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# None转空字符串
def xstr(s):
    return '' if s is None else str(s).strip()

# Upload progress


def get_progress(user_key):
    global user_progress
    return user_progress[f'{user_key}']


# Check username and password
def check_account(username, password):
    if not (username and password):
        print('用户名或密码为空')
        return False

    sql = "select 用户号 from erpbase..tblOperatorData where 用户号 = '%s' and 密码= '%s' " % (
        username, password)
    results = conn.MssConn.query(sql)
    if not results:
        print('查询不到数据')
        return False
    return True


# Get customer list
def get_custcode_list():
    jsonData = []

    sql = "SELECT DISTINCT CUSTOMERSHORTNAME FROM TBLTSVNPIPRODUCT ORDER BY CUSTOMERSHORTNAME "
    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['value'] = str(row[0])
        result['label'] = str(row[0])

        jsonData.append(result)
    return jsonData


# Get customer po template
def get_po_template(custcode):
    if not custcode:
        print('客户代码不可为空')
        return []

    jsonData = []
    sql = "SELECT CUST_CODE,TEMPLATE_FILE ,TEMPLATE_PIC ,KEY_LIST ,FILE_LEVEL,FILE_URL,ACCEPT,TEMPLATE_ID FROM CMP_CUST_PO_TEMPLATE WHERE CUST_CODE  = '%s'" % (
        custcode)
    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['file_name'] = str(row[1])
        result['img_url'] = str(row[2])
        result['file_key'] = str(row[3])
        result['level'] = str(row[4])
        result['file_url'] = str(row[5])
        result['accept'] = str(row[6])
        result['file_id'] = str(row[7])
        result['show_progress_flag'] = False
        result['show_filelist_flag'] = False
        result['load_progress'] = 0

        jsonData.append(result)
    return jsonData


# Upload po file
def upload_po_file(f, po_header):
    global user_progress
    if not f:
        print('文件不存在')
        return False

    file_dir = os.path.join(os.getcwd(), 'uploads/po/' +
                            po_header['po_type']+'/'+po_header['cust_code'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, f.filename)
    f.save(file_path)

    # Set upload id
    sql = "select PO_ITEM_SEQ.nextval from dual"
    po_header['upload_id'] = conn.OracleConn.query(sql)[0][0]

    # Parse
    parse_po_file(file_path, po_header)

    # Del user key
    # del user_progress[po_header['user_upload_progress']]

    ret = get_upload_data(po_header['upload_id'])

    # Send mail
    send_mail(ret, po_header, file_path)

    return ret


# Sent mail
def send_mail(ret_data, po_header, mail_attachment):
    mail_keyid = po_header['upload_id']

    mail_body = get_mail_body(
        '07885', mail_keyid, po_header['mail_content'], ret_data)
    sql = "select recv_user_to from erp_email_recv where email_type = 'WO_UPLOAD_RECV_TEST' "
    mail_recv = conn.OracleConn.query(sql)[0][0].split(',')
    sql = "select recv_user_cc from erp_email_recv where email_type = 'WO_UPLOAD_RECV_TEST' "
    mail_recv_cc = conn.OracleConn.query(sql)[0][0].split(',')
    mail_title = '测试新版WO上传'

    se.send_email(mail_title, mail_body, mail_attachment,
                  mail_recv, mail_recv_cc)


# Get mail body
def get_mail_body(createBy, uploadid, addContent, json_data):
    # Get total data
    content = f'''
          内勤人员：{createBy} 上传WO
          <div style="color:red">{addContent}</div>
          <h2>以下为上传WO的汇总信息</h2>
          <table border="1" cellspacing="0" cellpadding="5" style="border:rgb(175, 175, 175) solid thin">
              <tr style="background-color: rgb(175, 175, 175);">
                  <th>序号</th><th>保税</th><th>客户代码</th><th>客户PO</th><th>客户机种</th><th>客户Fab机种</th><th>厂内机种</th><th>晶圆料号</th>
                  <th>客户LOTID</th><th>片数</th><th>DIES</th><th>上传人员工号</th><th>上传时间</th>
              </tr>
          '''

    for row in json_data['total_data']:
        content = content + f'''<tr><td>{row['id']}</td><td>{row['banded']}</td><td>{row['cust_code']}</td><td>{row['po_id']}</td>
        <td>{row['cust_device']}</td><td>{row['fab_device']}</td><td>{row['ht_pn']}</td><td>{row['wafer_pn']}</td>
        <td>{row['lot_id']}</td><td>{row['wafer_qty']}</td><td>{row['die_qty']}</td><td>{row['upload_by']}</td><td>{row['upload_date']}</td></tr>
        '''

    content = content + '</table>'

    # Get detail data
    content = content + f'''<h2>以下为明细数据</h2>
    <table border="1" cellspacing="0" cellpadding="5" style="border:rgb(175, 175, 175) solid thin">
              <tr style="background-color: rgb(175, 175, 175);">
                  <th>序号</th><th>客户PO</th><th>客户机种</th><th>客户Fab机种</th><th>厂内机种</th>
                  <th>客户LOTID</th><th>waferID</th><th>grossdies</th><th>打标码</th>
              </tr>
    '''

    for row in json_data['detail_data']:
        content = content + f'''<tr><td>{row['id']}</td><td>{row['po_id']}</td>
        <td>{row['cust_device']}</td><td>{row['fab_device']}</td><td>{row['ht_pn']}</td>
        <td>{row['lot_id']}</td><td>{row['wafer_id']}</td><td>{row['gross_dies']}</td><td>{row['mark_code']}</td></tr>
        '''

    content = content + '</table>'

    return content


# Get upload data
def get_upload_data(upload_id):
    dict_data = {}
    json_data_total = []
    json_data_detail = []

    # Total data
    sql = f'''
    select row_number() over(ORDER BY bb.lotid) as 序号,case bb.substratetype when 'A' THEN '保税' when 'B' THEN '非保税' else '未知' end as 是否保税,
    bb.customershortname as 客户代码,aa.po_num,aa.mpn_desc as 客户机种名,aa.Fab_conv_id as 客户Fab机种,aa.mtrl_num as 厂内机种,cc.MARKETLASTUPDATE_BY AS 晶圆料号,
    bb.lotid AS LOTID,count(bb.wafer_id) AS 片,sum(bb.passbincount + bb.failbincount) Dies,bb.qtech_created_by, to_char(bb.qtech_created_date,'yyyy-MM-dd')
    from customeroitbl_test aa inner join mappingdatatest bb on to_char(aa.id) = bb.filename INNER JOIN TBLTSVNPIPRODUCT cc ON aa.CUSTOMERSHORTNAME  = cc.CUSTOMERSHORTNAME 
    AND aa.MPN_DESC  = cc.CUSTOMERPTNO1 AND aa.FAB_CONV_ID  = cc.CUSTOMERPTNO2  where aa.wafer_visual_inspect = '{upload_id}'
    group by bb.customershortname,aa.Fab_conv_id,aa.mpn_desc,bb.lotid,aa.mtrl_num,bb.passbincount,bb.failbincount,aa.po_num,bb.qtech_created_by,
    to_char(bb.qtech_created_date,'yyyy-MM-dd'),bb.substratetype,cc.MARKETLASTUPDATE_BY 
    '''
    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['id'] = str(row[0])
        result['banded'] = str(row[1])
        result['cust_code'] = str(row[2])
        result['po_id'] = str(row[3])
        result['cust_device'] = str(row[4])
        result['fab_device'] = str(row[5])
        result['ht_pn'] = str(row[6])
        result['wafer_pn'] = str(row[7])
        result['lot_id'] = str(row[8])
        result['wafer_qty'] = str(row[9])
        result['die_qty'] = str(row[10])
        result['upload_by'] = str(row[11])
        result['upload_date'] = str(row[12])

        json_data_total.append(result)

    dict_data['total_data'] = json_data_total

    # Detail data
    sql = f'''
    select row_number() over(ORDER BY  bb.lotid,bb.substrateid) as 序号,case bb.substratetype when 'A' then '保税' when 'B' then '非保税' else '未知' end as 是否保税, bb.customershortname as 客户代码, 
          aa.Fab_conv_id as FAB机种,aa.mpn_desc as 客户机种,cc.residual as NPI负责人员, 
          aa.mtrl_num as 厂内机种, 
          aa.po_num as PO_NUM, 
          bb.lotid as LOT_ID, 
          bb.wafer_id as WAFER_NO, 
          bb.substrateid as WAFERID, 
          bb.passbincount as GOOD_DIES, 
          bb.failbincount as NG_DIES, 
          bb.passbincount + bb.failbincount as GROSS_DIES, 
          bb.productid as 打标码, 
          aa.Imager_Customer_Rev as 二级代码, bb.qtech_created_by as 上传人员,bb.qtech_created_date as 上传时间,  bb.qtech_lastupdate_by as 更新人员, bb.qtech_lastupdate_date as 更新时间 
     from customeroitbl_test aa 
     left join tbltsvnpiproduct cc on cc.customerptno1 = aa.mpn_desc  and  cc.qtechptno = aa.mtrl_num  and cc.customershortname = aa.customershortname and cc.residual is not null 
    inner join mappingdatatest bb 
       on to_char(aa.id) = bb.filename 
      and aa.wafer_visual_inspect = '{upload_id}'
      group by  bb.customershortname,cc.residual,aa.mtrl_num,aa.Fab_conv_id, aa.mpn_desc,aa.po_num,bb.lotid,bb.wafer_id,bb.substrateid,bb.passbincount,bb.failbincount,bb.productid,aa.Imager_Customer_Rev ,bb.substratetype,bb.qtech_created_by,bb.qtech_created_date,bb.qtech_lastupdate_by,bb.qtech_lastupdate_date 
    '''

    results = conn.OracleConn.query(sql)
    for row in results:
        result = {}
        result['id'] = str(row[0])
        result['banded'] = str(row[1])
        result['cust_code'] = str(row[2])
        result['fab_device'] = str(row[3])
        result['cust_device'] = str(row[4])
        result['npi_owner'] = str(row[5])
        result['ht_pn'] = str(row[6])
        result['po_id'] = str(row[7])
        result['lot_id'] = str(row[8])
        result['wafer_no'] = str(row[9])
        result['wafer_id'] = str(row[10])
        result['good_dies'] = str(row[11])
        result['ng_dies'] = str(row[12])
        result['gross_dies'] = str(row[13])
        result['mark_code'] = str(row[14])
        result['second_code'] = str(row[15])
        result['upload_by'] = str(row[16])
        result['upload_date'] = str(row[17])
        result['update_by'] = str(row[18])
        result['update_date'] = str(row[19])

        json_data_detail.append(result)

    dict_data['detail_data'] = json_data_detail

    return dict_data


# Parse po file
def parse_po_file(file_name, po_header):
    po_dic = get_po_config(po_header)
    if not po_dic:
        return

    file_type = po_dic['file_type']
    if file_type == 'xlsx':
        parse_xlsx_file(file_name, po_header, po_dic)


# Get Json config
def get_po_config(po_header):
    sql = "SELECT TEMPLATE_CONFIG FROM CMP_CUST_PO_TEMPLATE WHERE TEMPLATE_ID  = %s" % (
        po_header['template_id'])
    results = conn.OracleConn.query(sql)
    if not results:
        print("无法获取配置文件")
        return False
    template_config = results[0][0]
    file_dir = os.path.join(os.getcwd(), template_config)
    # print("获取到配置文件", file_dir)

    f = open(file_dir, 'r', encoding="utf-8")
    po_dic = json.load(f)
    return po_dic


# Parse xlsx file
def parse_xlsx_file(file_name, po_header, po_dic):
    df = pd.DataFrame(pd.read_excel(file_name, header=None))
    keys = po_dic['file_keys']
    po_data = []
    for index, row in df.iterrows():
        if index == 0:
            continue

        po_row_data = {}
        po_row_data['po_id'] = str(
            row[column_index_from_string(keys['po_id']['position']['col_char'])-1]).strip()
        po_row_data['fab_device'] = str(
            row[column_index_from_string(keys['fab_device']['position']['col_char'])-1]).strip()
        po_row_data['customer_device'] = str(
            row[column_index_from_string(keys['customer_device']['position']['col_char'])-1]).strip()
        po_row_data['lot_id'] = str(
            row[column_index_from_string(keys['lot_id']['position']['col_char'])-1]).strip()
        po_row_data['wafer_id'] = str(
            row[column_index_from_string(keys['wafer_id']['position']['col_char'])-1]).strip()
        po_row_data['wafer_qty'] = str(
            row[column_index_from_string(keys['wafer_qty']['position']['col_char'])-1]).strip()
        # print(po_row_data)
        po_data.append(po_row_data)

    print(po_data)
    check_po_data(po_header, po_dic, po_data)
    save_po_data(po_header, po_dic, po_data)


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

    return result2


# Check po data
def check_po_data(po_header, po_dic, po_data):
    pass


# Save po data
def save_po_data(po_header, po_dic, po_data):
    global user_progress
    user_progress[po_header['user_upload_progress']] = 0
    num = 0
    for item in po_data:
        wafer_id_list = get_wafer_list(item['wafer_id'])
        num = num + len(wafer_id_list)

    # sql = "select PO_ITEM_SEQ.nextval from dual"
    # po_header['upload_id'] = conn.OracleConn.query(sql)[0][0]

    for item in po_data:
        wafer_id_list = get_wafer_list(item['wafer_id'])
        # print(wafer_id_list)
        wafer_qty = item['wafer_qty']
        if len(wafer_id_list) != int(wafer_qty):
            print('wafer qty和wafer list明细不一致')
            return False

        for i in range(len(wafer_id_list)):
            insert_po_data(wafer_id_list[i], po_header, item)
            user_progress[po_header['user_upload_progress']
                          ] = user_progress[po_header['user_upload_progress']] + 100 / float(num)


def insert_po_data(wafer_id, po_header, po_data):
    if wafer_id.isdigit() and (len(wafer_id) == 1):
        wafer_id = ('00' + wafer_id)[-2:]
    sql = "select CustomerBCtbl_SEQ.nextval ID from dual"
    max_id = conn.OracleConn.query(sql)[0][0]
    upload_id = po_header['upload_id']
    # bonded = 'A' if (po_header['is_bonded'] == '保税') else 'B'
    bonded = 'A' if po_header['is_bonded'] == '保税' else 'B'

    mark_id = 'ABC' + wafer_id
    lot_id = po_data['lot_id']
    cust_code = po_header['cust_code']
    po_id = po_data['po_id']
    cust_device = po_data['customer_device']
    fab_device = po_data['fab_device']
    ret = get_cust_pn_info(cust_device, fab_device)
    ht_pn = ret['ht_pn'] if ret else ''
    passbin_count = ret['gross_dies'] if ret else ''
    failbin_count = '0'
    product_id = ret['product_id'] if ret else ''

    # Delete old wafer data
    delete_po_data('1', lot_id+wafer_id)
    # Oracle insert
    sql = ''' insert into mappingDataTest(id,substrateid,substratetype,productid,micronlotid,lotid,Wafer_ID,passbincount,
              failbincount,CustomerShortName,flag,Qtech_Created_By,Qtech_Created_Date,filename)
              values( mappingData_SEQ.Nextval,'%s','%s','%s','%s',
                     '%s','%s','%s','%s','%s','Y','07885',sysdate,'%s')
          ''' % (lot_id+wafer_id, bonded, mark_id, mark_id, lot_id, wafer_id, passbin_count, failbin_count, cust_code, max_id)

    conn.OracleConn.exec(sql)

    sql = f''' insert into CustomerOItbl_test(id,po_num,wafer_visual_inspect,source_batch_id,SHIP_SITE,Test_site,FAB_CONV_ID,mpn_desc,
            Imager_Customer_Rev,Created_Date,mtrl_num,CustomerShortName,flag,Qtech_Created_By,Qtech_Created_Date,
            probe_ship_part_type,RETICLE_LEVEL_71,RETICLE_LEVEL_72,RETICLE_LEVEL_73,ASSEMBLY_FACILITY,BATCH_COMMENT_ASSY,
            jobno,date_code,shipping_mst_level,shipping_mst_260,TARGET_WAF_THICKNESS,COMP_CODE,SHIP_COMMENT)
            values( {max_id},'{po_id}','{upload_id}','{lot_id}','{cust_code}','HTKS','{fab_device}','{cust_device}','','','{ht_pn}','{cust_code}',
            'Y','07885',sysdate,'','','','','','','','','','','{lot_id}','HTKS','')
          '''

    conn.OracleConn.exec(sql)

    # Sqlserver insert
    sql = ''' insert into [ERPBASE].[dbo].[tblmappingData](substrateid,substratetype,productid,lotid,Wafer_ID,passbincount,
              failbincount,CustomerShortName,flag,Qtech_Created_By,Qtech_Created_Date,filename)
              values('%s','%s','%s','%s','%s','%s','0','%s','Y','07885',getdate(),'%s')
          ''' % (lot_id+wafer_id, bonded, mark_id, lot_id, wafer_id, passbin_count, cust_code, max_id)

    conn.MssConn.exec(sql)

    sql = f''' insert into [ERPBASE].[dbo].[tblCustomerOI](id,po_num,wafer_visual_inspect,source_batch_id,SHIP_SITE,Test_site,FAB_CONV_ID,mpn_desc,
            Imager_Customer_Rev,Created_Date,mtrl_num,CustomerShortName,flag,Qtech_Created_By,Qtech_Created_Date,
            probe_ship_part_type,RETICLE_LEVEL_71,RETICLE_LEVEL_72,RETICLE_LEVEL_73,ASSEMBLY_FACILITY,BATCH_COMMENT_ASSY,
            jobno,date_code,shipping_mst_level,shipping_mst_260,TARGET_WAF_THICKNESS,COMP_CODE,SHIP_COMMENT)
            values( {max_id},'{po_id}','{upload_id}','{lot_id}','{cust_code}','HTKS','{fab_device}','{cust_device}','','','{ht_pn}','{cust_code}',
            'Y','07885',getdate(),'','','','','','','','','','','{lot_id}','HTKS','')
          '''
    conn.MssConn.exec(sql)


def get_cust_pn_info(cust_device, fab_device):
    sql = "SELECT QTECHPTNO,CUSTOMERDIEQTY,QTECHPTNO2 FROM TBLTSVNPIPRODUCT t  WHERE t.CUSTOMERPTNO1  = '%s' AND CUSTOMERPTNO2  = '%s'" % (
        cust_device, fab_device)
    results = conn.OracleConn.query(sql)

    if not results:
        print('无法获取NPI对照表对应机种信息')
        return False

    ret = {}
    ret['ht_pn'] = results[0][0]
    ret['gross_dies'] = results[0][1]
    ret['product_id'] = results[0][2]
    return ret


# Delete po data
def delete_po_data(flag_, del_id):
    if flag_ == '0':
        # Delete by lot
        sql = f"delete from mappingdatatest where lotid = '{del_id}' "
        conn.OracleConn.exec(sql)
        sql = f"delete from CustomerOItbl_test where source_batch_id = '{del_id}' "
        conn.OracleConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblmappingData] where lotid = '{del_id} "
        conn.MssConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblCustomerOI] where source_batch_id = '{del_id}' "
        conn.MssConn.exec(sql)
    elif flag_ == '1':
        # Delete by wafer
        sql = f"delete from CustomerOItbl_test where to_char(id) in (select filename from mappingdatatest where substrateid = '{del_id}') "
        conn.OracleConn.exec(sql)
        sql = f"delete from mappingdatatest where substrateid = '{del_id}' "
        conn.OracleConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblCustomerOI] where CONVERT(char(20),id) in (select filename from [ERPBASE].[dbo].[tblmappingData] where substrateid = '{del_id}') "
        conn.MssConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblmappingData] where substrateid = '{del_id}' "
        conn.MssConn.exec(sql)
    elif flag_ == '2':
        # Delete by uploadid
        sql = f"delete from mappingdatatest where filename in (select to_char(id) from CustomerOItbl_test where wafer_visual_inspect = '{del_id}') "
        conn.OracleConn.exec(sql)
        sql = f"delete from CustomerOItbl_test where wafer_visual_inspect = '{del_id}' "
        conn.OracleConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblmappingData] where filename in (select CONVERT(char(20),id)  from [ERPBASE].[dbo].[tblCustomerOI] where wafer_visual_inspect = '{del_id}') "
        conn.MssConn.exec(sql)
        sql = f"delete from [ERPBASE].[dbo].[tblCustomerOI] where wafer_visual_inspect = '{del_id}' "
        conn.MssConn.exec(sql)

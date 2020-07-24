'''
@File    :   main.py
@Time    :   2020/07/09 15:30:24
@Author  :   Tang wei
@Version :   1.0
@Contact :   wei.tang_ks@ht-tech.com
@License :   (C)Copyright 2020-2021
@Desc    :   None
'''
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask_cors import CORS
import handle as h
import json

# CORS
app = Flask(__name__)
CORS(app)


# Login
@app.route('/login', methods=['GET', 'POST'])
def r_login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        if h.check_account(username, password):
            return 'success'
        else:
            return '用户名或密码不正确'


# Get customer list
@app.route('/cust_code_list', methods=['GET', 'POST'])
def r_get_cust_code_list():
    if request.method == 'GET':
        json_data = h.get_cust_code_list()

        return make_response(jsonify(json_data), 200)


# Get customer po template
@app.route('/po_template', methods=['GET', 'POST'])
def r_get_po_template():
    if request.method == 'POST':
        cust_code = request.values.get('custCode')
        json_data = h.get_po_template(cust_code)
        return make_response(jsonify(json_data), 200)



# Upload po file
@app.route('/upload_po_file', methods=['GET', 'POST'])
def r_upload_po_file():
    if request.method == 'POST':
        f = request.files.get('poFile')
        po_header = {}
        po_header['user_name'] = request.values.get('userName')
        po_header['cust_code'] = request.values.get('custCode')
        po_header['po_type'] = request.values.get('poType')
        po_header['bonded_type'] = request.values.get('bondedType')
        po_header['offer_sheet'] = request.values.get('offerSheet')
        po_header['need_delay'] = request.values.get('needDelay')
        po_header['delay_days'] = request.values.get('delayDays')
        po_header['need_mail_tip'] = request.values.get('needMailTip')
        po_header['mail_tip'] = request.values.get('mailTip')
        po_header['file_id'] = request.values.get('fileID')
        po_header['err_desc'] = ''

        json_data = h.upload_po_file(f, po_header)

        return make_response(jsonify(json_data), 200)


# Update progress
@app.route('/update_progress', methods=['GET', 'POST'])
def r_update_progress():
    if request.method == 'GET':
        user_key = request.args.get('userKey')
        num = h.get_progress(user_key)
        return make_response(jsonify({"progress": num}), 200)


# Run server
if __name__ == "__main__":
    app.run(host='10.160.31.115', debug=True, threaded=True)

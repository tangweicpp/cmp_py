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
@app.route('/cust_list', methods=['GET', 'POST'])
def r_get_custcode_list():
    if request.method == 'GET':
        json_data = h.get_custcode_list()

        return make_response(jsonify(json_data), 200)


# Get customer po template
@app.route('/po_template', methods=['GET', 'POST'])
def r_get_po_template():
    if request.method == 'POST':
        custcode = request.values.get('custcode')
        json_data = h.get_po_template(custcode)

        return make_response(jsonify(json_data), 200)


# Upload po file
@app.route('/upload_po_file', methods=['GET', 'POST'])
def upload_po_file():
    if request.method == 'POST':
        f = request.files.get('poFile')
        po_header = {}
        po_header['cust_code'] = request.values.get('custCode')
        po_header['po_type'] = request.values.get('poType')
        po_header['po_price'] = request.values.get('poPrice')
        po_header['is_delay'] = request.values.get('isDelay')
        po_header['delay_days'] = request.values.get('delayDays')
        po_header['template_id'] = request.values.get('templateId')
        po_header['is_bonded'] = request.values.get('isBonded')
        po_header['mail_content'] = request.values.get('mailContent')
        po_header['user_upload_progress'] = request.values.get(
            'userUploadRandom')
        json_data = h.upload_po_file(f, po_header)

        return make_response(jsonify(json_data), 200)


# Update progress
@app.route('/update_progress', methods=['GET', 'POST'])
def r_update_progress():
    if request.method == 'GET':
        user_key = request.args.get('userKey')
        num = str(h.get_progress(user_key))
        return str(num)


# Run server
if __name__ == "__main__":
    app.run(host='10.160.31.115', debug=True, threaded=True)

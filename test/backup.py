from flask import Flask
from flask import jsonify
from flask import request
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
# from flask.wrappers import Request
from flask_cors import CORS
from flask import make_response
import connect_db as conn
import time
import os
import logging

logging.basicConfig(level=logging.INFO, filename='erp.txt',
                    format='%(asctime)s :: %(funcName)s :: %(levelname)s :: %(message)s')

app = Flask(__name__)
CORS(app)
# CORS(app, supports_credentials=True)
# cors = CORS(app, resources={r"/login": {"origins": "*"}})

# cors = CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, supports_credentials=True)
# cors = CORS(app)

@app.route('/upload',methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    # f = request.files.get('file')
    # # f.save(secure_filename(f.filename))
    # f.save(f.filename)
    # response = {
    #   'msg': 'Hello, Python !'
    # }
    # # return Response(json.dumps(response), mimetype='application/json')
    # return jsonify(response)
    file_dir = os.path.join(os.getcwd(),'custcode/37/PO')
    
    # 目标路径如果不存在则创建
    if not os.path.exists(file_dir):
      os.makedirs(file_dir)
    # 获取上传文件
    f = request.files.get('file')
    # print(f.__dict__)
    if f:
      # 文件保存路径+文件名
      file_path = os.path.join(file_dir,f.filename)
      # 保存
      f.save(file_path)
      return '文件保存成功'
    return '文件获取失败'





@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.values.get('username')
    password = request.values.get('password')

    sql = "select 用户号 from erpbase..tblOperatorData where 用户号 = '%s' and 密码= '%s' " % (username, password)
    results = conn.MssConn.query(sql)
    if not results:
        logging.warning('查询不到数据')
        print('查询不到数据')
        return '账号不存在'
    return 'success'

    # if (username == '07885') and (password == '.7885'):
    #   return 'success'
    # else:
    #   return '账号不存在'
  else:
    user = request.args.get('username')
    password = request.args.get('password')
    if (user == '07885') and (password == '.7885'):
      return 'success'
    else:
      return '账号不存在'

# 启动运行
if __name__ == '__main__':
    app.run(host='10.160.31.115',debug=True)   # 这样子会直接运行在本地服务器，也即是 localhost:5000
  #  app.run(debug=True) # 这里可通过 host 指定在公网IP上运行
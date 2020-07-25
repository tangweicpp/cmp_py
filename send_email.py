'''
@File    :   send_email.py
@Time    :   2020/07/21 15:49:01
@Author  :   Tony Tang
@Version :   1.0
@Contact :   wei.tang_ks@ht-tech.com
@License :   (C)Copyright 2020-2021, Liugroup-NLPR-CASIA
@Desc    :   None
'''
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# send_email
def send_email(subject, body, file_path, to_reciver, cc_reciver):
    sender = 'sqladmin@ht-tech.com'
    reciver = to_reciver + cc_reciver

    message = MIMEMultipart()
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender
    message['To'] = ','.join(to_reciver)
    message['Cc'] = ','.join(cc_reciver)

    message.attach(MIMEText(body, 'html', 'utf-8'))
    # if file_path != '':
    #     message.attach(MIMEText(body, 'html', 'utf-8'))
    # else:
    #     message.attach(MIMEText(body, 'plain', 'utf-8'))

    # if file_path != '':
    #     xmlApart = MIMEApplication(open(file_path, 'rb').read())
    #     file_name = file_path.split('/')[-1]
    #     xmlApart.add_header('Content-Disposition',
    #                         'attachment', filename=file_name)
    #     message.attach(xmlApart)

    for i in range(len(file_path)):
        xmlApart = MIMEApplication(open(file_path[i], 'rb').read())
        file_name = file_path[i].split('/')[-1]
        xmlApart.add_header('Content-Disposition',
                            'attachment', filename=file_name)
        message.attach(xmlApart)

    try:
        smtpObj = smtplib.SMTP('ksmail.ht-tech.com:587')
        smtpObj.login('sqladmin@ht-tech.com', 'ksitadmin')
        smtpObj.sendmail(sender, reciver, message.as_string())
        print("Success to send email!!!")
        smtpObj.quit()
        return True
    except smtplib.SMTPException as e:
        print('error:', e)
        return False

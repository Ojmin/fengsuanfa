# coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_mail(text):
    smtpserver = 'smtp.163.com'
    username = '13099920823@163.com'
    password = 'mimashi2'
    sender = '13099920823@163.com'

    receiver = ['1543461999@qq.com', '13099920823@163.com']

    subject = 'Server Unusual'

    # 构造邮件对象MIMEMultipart对象
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = '13099920823@163.com <13099920823@163.com>'

    msg['To'] = ";".join(receiver)
    # 构造文字内容
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
if __name__ == '__main__':
    send_mail('hello world')
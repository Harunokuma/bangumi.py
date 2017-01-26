#!/usr/bin/python3
# coding:utf-8
#=========================================================================
# 加密SMTP
#
# 使用标准的25端口连接SMTP服务器时，使用的是明文传输，发送邮件的整个过程可能会被窃听。要更安全地发送邮件，可以加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件。  
#=========================================================================

from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr, formatdate
import os
import smtplib
import logging

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendTorrent(toAddrs, torrents):
    logger = logging.getLogger("bangumiLogger")
    abspath = os.path.dirname(__file__)
    torrentDirPath = os.path.join(abspath, "torrent")

    # 接收参数: 发件人地址
    from_addr = 'kumanobangumi@163.com'
    # 接收参数: 客户端授权密码
    passwd = 'password123'
    # 接收参数: 收件人地址,可多个
    to_addrs = toAddrs
    # 接收参数: SMTP服务器(注意:是发件人的smtp服务器)
    smtp_server = 'smtp.163.com'


    # 接收参数: 邮件主题
    subject = '有新番更新啦'

    # 接收参数: 邮件正文
    # html = '本次更新的新番有：<br>'
    html = ''
    for torrent in torrents:
        html += torrent['title'] + torrent['num'] + '<br>'
        html += 'Magnet link: ' + torrent['maglink'] + '<br>'

    # 带附件邮件
    # 指定subtype为alternative，同时支持html和plain格式
    msg = MIMEMultipart('alternative')
    
    html = '<html><body><h1>本次更新的新番有：</h1><p>' + html + '</p></body></html>'
    msg.attach(MIMEText(html, 'html', 'utf-8'))         # HTML

    # for torrent in torrents:
    #     fileName = '['+torrent['title']+']'+'['+torrent['num']+']'+'.torrent'
    #     filePath = os.path.join(torrentDirPath, fileName)
    #     part = MIMEApplication(open(filePath,'rb').read())
    #     part.add_header('Content-Disposition','attachment',fileName = fileName)
    #     msg.attach(part)

    msg['From'] = _format_addr(from_addr)
    msg['To'] = _format_addr(to_addrs)
    msg['Subject'] = Header(str(subject), 'utf-8').encode()
    msg['Date'] = formatdate()


    #=========================================================================
    # 发送邮件
    #=========================================================================
    try:
        # SMTP服务器设置(地址,端口):
        server = smtplib.SMTP_SSL(smtp_server, 465)
        # 连接SMTP服务器(发件人地址, 客户端授权密码)
        server.login(from_addr, passwd)
        # 发送邮件
        server.sendmail(from_addr, to_addrs, msg.as_string())

        for torrent in torrents:
            logger.info("Send a mail to %s, which include [%s][%s]" % (to_addrs, torrent['title'], torrent['num']))
        # print('Send a mail to %s' % to_addrs)

    except smtplib.SMTPException as e:
        logger.error("Send mail to %s failed" % to_addrs, exc_info=True)
        # print(e)
        # print('Send mail fail')

    finally:
        # 退出SMTP服务器
        server.quit()
# -*- encode: utf-8 -*-

import hashlib
import random
import xml.etree.ElementTree as ET
import requests
import bs4
import joke
from flask import Flask, request, make_response

app = Flask(__name__)


def parserMsg(msg):
    def parserData(content, contentType):
        if contentType == 'text':
            return content.text


    xml = ET.fromstring(msg)
    data = {
        'toUserName': xml.find('ToUserName').text,
        'fromUserName': xml.find('FromUserName').text,
        'createTime': xml.find('CreateTime').text,
        'msgType': xml.find('MsgType').text,
        'msgContent': parserData(xml.find('Content'), xml.find('MsgType').text), 'msgId': xml.find('MsgId').text,
    }
    return data

def constructMsg(fromUserName=None, toUserName=None, createTime=None, msgType=None, msgContent=None):
    allowType = ['text', 'image']
    if msgType not in allowType:
        return None
    return '''
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>
            ''' % (
                fromUserName,
                toUserName,
                createTime,
                msgType,
                msgContent
                )



@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        print('Get coming...')
        data = request.args
        token = 'echodlnu'
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        # print(token, signature, timestamp, nonce, echostr)
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s).encode('utf-8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)

    if request.method == 'POST':
        # 获取微信发过来的消息
        xml_str = request.stream.read()

        # 解析成xml
        msg = parserMsg(xml_str)

        # 配置回复信息
        fromUserName=msg['fromUserName']
        toUserName=msg['toUserName']
        createTime=msg['createTime']
        msgType='text'
        msgContent =  joke.getJokes(
                                random.randint(1, 13),
                                random.randint(1, 25)
                            )  if msg['msgType'] == 'text'\
                               else u'Unknow message type, Please checkout'

        return constructMsg(
                fromUserName=fromUserName,
                toUserName=toUserName,
                createTime=createTime,
                msgType='text',
                msgContent = msgContent,
            )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)



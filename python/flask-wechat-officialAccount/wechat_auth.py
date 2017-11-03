from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/', method=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        print('Get coming...')
        data = request.args()
        token = 'echodlnu'
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexddigest() == signature):
            return make_response(echostr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



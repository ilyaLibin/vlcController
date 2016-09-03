# wget http://0.0.0.0:5000/check --post-data "&pass=1234&port=9033"

import json
from time import sleep
import pdb
import os
from subprocess import Popen, PIPE
from flask import request, url_for
from flask_api import FlaskAPI, status
from vlcremote import VLCRemote
from exception import InvalidUsage
import multiprocessing
app = FlaskAPI(__name__)
vlc = VLCRemote()

proc = None

@app.route('/switch', methods=['POST'])
def switch():
    global proc
    value = request.form.get('value', type=str)

    if (proc is not None):
        proc.kill()

    if (value == 'on'):
        proc = Popen(["python", "recognize.py"], shell=False, stdin=PIPE, stderr=PIPE)
        outs, errs = None, None
        try:
            outs, errs = proc.communicate(timeout=4)
        except:
            print("the process alive!!!")

        print("outs: {0}".format(outs))
        print("errs: {0}".format(errs))
        if (errs is not None):
            content = {'error': "can't connect"}
            return content, status.HTTP_406_NOT_ACCEPTABLE

# HTTP_400_BAD_REQUEST
# HTTP_406_NOT_ACCEPTABLE
    return {}

@app.route('/check', methods=['POST'])
def connect():
    vlc = VLCRemote()
    port = request.form.get('port', type=str)
    password = request.form.get('pass', type=str)

    try:
        vlc.login(port, password)
    except Exception as e:
        print("Except")
        raise InvalidUsage('Can not connect to vlc', status_code=400)

    with open('credentials.txt', 'w') as file:
        json.dump({'port': port, 'password': password}, file)

    return {}

def read_credentials():
    params = {}
    with open('credentials.txt', 'r') as f:
        params = json.load(f)

    return params


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

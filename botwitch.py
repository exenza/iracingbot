import os
import requests
import json
import datetime
import webbrowser
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import argparse
import sys
sys.stdout = open('my_stdout.log', 'w')
sys.stderr = open('my_stderr.log', 'w')

cwd=os.path.dirname(os.path.realpath(__file__))

#Configure your client
client_id="ee7g573dkwms04ijbb4nrah3jeeurh"
channel= ""
code= ""
token = ""
sender_id = ""
data_json = ""

def code_webserver():
    global data_json

    print("Initiating webserver")
    print(json.dumps(data_json))
    hostName = "localhost"
    serverPort = 3000

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):

            try:
                file_to_open = open('authcode.html').read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
            except Exception as error:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
                self.wfile.write(bytes("<html><head><title>iracingbot</title></head>", "utf-8"))
                print("49")
                exit()
            try:
                parsed_path = urllib.parse.parse_qs(self.path.replace('/?', '', 1))
                code=parsed_path['code'][0]
                update_data_json('code', code)
                exit()
                
            except Exception as error:
                print("58")
                exit()
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server closed")

#Get token
def get_token():
    global data_json

    url = 'https://5j5dlb2eis3ajgd6nmj52e3fqy0bkezq.lambda-url.eu-west-1.on.aws/'
    headers = {'Content-Type': 'application/json'}
    payload = {'code': data_json['code']}
    r = requests.get(url, headers=headers, json=payload)

    if r.status_code == 401:
        url = 'https://5j5dlb2eis3ajgd6nmj52e3fqy0bkezq.lambda-url.eu-west-1.on.aws/'
        headers = {'Content-Type': 'application/json'}
        payload = {'refresh_token': data_json['refresh_token']}
        r = requests.get(url, headers=headers, json=payload)

    if r.status_code == 200:
        data_json['token'] = r.json()['access_token']
        data_json['refresh_token'] = r.json()['refresh_token']
        update_data_json('token', data_json['token'])
        update_data_json('refresh_token', data_json['refresh_token'])
    else:
        if r.json()['message'] == "Invalid authorization code":
            get_code()
    print("Exiting get token")
    exit()


#Get sender_id
def get_sender_id():
    global data_json
    global client_id

    url = 'https://api.twitch.tv/helix/users'
    payload = {'login':data_json['channel']}
    headers = {'Authorization':'Bearer '+data_json['token'],'Client-Id':client_id}
    r = requests.get(url, params=payload, headers=headers)
    user = r.json()
    try:
        sender_id=(user['data'][0]['id'])
        return(update_data_json('sender_id', sender_id))
    except Exception as error:
        print(json.dumps(user))
        return(error)

def get_code():
    global data_json
    global client_id

    url = 'https://id.twitch.tv/oauth2/authorize?response_type=code&client_id='+client_id+'&redirect_uri=http://localhost:3000&scope=user%3Awrite%3Achat%20user%3Abot%20channel%3Amanage%3Abroadcast'
    webbrowser.open_new(url)
    try:
        webserver=threading.Thread(target=code_webserver)
        webserver.daemon=True
        webserver.start()
    except Exception as error:
        print("125")
        print(error)
    timeout=120
    print("Waiting for code")
    update_data_json("code", "")
    while not data_json['code']:
        time.sleep(1)
        print("Waiting for code, timing out in "+str(timeout))
        timeout = timeout -1
        if timeout == 0:
            exit("Can't get Twitch auth code")

########################################## 
def new_data_json():
    print("Write new empty data.json")
    with open("data.json", "w") as outfile:
        outfile.write(json.dumps({'channel':'', 'code':'', 'token':'','refresh_token':'','sender_id':''}, indent=2))
    exit("A new data.json file has been created, provide your channel name in the file.")

def update_data_json(key, value):
    global data_json

    data_json[key]=value
    try:
        with open("data.json", "w") as outfile:
            outfile.write(json.dumps(data_json, indent=2))
            return True
    except Exception as error:
        print(error)
        return error

#Check data.json exist
def load_data_json():
    global data_json

    try:
        with open('data.json') as data_json:
            data_json = json.load(data_json)
    except Exception as error:
        print(error)
        new_data_json()

load_data_json()

def initialise(error):
    global channel
    global code
    global token
    global sender_id

    print(error)
    print("Initialising application")
    print("Getting token")
    get_token()
    print("Getting sender id")
    get_sender_id()

def start():
    global data_json

    try:
        try:
            channel=data_json['channel']
            print("Getting channel from data.json")
            if not channel:
                exit("Fatal error, Twitch channel name not provided, edit data.json and retry.")
        except Exception as error:
                new_data_json()

        try:
            code=data_json['code']
            print("Getting code from data.json")
            if not code:
                get_code()
        except Exception as error:
            print("Unable to get code: "+str(error))
            get_code()

        try:       
            token=data_json['token']
            print("Getting token from data.json")
            if not token:
                get_token()
        except Exception as errror:
            print(error)
            get_token()

        try:
            sender_id=data_json['sender_id']
            print("Getting sender_id from data.json")
            if not sender_id:
                get_sender_id()
        except Exception as error:
            print(error)
            get_sender_id()


    except Exception as error:
        initialise(error)


try:
    start()
except Exception as error:
    print(error)


def api_error(caller, error):
    global data_json

    print("From: "+caller+" - "+json.dumps(error))
    try:
        message = error['message']
    except Exception as error:
        exit("From "+caller+" unknown error: "+str(error))
    if message == "Invalid OAuth token":
        print("Refreshing token")
        get_token()
        return True
    if message == "The sender must have authorized the app with the user:write:chat and user:bot scopes.":
        print("Get new Twitch authorization")
        data_json['code'] = ""
        get_code()
        return True

def message(body):
    global data_json
    global client_id

    url = 'https://api.twitch.tv/helix/chat/messages'
    payload =   {
                 'broadcaster_id':data_json['sender_id'],
                 'sender_id':data_json['sender_id'],
                 'message':body,
                }
    headers =   {
                'Authorization':'Bearer '+data_json['token'],
                'Client-Id':client_id,
                'Content-Type':'application/json'
                }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())
    if r.status_code != 200:
        retry=api_error("message()", r.json())
        if retry:
            "Print message retry"
            message(body)

def stream_info(payload):
    global data_json
    global client_id 

    url = 'https://api.twitch.tv/helix/channels?broadcaster_id='+data_json['sender_id']
    headers =   {
                'Authorization':'Bearer '+data_json['token'],
                'Client-Id':client_id,
                'Content-Type':'application/json'
                }
    r = requests.patch(url, data=json.dumps(payload), headers=headers)

#Arguments
parser = argparse.ArgumentParser()

parser.add_argument('-m', "--message",)
parser.add_argument('-g', "--game",)
parser.add_argument('-t', "--title",)
parser.add_argument('-s', "--tags",)

args = parser.parse_args()

if args.message:
    message(args.message)

stream_payload={}
if args.game: #iracing is 19554
    stream_payload['game_id']=args.game

if args.title:
    stream_payload['title']=args.title

if args.tags:
    stream_payload['tags']=[args.tags]

if stream_payload:
    stream_info(stream_payload)
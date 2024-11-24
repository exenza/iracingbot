import json
import os
import requests

response = {}
status_code = 200

def get_token(code, client_id, client_secret):
    global status_code
    
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret, 
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:3000'
    }
    r = requests.post(url, data=payload)
    status_code = r.status_code
    response = r.json()
    return response

def get_refresh_token(refresh_token, client_id, client_secret):
    global status_code

    url = 'https://id.twitch.tv/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'client_id': client_id,
        'client_secret': client_secret, 
        'refresh_token': urlencode(refresh_token),
        'grant_type': 'refresh_token'
    }
    r = requests.post(url, headers=headers, data=payload)
    status_code = r.status_code
    response = r.json()
    return response

def lambda_handler(event, context):
    global response
    global status_code

    try:
        client_id = os.environ['client_id']
        client_secret = os.environ['client_secret']
    except:
        status_code = 400
        response['message'] = "client_id or client_secret not found"
        return {
            'statusCode': status_code,
            'body': json.dumps(response)
        }

    # Get code or refresh_token from event
    try:
        code = json.loads(event['body'])['code']
        response=get_token(code, client_id, client_secret)
    except:
        try:
            refresh_token = json.loads(event['body'])['refresh_token']
            response=get_refresh_token(refresh_token, client_id, client_secret)
            return {
                'statusCode': status_code,
                'body': json.dumps(response)
            }
        except:
            status_code = 400
            response['message'] = "Code or refresh_token not found"
            return {
                'statusCode': status_code,
                'body': json.dumps(response)
            }


    # TODO implement
    return {
        'statusCode': status_code,
        'body': json.dumps(response)
    }
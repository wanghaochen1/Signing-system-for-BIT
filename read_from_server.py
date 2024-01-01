import json

def identify_result(s):
    try:
        receivedata = s.recv(10240)
        json_str = receivedata.decode('utf-8')
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print('Failed to decode JSON data')
        return False
    #如果是登陆信息：
    if data['usage'] == 'login':
        return data['result']
    
import json

#client端的json格式：(client端发出的信号)
#data={
#    'usage':'',
#    'stu_num':'',
#    'sign_time':''}
def message_read_from_client(json_str):
    data = json.loads(json_str.decode())
    usage=data['usage']
    stu_num=data['stu_num']
    sign_time=data['sign_time']
    return usage,stu_num,sign_time


#server端的json格式：(server端发出的信号)
#data={
#    'usage':'',
#    'sign_time_history':''}
def message_read_form_server(json_str):
    data = json.loads(json_str.decode())
    usage=data['usage']
    sign_time_history=data['sign_time_history']
    return usage,sign_time_history

    

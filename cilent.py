import socket
import sys
import tkinter as tk
import GUI_fun

s=None#定义全局变量s，用于指定socket
Var_Pass=False
#定义socket连接函数
def socket_connect(host,port):
    global s #给全局的s赋值
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except:
        print(f"出现问题\n")
        sys.exit(1)#退出程序
    print("\n已连接到server\n")
    return s

#定义socket发送和接收函数
def socket_send_recv(send_data):
    global s#使用全局变量socket
    s.sendall(send_data.encode())#发送数据
    recv_data = s.recv(1024)#接收数据
    return recv_data.decode()


#定义登陆认证函数
def comp(window_connect,stu_num,stu_password):
    global Var_Pass#使用全局的Var_Pass
    #测试能否连接到server
    print("\n正在等待老师打开签到连接\n")
    socket_connect('192.168.21.216', 12345)
    print("\n可以开始签到,正在进行登陆认证\n")
    #检查账号密码是否正确
    if stu_num=='' or stu_password=='':
        print("\n学号或密码不能为空\n")
        Var_Pass=False
        return 
    elif stu_num != '1120210529':
        print("\n请使用自己的的账号\n")
        Var_Pass=False
        return 
    elif stu_password != '123456':
        print("\n密码错误\n")
        Var_Pass=False
        return 
    else:
        print("\n登陆成功\n")
        Var_Pass=True
        window_connect.destroy()
        return 
#定义初始连接界面
def create_window():
    window_connect=tk.Tk()
    window_connect.title("登陆界面")
    window_connect.geometry("500x500+1000+100")
    #创建标签
    tk.Label(window_connect,text="统一身份认证登陆",bg='maroon',fg='white',font=('宋体',20),width=30,height=2).pack()

    #定义学号输入框
    tk.Label(window_connect,text="学号",font=('宋体',20),width=30).pack()
    stu_num=tk.Entry(window_connect,show=None,font=('宋体',20),width=15)
    stu_num.pack(anchor='center')  # Center-align the input field

    #定义密码输入框
    tk.Label(window_connect,text="密码",font=('宋体',20),width=30).pack()
    stu_password=tk.Entry(window_connect,show="*",font=('宋体',20),width=30)
    stu_password.pack(anchor='center')
    
    #定义登陆按钮
    tk.Button(window_connect,text="登陆",font=('宋体',20),width=10,command=lambda:comp(window_connect,stu_num.get(),stu_password.get())).pack()

    return window_connect

#创建主函数
window_1=create_window()
window_1.mainloop()

#判断是否成功登陆：
if Var_Pass is True:
    GUI_fun.Sign_window(s)
else:
    print("请重启界面")

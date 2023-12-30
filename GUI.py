# 第四步：设计GUI

# 1. 导入第三方库
import os
import tkinter as tk
import time
# 2. 创建屏幕窗口
windows = tk.Tk()  # 创建windows的窗口
windows.title('签到窗口')  # 窗口名称
windows.geometry('500x500+1000+100')  # 窗口大小（注：x是小写字母x，不能写乘号*），+1000+100表示窗口在屏幕上的位置

# 3. 定义功能函数
def function1():
    os.system('python capture_face.py')  # 执行python capture_face.py命令
def function2():
    os.system('python train.py')  # 执行python train.py命令
def function3():
    os.system('python sign_in.py')  # 执行python sign_in.py命令
def function4():
    os.startfile(os.getcwd()+'/签到表1.xls')  # 打开'签到表1.xls'文件
def function5():
    os.startfile(os.getcwd()+'/基于OpenCV的人脸识别说明文档.docx')  # 打开说明文档
def function6():
    windows.destroy()
def tick():#实时更新时间
    time_string = time.strftime("%Y年%m月%d日%H:%M:%S")
    clock.config(text=time_string)
    clock.after(200,tick)
# 4. 创建标签及按钮
tk.Label(windows, text='人脸识别上课签到系统', font=('黑体', 20, 'bold'), fg='white',
         bg='maroon', height=2).grid(padx=7, pady=5)

#添加时间
clock = tk.Label(windows,font = ("黑体",20,"bold"),fg = "white",bg = "blue")#实时更新时间
clock.grid(row = 1,column = 0)#放置标签
tick()#调用tick函数

tk.Button(windows,text='采 集 人 脸 图 像', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function1).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='训 练 模 型', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function2).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='识 别 签 到', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function3).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='查 看 签 到 表', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function4).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='查看项目说明文档', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function5).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='  退      出  ', font=('黑体', 20, 'bold'), fg='white',
         bg='#0D47A1', command=function6).grid(padx=7, pady=5, sticky=tk.W+tk.E)

tk.Button(windows,text='学号：2021520542   姓名：蔡徐坤', font=('仿宋', 20, 'bold'), fg='black',
         bg='white').grid(padx=20, pady=50, sticky=tk.W+tk.E)

# 5. 运行
windows.mainloop()
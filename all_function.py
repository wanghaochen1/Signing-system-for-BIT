import cv2
import os
import xlrd
from PIL import Image
import numpy as np
import xlrd,xlwt
from xlutils.copy import copy
from datetime import datetime
import cv2
import time
import send_client

#人脸采集函数
def capture_face(s):
    font = cv2.FONT_HERSHEY_SIMPLEX    # 定义字体，使用opencv中的FONT_HERSHEY_SIMPLEX字体
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # 导入人脸检测级联文件。CascadeClassifier是opencv中做人脸检测时的一个级联分类器，对输入的图片进行分类，判断图像内是否有无人脸
    try:
        current_directory = os.getcwd()
        print(f"\n当前你人脸所在的目录为:{current_directory}\n")
        if not os.path.exists('dataset'):  # 判断项目目录中是否存在dataset文件（dataset中存放采集到的人脸图像）
            print('\n你是第一次录入人脸,正在创建dataset文件夹\n')
            os.mkdir('dataset')  # 如果没有就新建立dataset文件夹
        else:
            print("\n你已经录入过人脸,正在尝试重新导入\n")
            #清空dataset文件夹
            for root, dirs, files in os.walk('dataset'):
                for name in files:
                    os.remove(os.path.join(root, name))
            print("\n已经清空dataset文件夹\n")
    except Exception as e:
        print("导入人脸出现问题,请联系管理员", str(e))
    finally:
        count = 0  # 人脸图像的初始数量

    # 3.输入学号
    student_ID = 2021520542

    # 4.采集图像
    capture = cv2.VideoCapture(0)  # 打开电脑的内置摄像头

    while capture.isOpened():  # 当摄像头打开的时候
        kk = cv2.waitKey(1)    # 等待键盘的输入，1:表示延时1ms切换到下一帧图像
        _, frame = capture.read()   # 读取摄像头内容，返回两个参数
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 将读取到的RGB图像转换为灰度图像
        faces = classifier.detectMultiScale(gray, 1.3, 5)  # 让classifier判断人脸，detectMultiScale函数可以检测出图像中的人脸，其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
        if len(faces) != 0:  # 如果找到人脸
            # 框选人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)  # 用矩形框框出人脸，xy为左上角的坐标,w为宽，h为高
                cv2.putText(frame, 'please "s" to save a picture ', (200, 450), font, 0.8, (0, 255, 255), 2)  # 在人脸图像上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细

                if kk == ord('s'):  # ord(' ')将字符转化为对应的整数（ASCII码）
                    try:
                        cv2.imwrite('dataset/caixukun.'+str(student_ID)+'.'+str(count)+'.jpg', gray[y:y+h, x:x+w])  # 保存图像
                        count += 1  # 成功框选人脸后，则样本数增加
                        print('采集了'+str(count)+'张人脸图像')
                    except Exception as e:
                        print("采集人脸文件位置出现问题", str(e))

        cv2.putText(frame, 'please "esc" to quit ', (10, 20), font, 0.8, (0, 255, 255), 2)  # 在窗口上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细

        cv2.imshow("picture from a cammre", frame)  # 打开窗口的名称
        if kk == 27:
            print('一共采集了' + str(student_ID) + '同学的' + str(count) + '张人脸图像')
            break

    # 5.退出程序
    capture.release()  # 释放变量
    cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉

#人脸训练函数

def train(s):
    # 2. 加载特征提取模型
    recognizer_create = cv2.face.LBPHFaceRecognizer_create()

    # 3. 数据处理
    def data_translate(path):
        face_data = []
        id_data = []
        file_list = [os.path.join(path, f) for f in os.listdir(path)]
        # print(file_list)
        for file in file_list:
            PIL_image = Image.open(file).convert("L")
            np_image = np.array(PIL_image, 'uint8')
            image_id = int(file.split('.')[1])
            # print(image_id)
            face_data.append(np_image)
            id_data.append(image_id)
        return face_data, id_data

    # 4. 训练模型
    Face, ID = data_translate('dataset')
    recognizer_create.train(Face, np.array(ID))
    print('训练完成')

    # 5. 保存模型
    recognizer_create.save('face_model.yml')
    print('模型已保存')

#人脸识别签到
def sign_in(s):
    def sign_name(idx, name):
        style0 = xlwt.easyxf('font:height 240,bOld on,color_index red', num_format_str='DD:MM HH:MM')  # 样式0
        style1 = xlwt.easyxf('font:height 240,bOld on,color_index blue')  # 样式1
        workbook = xlrd.open_workbook('签到表.xls')  # 读取excel文件
        newbook = copy(workbook)  # 复制文件
        newsheet = newbook.get_sheet(0)  # 在源文件上追加
        newsheet.write(idx, 4, datetime.now(), style0)  # 第idx行，第4列，写入签到时间，样式为style0（注：代码中的行列是从0开始的）
        newsheet.write(idx, 3, name, style1)   # 第idx行，第3列，写入签到学生的名字，样式为style1（（注：代码中的行列是从0开始的））

        # 设置列宽
        newsheet.col(0).width = 256 * 6  # 第0列的列宽为 256 * 6 （256为衡量单位，6表示6个字符宽度）
        newsheet.col(1).width = 256 * 12  # 第1列的列宽为 256 * 12 （256为衡量单位，12表示12个字符宽度）
        newsheet.col(2).width = 256 * 10  # 第2列的列宽为 256 * 10 （256为衡量单位，10表示10个字符宽度）
        newsheet.col(3).width = 256 * 12  # 第3列的列宽为 256 * 12 （256为衡量单位，12表示12个字符宽度）
        newsheet.col(4).width = 256 * 15  # 第4列的列宽为 256 * 15 （256为衡量单位，15表示15个字符宽度）
        newbook.save('签到表1.xls')

    # 3. 导入模块，初始化变量
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer_create = cv2.face.LBPHFaceRecognizer_create()
    recognizer_create.read('face_model.yml')  # 读取训练好的模型
    flag = 0  # 标记次数
    start_time = time.time()  # 系统时间提取
    duration = 25  # 持续时间
    ID = 'Unkonw'
    font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体，使用opencv中的FONT_HERSHEY_SIMPLEX字体

    # 4. 导入应到学生名单
    workbook = xlrd.open_workbook('签到表.xls')  # 导入考勤记录表
    worksheet = workbook.sheet_by_index(0)  # 打开工作表
    stu_num = worksheet.col_values(1)  # 提取工作表第1列，第1列为学生学号
    stu_name = worksheet.col_values(2)  # 提取工作表第2列，第2列为学生名字

    # 5.识别签到
    capture = cv2.VideoCapture(0)  # 打开摄像头

    while capture.isOpened():  # 当打开摄像头的时候
        kk = cv2.waitKey(1)  # 等待键盘的输入
        _, frame = capture.read()  # 读取摄像头内容
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 将读取到的RGB图像转换为灰度图像
        faces = classifier.detectMultiScale(gray, 1.3, 5)  # 让classifier判断人脸，detectMultiScale函数可以检测出图像中的人脸
        if len(faces) != 0:  # 如果能找到人脸
            # 框选人脸
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # 用矩形框框出人脸，xy为左上角的坐标，w为宽，h为高
                roi_face = gray[y:y + h, x:x + w]
                label, conf = recognizer_create.predict(roi_face)  # 预测出的学号和可信度
                # print(label,conf)

                if conf < 60:
                    index = [list for list, i in enumerate(stu_num) if i == str(label)]  # 得到预测学号在excel表格中所在的行数（注：index的值是从0开始的，index=3表示在excel表格中的第4行）
                    # print(index)
                    if index != []:
                        name = stu_name[index[0]]
                        ID = stu_name[index[0]]
                        flag += 1
                    else:
                        ID = 'unknow'
            cv2.putText(frame, str(ID), (x, y-10), font, 0.8, (0, 0, 255), 2)  # 添加字幕

        cv2.putText(frame, 'press "esc" to quit ', (10, 20), font, 0.8, (0, 255, 255), 2)  # 在窗口上添加文字，参数依次表示：图像、要添加的文字、文字的位置、字体、字体大小、颜色、粗细
        cv2.imshow("picture from a cammre", frame)  # 打开窗口的名称
        if flag > 5:
            sign_name(index[0], name)
            print('签到成功')
            break
        if time.time()-start_time > duration:  # 如果超时，则签到失败
            print('签到失败！')
            break
        if kk == 27:  # 如果退出
            print('程序被终止，请重新签到！')
            break

    # 6.退出程序
    capture.release()  # 释放变量
    cv2.destroyAllWindows()  # 检查有无打开窗口，有的话关掉
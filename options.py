import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import numpy as np
import face_recognition as fr
import pickle
import time
import tkinter.font as tkFont
from game import *


# must be n, ne, e, se, s, sw, w, nw, or center
# 身份验证成功后的等待时间
KEEP_TIME = 3000  # 身份验证成功后的等待时间（用于演示）
FPS_TIME = 2  #计算FPS的时间精度,默认为“2”
LIGHT_LEVEL = 135  # 当图像亮度大于此值时，采用最大值
SAMPLE = 1  # 人脸编码采样频率间隔，越大等待时间越长，默认为'1'

START_GAME_FLAG = 0  #游戏开关，1则开始，0则不开始

# 窗口的大小
WINDOW_SIZE = "700x600+333+70"
# 字体
FONT = cv2.FONT_HERSHEY_SIMPLEX  # 显示用字体
# FONT1 = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
# 加载 用于识别人脸的haar特征文件
FACE_XML = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')

# 用户信息存放路径
USERS_INFOR_PATH = "files/usrs_info.pkl"
# 人脸编码存放路径
ENCODER_PATH = "files/face_data_dic.pkl"
# 日志文件存放路径
LOG_PATH = "logs/"


# 颜色
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLUE_GREEN = (155,155,0)
BLUE_RED = (155,0,155)
GREEN_RED = (0,155,155)


# 告警
ERROR0 = "ERROR"
ERROR1 = "Wrong Passward!"
ERROR2 = "User Dosn`t Exist!"
ERROR3 = "No such file ERROR 003: usrs_info.pkl!"
ERROR4 = "No such file ERROR 004: usrs_info.pkl!"
ERROR5 = "Passward and the confirm passward must be the same!"
ERROR6 = "No such file ERROR 006: files/face_data_dic.pkl!"
ERROR7 = "ERROR7 video_loop:Please sign up!"
ERROR8 = "ERROR 8:Unknown ERROR! "
NO_PIC = "Cannot Catch any picture"

# 当没有识别出用户时显示
UNKNOWN = "Unknown"
# 识别出用户时显示
HELLO_FACE = "Hello!"
# 用于在摄像头显示上方提示信息
TOPTEXT_1 = "stay in the Center"
# 窗口名称
MAIN_TITLE = "Welcome!"
# 当窗口关闭时提示
WIN_CLOSSE = "window Closed"
# 当成功登录时显示
SUCCESS_LOGIN = "Sucessfully Login! "
STAR = "*************************************"
# 当前时间
# CUR_TIME = self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")

HAMLET="""

	HAMLET:
		To be, or not to be
		that is the question
		Whether 'tis nobler in the mind to suffer
		The slings and arrows of outrageous fortune
		Or to take arms against a sea of troubles
		And by opposing end them. 
		To die, to sleep
		No more and by a sleep to say we end
		The heartache, and the thousand natural shocks
		That flesh is heir to. 
		`Tis a consummation
		Devoutly to be wished.

					--- Shakespeare

\n"""
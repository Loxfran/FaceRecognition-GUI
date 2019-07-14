import cv2
import time
import pickle
import numpy as np
import tkinter as tk
from PIL import Image,ImageTk
import face_recognition as fr
from tkinter import messagebox
from options import *
from maintenance import MC


class MainWindow():
	"""创建一个MainWindow类，包含人脸识别整体框架"""
	def __init__(self):
		self.face_xml = FACE_XML  # 读取 用于人脸识别的haar特征参数
		self.top_text = TOPTEXT_1  # 识别窗口顶层显示信息
		self.font = FONT
		self.detect_flag = 0  # 用于判断是否检测完成
		self.frame_number = 0  # 用于计算FPS值 初始值设为0 每两秒计算一次 然后重设为0
		self.top_text_time = 0  # 顶层仅显示一层信息
		self.log_name = LOG_PATH + str(time.strftime("%Y%m%d%H%M%S"))+"_main.log"
		self.game_flag = 0


	def creat_window(self):
		"""
			主界面窗口的创建 ！！可单独设为一个类
		"""
		self.window = tk.Tk()
		self.window.title(MAIN_TITLE)
		# 800x600窗口大小 距离屏幕左边与上面分别为283,70像素值
		self.window.geometry(WINDOW_SIZE)  
		# 在主界面创建一个画布大小为
		self.canvas = tk.Canvas(self.window,bg='Gray',height=400,width=690)  
		self.canvas.pack()

		self.S = tk.Scrollbar(self.canvas,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.S.set)
		self.T = tk.Text(self.canvas,bg='gray75',fg='green', height=25, width=90)
		self.S.pack(side=tk.RIGHT, fill=tk.Y)
		self.T.pack(side=tk.LEFT, fill=tk.BOTH)
		self.S.config(command=self.T.yview)
		self.T.config(yscrollcommand=self.S.set)
		self.quote = HAMLET
		self.T.insert(tk.END, "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END, self.quote)
		self.T.see(tk.END)

		# 获取用户名 登录用
		self.label_1 = tk.Label(self.window,text="用户名：")
		self.label_1.place(x=225, y=350)
		self.usr_name_get = tk.StringVar()  
		self.usr_name_entry = tk.Entry(self.window, textvariable=self.usr_name_get)
		self.usr_name_entry.place(x=275, y=350)
		# 获取用户密码 登录用
		self.label_1 = tk.Label(self.window,text="  密码：")
		self.label_1.place(x=225, y=380)
		self.usr_pwd_get = tk.StringVar()
		self.usr_pwd_entry = tk.Entry(self.window, textvariable=self.usr_pwd_get,show="*")
		self.usr_pwd_entry.place(x=275, y=380)
		# 布置一个登陆按键
		self.window.bind('<Return>', self.sign_in)
		# self.button1 = tk.Button(self.window, text='登录', width=15,
		# 				height=1,command=self.sign_in)

		self.button1 = tk.Button(self.window, text='登录', width=15,
						height=1)
		self.button1.bind('<Button-1>',self.sign_in)
		self.button1.place(relx=0.5,rely=0.75,anchor=tk.CENTER)
		# self.button1.place(x=275, y=400)
		# self.button1.place(x=275,y=450,anchor=tk.W,width=80,height=20)
		# self.button1.pack(side=tk.BOTTOM,pady=30)
		# self.button1.pack(side=tk.BOTTOM,ipadx=5,ipady=50,expand=1)
		# 布置一个注册按键
		self.button2 = tk.Button(self.window, text='注册', width=15,
						height=1,command=self.sign_up)
		self.button2.place(relx=0.5,rely=0.8,anchor=tk.CENTER)
		# self.button2.place(x=275,y=400,anchor=tk.W,width=80,height=20)
		# self.button2.pack(side=tk.BOTTOM,pady=50)
		# self.button2.pack(side=tk.BOTTOM,ipadx=5,ipady=20,expand=1)
		self.button3 = tk.Button(self.window, text='管理', width=15,
						height=1,command=self.manager)
		self.button3.place(relx=0.5,rely=0.85,anchor=tk.CENTER)
		self.window.mainloop() 
		self.store_text()
		################################################################
	def manager(self):
		self.mc = MC(self.window)
		self.mc.creat_window()

	def sign_in(self, event):
		"""用于实现登陆的函数"""
		self.T.insert(tk.END, "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END, "User Sign in.\n")
		self.T.see(tk.END)
		self.T.see(tk.END)
		if not self.check_pwd():
			# 如果用户名与密码不对应，返回False
			return False
		# 密码确认后，创建一个窗口用于人脸识别 登陆用
		self.sign_in_window = tk.Toplevel(self.window)  # 采用Toplevel，因为无法同时建立两个window
		self.sign_in_window.title("Sign In")
		self.sign_in_window.geometry(WINDOW_SIZE)
		# 调用opencv的VideoCapture函数 开启摄像头
		# self.camera = cv2.VideoCapture(0)
		# 用于计算FPS值 初始值为0 两秒清零
		self.start_time = time.time() 
		# 第一次先对frame_number清零 ？
		self.frame_number = 0
		self.last_frame_number = 0  # ？
		self.fps = 1
		#self.window.protocol('WM_DELETE_WINDOW', detector)
		self.label1 = tk.Label(self.sign_in_window)  # initialize image self.label
		self.label1.pack(padx=10, pady=10)
		self.sign_in_window.config(cursor="arrow")
		# 用于判断时登陆界面1还是注册界面0
		self.window_name = 1
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"self.window_name = 1\n")
		self.T.see(tk.END)
		self.detect_flag = 1
		self.i = 0
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"self.detect_flag = 1\n")
		self.T.see(tk.END)
		# 初始检测输出为Unknown
		self.dec_name = UNKNOWN
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"self.dec_name = UNKNOWN\n")
		self.T.see(tk.END)

		# ？
		self.hold_time_start = None
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"self.hold_time_start = None\n")
		self.T.see(tk.END)
		try:
			self.camera = cv2.VideoCapture(0)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"打开摄像头!\n")
			self.T.see(tk.END)
			self.detect_start_time = time.time()
			self.video_loop()
		except:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ERROR0
			print(MESSAGE)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)
		self.store_text()
		# if self.game_flag == 1:
		# 	self.start_game()
		# else:
		# 	tk.messagebox.showerror("Bad Person!")
		return

	def check_pwd(self):
		"""用于检测用户名与密码是否一致"""
		
		# 从窗口获取用户名与密码
		self.usr_name = str(self.usr_name_get.get())
		self.usr_pwd = str(self.usr_pwd_get.get())

		# 尝试打开存放用户密码信息的数据库
		try:
			with open(USERS_INFOR_PATH, "rb") as f:
				# 加载用户密码
				exist_usr_info = pickle.load(f)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"loading files:"+USERS_INFOR_PATH+"\n")
				self.T.see(tk.END)
			# print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:",exist_usr_info)
			# 判断该用户是否存在
			if self.usr_name in exist_usr_info:
				# print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:",self.usr_pwd)
				# 判断密码是否正确
				if self.usr_pwd != exist_usr_info[self.usr_name]:
					MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+exist_usr_info[self.usr_name]
					print(MESSAGE)
					self.T.insert(tk.END,MESSAGE+"\n")
					self.T.see(tk.END)
					tk.messagebox.showerror(ERROR1)
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,ERROR1+"\n")
					self.T.see(tk.END)
					return False
				else:
					MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"User Name:"+self.usr_name
					print(MESSAGE)
					self.T.insert(tk.END,MESSAGE+"\n")
					self.T.see(tk.END)
					MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"User Passward:"+self.usr_pwd
					print(MESSAGE)
					self.T.insert(tk.END,MESSAGE+"\n")
					self.T.see(tk.END)
					return True
			else:
				tk.messagebox.showerror(ERROR2)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,ERROR2+"\n")
				self.T.see(tk.END)
				return False
		# ？此处是不是有BUG 是不是应该加一个生成usrs_info.pkl文件的语句
		# ！不需要
		except:
			tk.messagebox.showerror(ERROR2)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,ERROR2+"\n")
			self.T.see(tk.END)
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ERROR3
			print(MESSAGE)
			self.T.insert(tk.END, MESSAGE+"\n")
			self.T.see(tk.END)
			# self.T.insert(tk.END,ERROR3+"\n")
			self.T.see(tk.END)
			return False
		self.store_text()

	def sign_up(self):
		"""注册新用户"""
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"开始进行注册\n")
		self.T.see(tk.END)
		# 创建新的注册窗口
		self.window_sign_up = tk.Toplevel()
		self.window_sign_up.geometry('350x200+508+150')
		self.window_sign_up.title('Sign Up')

		# 用户名
		self.new_name_get = tk.StringVar()
		self.new_name_get.set('example@python.com')
		tk.Label(self.window_sign_up,text='User name').place(x=10,y=10)
		self.new_name_entry = tk.Entry(self.window_sign_up,textvariable=self.new_name_get)
		self.new_name_entry.place(x=150,y=10)
		# 密码
		self.new_pwd_get = tk.StringVar()
		tk.Label(self.window_sign_up,text='Passward:').place(x=10,y=50)
		self.entry_usr_pwd = tk.Entry(self.window_sign_up,textvariable=self.new_pwd_get,show='*')
		self.entry_usr_pwd.place(x=150,y=50)
		# 密码确认
		self.new_pwd_confirm = tk.StringVar()
		tk.Label(self.window_sign_up,text='comfirm passward:').place(x=10,y=90)
		self.entry_usr_pwd_confirm = tk.Entry(self.window_sign_up,textvariable=self.new_pwd_confirm,show='*')
		self.entry_usr_pwd_confirm.place(x=150,y=90)
		# 确认按键 调用sign_to函数实现人脸信息采集
		self.window_sign_up.bind("<Return>",self.sign_to)
		self.confirm_sign_up_btn = tk.Button(self.window_sign_up,text='Sign up')
		self.confirm_sign_up_btn.bind("<Button-1>",self.sign_to)
		self.confirm_sign_up_btn.place(x=150,y=130)
		self.store_text()

	def sign_to(self,event):
		"""
		注册功能 （判断用户是否已经存在），判断两次密码输入密码是否一致
		将新用户用户名与密码存入数据库

		"""

		# 得到用户名 并进行密码确认功能
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"确认密码\n")
		self.T.see(tk.END)
		self.new_name = str(self.new_name_get.get())
		np = str(self.new_pwd_get.get())  # 
		npf = str(self.new_pwd_confirm.get())
		try:
			with open(USERS_INFOR_PATH, "rb") as f:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"loading files:"+str(USERS_INFOR_PATH)+"\n")
				self.T.see(tk.END)
				# 加载用户信息文件
				exist_usr_info = pickle.load(f)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"completed!\n")
				self.T.see(tk.END)
		except:
			exist_usr_info = {}
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ERROR4
			print(MESSAGE)
			self.T.insert(tk.END, MESSAGE+"\n")
			self.T.see(tk.END)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"No such files:"+USERS_INFOR_PATH+"\n")
			self.T.see(tk.END)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"Creating files"+USERS_INFOR_PATH+"\n")
			self.T.see(tk.END)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"completed!\n")
			self.T.see(tk.END)

		# if self.new_name in exist_usr_info:
		# 	tk.messagebox.showerror('Error','User Already Exist!')
		# 	self.window_sign_up.destroy()
		# 	self.sign_up()
		# 	return

		if np != npf:
			tk.messagebox.showerror(ERROR5)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,ERROR5+"\n")
			self.T.see(tk.END)
			self.window_sign_up.destroy()
			self.sign_up()
			return
		else:
			exist_usr_info[self.new_name] = np
			with open(USERS_INFOR_PATH,'wb') as usr_file:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				pickle.dump(exist_usr_info,usr_file)
				self.T.insert(tk.END,"Information Saved Successfully!\n")
				self.T.see(tk.END)
			# tk.messagebox.showinfo(message='Wlcome you have successfully signed up!')
			self.window_sign_up.destroy()
			# 调用人脸识别窗口
			self.sign_up_face()
		self.store_text()

	def sign_up_face(self):
		"""注册 用于人脸检测窗口的搭建 ！！还能优化 界面还能没一点"""
		self.sign_up_face_window = tk.Toplevel(self.window)
		self.sign_up_face_window.title("Sign Up")
		self.sign_up_face_window.geometry(WINDOW_SIZE)
		# 打开摄像机
		# self.camera = cv2.VideoCapture(0)
		# 初始化参数
		self.start_time = time.time() 
		self.frame_number = 0
		self.last_frame_number = 0
		self.fps = 1
		# ？ 下面需要研究研究 然后修改修改
		###########################################
		self.label0 = tk.Label(self.sign_up_face_window)  # initialize image self.label
		self.label0.pack(padx=10, pady=10)
		#########################################
		self.sign_up_face_window.config(cursor="arrow")
		# self.sign_up_face_window.bind("<Return>",self.get_face)
		self.sign_up_face_button = tk.Button(self.sign_up_face_window, text="Ready!")
		self.sign_up_face_button.bind("<Button-1>",self.get_face)
		self.sign_up_face_button.pack(fill="both", expand=True, padx=10, pady=10)
		# 下面四行可以放在上面吗？或者将上面的取下来
		self.window_name = 0
		self.detect_flag = 0
		self.i = 0
		self.dec_name = UNKNOWN
		self.hold_time_start = None
		# 这么做不怎么报错
		try:
			self.camera = cv2.VideoCapture(0)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"Camera On!\n")
			self.T.see(tk.END)
			self.detect_start_time = time.time()
			self.video_loop()
		except:
			print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:",ERROR0)
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,ERROR0+"\n")
			self.T.see(tk.END)
		self.store_text()
		return

	def get_face(self,event):
		self.detect_flag = 1
		MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+HELLO_FACE
		print(MESSAGE)
		self.T.insert(tk.END,MESSAGE+"\n")
		self.T.see(tk.END)
		self.store_text()

	def store_face_codings(self, unknown_encoding):
		"""存储用户头像信息"""
		try:
			with open(ENCODER_PATH, "rb") as f:
				self.face_data_dic = pickle.load(f)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"Loading Files:"+ENCODER_PATH+"\n")
				self.T.see(tk.END)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"Completed!\n")
				self.T.see(tk.END)
		except:
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"No such files:"+ENCODER_PATH+"\n")
			self.T.see(tk.END)
			self.face_data_dic = {}
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ERROR6
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)
		self.face_data_dic[self.new_name] = unknown_encoding
		with open(ENCODER_PATH, "wb") as f1:
			pickle.dump(self.face_data_dic, f1)
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+SUCCESS_LOGIN+self.new_name
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)
		MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+str(self.face_data_dic.keys())
		print(MESSAGE)
		self.T.insert(tk.END,MESSAGE+"\n")
		self.T.see(tk.END)
		self.store_text()
		return



	def video_loop(self):
		"""实现人脸识别与检测的函数 太长了可简化"""

		# 加载人脸编码数据库文件
		# if not self.face_data_dic:
		if self.i == 0:
			try:
				with open(ENCODER_PATH, "rb") as f:
					self.face_data_dic = pickle.load(f)
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"Loading Files:"+ENCODER_PATH+"\n")
					self.T.see(tk.END)
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"Completed!\n")
					self.T.see(tk.END)

			except:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"No such files:"+ENCODER_PATH+"\n")
				self.T.see(tk.END)
				with open(ENCODER_PATH, "wb") as f:
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"Creating files:"+ENCODER_PATH+"\n")
					self.T.see(tk.END)
					self.face_data_dic = {}
					pickle.dump(self.face_data_dic, f)
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"Completed!\n")
					self.T.see(tk.END)
				MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ERROR7
				print(MESSAGE)
				self.T.insert(tk.END,MESSAGE+"\n")
				self.T.see(tk.END)
			self.i=1
		else:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+ "self.i=" +str(self.i)
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)
			self.i += 1

		# success:是否读取到图像的flag
		# img：返回的单帧图像数据
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"Reading Frame...\n")
		self.T.see(tk.END)
		success, img = self.camera.read()  # 从摄像头读取照片
		if not success:
			MESSAGE="["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+NO_PIC
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)

		if success:
			cv2.waitKey(0)
			# 开始计算帧数
			self.calfps()
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"FPS= "+str(int(self.fps))+" frames per second\n")
			self.T.see(tk.END)
			# 判断摄像头是否启动成功
			if int(self.fps) < 1:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"self.fps = 0\n")
				self.T.see(tk.END)
				self.camera.release()
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.insert(tk.END,"self.camera.release()\n")
				self.T.see(tk.END)
				time.sleep(1)
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"正在重新启动摄像机\n")
				self.T.see(tk.END)
				self.camera=cv2.VideoCapture(0)
				self.fps = 1
				self.detect_start_time = time.time()
				self.start_time = time.time()

			# img = np.minimum(img,150)
			# 对帧进行灰度处理
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			self.mean_light = int(np.mean(gray))
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.insert(tk.END,"Light Level: "+str(self.mean_light)+"\n")
			self.T.see(tk.END)
			if self.mean_light > LIGHT_LEVEL:
				gray = np.minimum(gray,155)
				MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:" + "光线太强！"
				print(MESSAGE)
				self.T.insert(tk.END,MESSAGE+"\n")
				self.T.see(tk.END)
				# gray = gray/2
				self.top_text_time = time.time()
				# self.dec_name = UNKNOWN
				# self.detect_flag = 1
				self.top_text = "What a Sunny Day"

			# 调用opencv函数对图像进行检测
			self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			self.T.see(tk.END)
			self.T.insert(tk.END,"开始进行人像检测。。。\n")
			self.T.see(tk.END)
			faces = self.face_xml.detectMultiScale(gray,1.2,5)  # 参数了解一下？
			###################################################
			# 消灭登录窗口1或者注册窗口
			try:
				if (time.time() - self.detect_start_time) > KEEP_TIME:
					# 判断是哪个
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"关闭检测窗口\n")
					self.T.see(tk.END)
					if self.window_name == 1:
						self.sign_in_window.destroy()
						self.confirmed_face()
					else:
						self.sign_up_face_window.destroy()
						self.confirmed_face()
					self.release()
					return 
			except:pass

			# 当检测到不止一个人脸时，提示 三 秒
			if (time.time() - self.top_text_time) > 3:
				self.top_text = TOPTEXT_1

			if len(faces)>1:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"人像数目大于一\n")
				self.T.see(tk.END)
				self.top_text_time = time.time()
				self.dec_name = UNKNOWN
				self.detect_flag = 1
				self.top_text = "Keep Your Face Only"
			if len(faces)==0:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"没有检测到人像\n")
				self.T.see(tk.END)
				self.detect_flag = 1

			# 提取左上角坐标，与宽，高信息
			for (x, y, w, h) in faces:
				self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
				self.T.see(tk.END)
				self.T.insert(tk.END,"检测到人脸\n")
				self.T.see(tk.END)
				MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"x="+str(x)+" y="+str(y)+" w="+str(w)+" h="+str(h)
				self.T.insert(tk.END,MESSAGE+"\n")
				self.T.see(tk.END)
				print(MESSAGE)
				x_ = x - int(w/4)
				y_ = y - int(h/4)
				w_ = int(1.25*w)
				h_ = int(1.25*h)
				# 当没有检测出来时，进行下一步
				if (self.detect_flag == 1) and ((self.frame_number+1)%SAMPLE == 0):
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"开始进行识别。。。\n")
					self.T.see(tk.END)
					face = img[x_:x_+w_, y_:y_+h_]
					face_locations = fr.face_locations(face)
					if face_locations:
						# print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:","##################################")
						unknown_encoding = fr.face_encodings(face, face_locations)[0]
						self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
						self.T.see(tk.END)
						self.T.insert(tk.END,"开始对人脸进行编码。。。\n")
						self.T.see(tk.END)
						self.i = 1000
						if self.window_name == 1:
							"""登录"""
							MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"This is:"+self.usr_name
							print(MESSAGE)
							self.T.insert(tk.END,MESSAGE+"\n")
							self.T.see(tk.END)
							self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
							self.T.see(tk.END)
							self.results = fr.compare_faces([self.face_data_dic[self.usr_name]], unknown_encoding)
							self.T.insert(tk.END,"对比完成\n")
							self.T.see(tk.END)
							MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+str(self.results)
							print(MESSAGE)
							self.T.insert(tk.END,MESSAGE+"\n")
							self.T.see(tk.END)
							if self.results[0]:
								self.dec_name = self.usr_name
								self.hold_time_start = time.time()
								self.detect_flag = 0
								self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
								self.T.see(tk.END)
								self.T.insert(tk.END,"识别完成，"+self.dec_name+"\n")
								self.T.see(tk.END)
								self.game_flag = 1
							else:
								
								self.dec_name = UNKNOWN
								MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"认证失败！"+self.dec_name
								print(MESSAGE)
								self.T.insert(tk.END,MESSAGE+"\n")
								self.T.see(tk.END)
						else:
							"""注册"""
							if self.i == 1000:
								self.store_face_codings(unknown_encoding)
								self.dec_name = self.new_name
								MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"已将您的身份信息录入："+self.dec_name
								print(MESSAGE)
								self.T.insert(tk.END,MESSAGE+"\n")
								self.T.see(tk.END)
								self.hold_time_start = time.time()
								self.detect_flag = 0
							else:
								pass
				
				l_w = int(w/8)

				cv2.rectangle(img,(x+l_w,y+h),(x+w-l_w,y+h+max(30,int(30*h/200))),WHITE,-1)
				cv2.putText(img, self.dec_name,(x+l_w+min(10,int(2000/w)),y+h+max(25,int(30*h/250))),self.font, max(0.75,w/250),RED,min(3,max(int(w/75),2)),cv2.LINE_AA)

				# 左上					
				cv2.line(img,(x,y),(x+l_w,y),WHITE,2)
				cv2.line(img,(x,y),(x,y+l_w),WHITE,2)
				# 右上
				cv2.line(img,(x+w,y),(x+w-l_w,y),WHITE,2)
				cv2.line(img,(x+w,y),(x+w,y+l_w),WHITE,2)
				# 左下
				cv2.line(img,(x,y+h),(x+l_w,y+h),WHITE,2)
				cv2.line(img,(x,y+h),(x,y+h-l_w),WHITE,2)
				# 右下
				cv2.line(img,(x+w,y+h),(x+w-l_w,y+h),WHITE,2)
				cv2.line(img,(x+w,y+h),(x+w,y+h-l_w),WHITE,2)
				
			cv2.putText(img, self.top_text,(220,50), self.font,0.75,BLUE,2,cv2.LINE_AA)
			cv2.putText(img, "FPS: "+str(int(self.fps)),(10,25), self.font,0.75,WHITE,2,cv2.LINE_AA)
			cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
			current_image = Image.fromarray(cv2image)#将图像转换成Image对象
			imgtk = ImageTk.PhotoImage(image=current_image)
			
			try:
				if self.window_name == 1:
					self.label1.imgtk = imgtk
					self.label1.config(image=imgtk)
				else:
					self.label0.imgtk = imgtk
					self.label0.config(image=imgtk)
				self.window.after(1, self.video_loop)
			except:
				if self.window_name == 1:
					self.sign_in_window.destroy()
					self.release()
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"self.sign_in_window.destroy()\n")
					self.T.see(tk.END)
					
				else:
					self.sign_up_face_window.destroy()
					self.release()
					self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
					self.T.see(tk.END)
					self.T.insert(tk.END,"self.sign_up_face_window.destroy()\n")
					print("self.sign_up_face_window.destroy()")
					self.T.see(tk.END)
				return 
				MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+WIN_CLOSSE
				print(MESSAGE)
				self.T.insert(tk.END,MESSAGE+"\n")
				self.T.see(tk.END)


	def calfps(self):
		"""计算FPS"""
		self.frame_number+=1
		self.time_sec = time.time() - self.start_time
		# print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:",self.time_sec)
		if self.time_sec > FPS_TIME:
			self.fps = (self.frame_number-self.last_frame_number)/self.time_sec
			self.last_frame_number = self.frame_number
			self.start_time = time.time()
			# print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+,"]:",imeSec=",int(self.time_sec),"|FPS=",int(self.fps))
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"FPS="+str(int(self.fps))
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)

		# if self.fps==0:
		# 	self.camera.release()
		# 	time.sleep(2)
		# 	self.camera=cv2.VideoCapture(0)
		return

	def confirmed_face(self):
		MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"+"This is:"+self.dec_name
		print(MESSAGE)
		self.T.insert(tk.END,MESSAGE+"\n")
		self.T.see(tk.END)
		self.store_text()

	def release(self):
		# 当一切都完成后，关闭摄像头并释放所占资源
		self.camera.release()
		cv2.destroyAllWindows()
		self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
		self.T.see(tk.END)
		self.T.insert(tk.END,"关闭摄像头并释放所占资源\n")
		print("关闭摄像头并释放所占资源")
		self.T.see(tk.END)
		self.store_text()
		if self.window_name == 1 and START_GAME_FLAG==1:
			self.start_game()

	def store_text(self):
		try:
			self.text = self.T.get("0.0",tk.END)
			self.log = open(self.log_name, mode='w')
			self.log.write(self.text)
		except:
			print("store_text: End")

	def start_game(self):
		if self.game_flag == 1:
			g=Game()
			g.show_start_screen()
			while g.running:
			    g.new()
			    g.show_go_screen()

			pg.quit()
		else:
			tk.messagebox.showerror("Bad Person!")
		return
import tkinter as tk
import pickle
from options import *


class MC():
	def __init__(self,mw):
		self.usr_info = {}
		self.usr_info_name = []
		self.usr_info_pwd = []
		self.usr_encoder = {}
		self.usr_encoder_name = []
		self.usr_encoder_data = []
		self.mw = mw
		self.log_name = LOG_PATH + str(time.strftime("%Y%m%d%H%M%S"))+"_maintenance.log"

	def creat_window(self):
		self.load_data()
		self.mc_window = tk.Toplevel(self.mw)
		# self.mc_window = tk.Tk()
		self.mc_window.title("Maintenance")
		self.mc_window.geometry('600x400+383+200')
		self.var1 = tk.StringVar()
		self.var2 = tk.StringVar()
		self.var3 = tk.StringVar()
		self.var3.set("Passward:***")
		# self.new_pwd = "Change Passward"

		self.label = tk.Label(self.mc_window,bg='Pink',width=25,height=1, textvariable=self.var1)
		self.label.place(relx=0.75,rely=0.625,anchor=tk.CENTER)
		self.label2 = tk.Label(self.mc_window,bg='LightGreen',width=25,height=1, textvariable=self.var3)
		self.label2.place(relx=0.75,rely=0.7,anchor=tk.CENTER)


		self.button = tk.Button(self.mc_window,text='Deleat Selection',width=15,
					  height=1,command=self.delete_item)
		self.button.place(relx=0.75,rely=0.8,anchor=tk.CENTER)
		self.button2 = tk.Button(self.mc_window,text='Get Passward',width=15,
					  height=1,command=self.get_pwd)
		self.button2.place(relx=0.75,rely=0.9,anchor=tk.CENTER)


		#### listbox的修改
		self.listbox = tk.Listbox(self.mc_window,bg="Plum", width=40,height=21,listvariable=self.var2)
		self.list_items = self.usr_info_name
		for item in self.list_items:
			self.listbox.insert('end',item)
		# self.listbox.pack()
		self.listbox.place(relx=0.02,rely=0.0,anchor=tk.NW)

		self.label3 = tk.Label(self.mc_window,width=8,height=1, text=" NewPWD：")
		self.label3.place(relx=0.525,rely=0.4,anchor=tk.W)
		self.entry = tk.Entry(self.mc_window, show=None)
		self.entry.place(relx=0.75,rely=0.4,anchor=tk.CENTER)
		self.button3 = tk.Button(self.mc_window,text='Change PWD',width=15,
					  height=1,command=self.change_pwd)
		self.button3.place(relx=0.75,rely=0.5,anchor=tk.CENTER)


		self.canvas = tk.Canvas(self.mc_window,bg='Gray',height=150,width=290)  
		self.canvas.place(relx=0.51,rely=0.0,anchor=tk.NW)
		self.S = tk.Scrollbar(self.canvas,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.S.set)
		self.T = tk.Text(self.canvas,bg='gray75',fg='green', height=10, width=38)
		self.S.pack(side=tk.RIGHT, fill=tk.Y)
		self.T.pack(side=tk.LEFT, fill=tk.BOTH)
		self.S.config(command=self.T.yview)
		self.T.config(yscrollcommand=self.S.set)
		self.quote = "Welcome!\n"
		self.T.insert(tk.END, "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:\n")
		self.T.see(tk.END)
		self.T.insert(tk.END, self.quote)
		self.T.see(tk.END)
		self.store_text()


		self.mc_window.mainloop()
	def change_pwd(self):
		try:
			usr_name = self.listbox.get(self.listbox.curselection())
			self.new_pwd = self.entry.get()
			self.usr_info[usr_name] = self.new_pwd
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			print(MESSAGE + self.usr_info[usr_name])
			self.T.insert(tk.END,MESSAGE+usr_name+" has change passward!\n")
			self.T.see(tk.END)
		except:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			print(MESSAGE+"Error:Please Choice a person!")
			self.T.insert(tk.END,MESSAGE+"Error:Please Choice a person!\n")
			self.T.see(tk.END)
		self.dump_data()
		self.store_text()

	
	def get_pwd(self):
		try:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			value = self.usr_info[self.listbox.get(self.listbox.curselection())]
			self.var3.set("Passward:"+value)
			MESSAGE = MESSAGE + "the passward of "+ self.listbox.get(self.listbox.curselection()) + " is: " + value
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)

		except:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			print(MESSAGE+"Error:")
			self.T.insert(tk.END,MESSAGE+"Error:\n")
			self.T.see(tk.END)
		self.store_text()


	def delete_item(self):
		try:
			self.print_selection()
			print(self.usr_info)
			print(self.usr_encoder_name)
			value = self.listbox.get(self.listbox.curselection())
			value_index = self.list_items.index(value)
			print(value_index)
			self.listbox.delete(value_index)
			self.usr_info.pop(value)
			self.usr_encoder.pop(value)
			self.usr_info_name.pop(self.usr_info_name.index(value))
			for key in list(self.usr_encoder.keys()):
				if key not in self.usr_info_name:
					del self.usr_encoder[key]
					self.usr_encoder_name.pop(self.usr_encoder_name.index(key))
			print(self.usr_encoder_name)
			print(self.usr_info)
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			MESSAGE = MESSAGE + value + "`s information has been deleated!"
			print(MESSAGE)
			self.T.insert(tk.END,MESSAGE+"\n")
			self.T.see(tk.END)
		except:
			MESSAGE = "["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:"
			print(MESSAGE+"Error:")
			self.T.insert(tk.END,MESSAGE+"Error:\n")
			self.T.see(tk.END)
		self.dump_data()
		self.store_text()

	def print_selection(self):
		try:
			value = self.listbox.get(self.listbox.curselection())
			self.var1.set(value+" Deleted")
		except:
			pass
		self.store_text()

	def load_data(self):
		with open(USERS_INFOR_PATH, "rb") as f:
			# 加载用户密码
			self.usr_info = pickle.load(f)
			for item in self.usr_info.keys():
				self.usr_info_name.append(item)
			print(self.usr_info_name)
			for item in self.usr_info.values():
				self.usr_info_pwd.append(item)
			print(self.usr_info_pwd)
			# self.T.insert(tk.END,"["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:")
			# self.T.see(tk.END)
			# self.T.insert(tk.END,"loading files:"+USERS_INFOR_PATH+"\n")
			# self.T.see(tk.END)

		with open(ENCODER_PATH, "rb") as f:
			self.usr_encoder = pickle.load(f)
			for item in self.usr_encoder.keys():
				self.usr_encoder_name.append(item)
			print(self.usr_encoder_name)
			for item in self.usr_encoder.values():
				self.usr_encoder_data.append(item)
			print(self.usr_encoder_data)
		self.store_text()

	def dump_data(self):
		with open(USERS_INFOR_PATH, "wb") as f:
			pickle.dump(self.usr_info,f)

		with open(ENCODER_PATH, "wb") as f:
			pickle.dump(self.usr_encoder,f)
		self.store_text()

	def store_text(self):
		try:
			self.text = self.T.get("0.0",tk.END)
			self.log = open(self.log_name, mode='w')
			self.log.write(self.text)
		except:
			print("store_text: End")

# if __name__ == "__main__":
# 	mc = MC()
# 	mc.creat_window()
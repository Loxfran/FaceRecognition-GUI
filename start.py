from main import *

print("["+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"]:##############bSTART##############")
C = MainWindow()
try:
	C.creat_window()

except:
	C.release()
	print(ERROR8)



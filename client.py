# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200714.1200

# 用法

'''
连接到 IP 地址为 192.168.1.106 的主机
python client.py -s 192.168.1.106
'''

# 导入必要的包
from imutils.video import VideoStream		  # 摄像头作为输入源
from imagezmq import imagezmq				  # 网络视频流设置
import argparse								  # 命令行参数
import socket								  # 网络操作
import time									  # 时间操作
import sys									  # 系统操作
import cv2									  # OpenCV
import os									  # 文件和文件夹操作

# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

# 显示欢迎信息
print("""

**********************************************************************************
 _   _  _      _                _____                _                            
| | | |(_)    | |              /  __ \              | |                           
| | | | _   __| |  ___   ___   | /  \/  __ _  _ __  | |_  _   _  _ __   ___  _ __ 
| | | || | / _` | / _ \ / _ \  | |     / _` || '_ \ | __|| | | || '__| / _ \| '__|
\ \_/ /| || (_| ||  __/| (_) | | \__/\| (_| || |_) || |_ | |_| || |   |  __/| |   
 \___/ |_| \__,_| \___| \___/   \____/ \__,_|| .__/  \__| \__,_||_|    \___||_|   
                                             | |                                  
*******************************************  |_|  ********************************
（客户端）


[i] 本程序将当前设备的视频串流到指定 IP 地址的服务器上。

    您需要：
     1. 在服务器上运行 video-capturer 主程序 / 服务器端：vccmd.py 或 vcgui.py
     2. 按 y 运行本程序
""")

# 设置循环
i = 0

while i == 0:
	# 询问用户是否开始采集
	answer = input("    现在开始串流本设备的视频到服务器？[y/n]").lower()	

	if answer == "y":
		i = 1

		# 使用服务器的套接字地址初始化 ImageSender 对象
		sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
			args["server_ip"]))

		# 获取主机名，初始化网络视频流，并允许摄像机传感器预热
		rpiName = socket.gethostname()
		# vs = VideoStream(usePiCamera=True).start()
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
		print("    正在串流...")
		print("    按 Ctrl + C 停止。")
		
		while True:
			# 从摄像机读取帧并将其发送到 Video Capturer
			frame = vs.read()
			sender.send_image(rpiName, frame)

			# 如果用户按下 Q 键，则中断进程
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				print("\n\n[x] 您已中止串流。")
				print("\a")
				i = 1
				sys.exit(0)

	elif answer == "n":
		print("\n\n[x] 您已取消串流。")
		print("\a")
		i = 1

	else:
		print("    请输入 y 开始串流，或输入 n 取消串流。")
		print("\a")
		i = 0
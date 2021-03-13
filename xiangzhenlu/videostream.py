# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 210313.2317

# 导入必要的包
from imutils.video import VideoStream		  # 摄像头作为输入源
from imagezmq import imagezmq				  # 网络视频流设置
import argparse								  # 命令行参数
import socket								  # 网络操作
import time									  # 时间操作
import sys									  # 系统操作
import cv2									  # OpenCV
import os									  # 文件和文件夹操作

def startStream():

	# 使用服务器的套接字地址初始化 ImageSender 对象
	sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

	# 指定网络视频流地址和名称
	paths = []
	
	# 读取全部内容，并以列表方式返回
	t = open("streams.txt","r")
	lines = t.readlines()
	for line in lines:
		line = line.strip()
		paths.append(line)

	for path in paths:
		if path == "" or "://" not in path:
			paths.remove(path)

	rpiNames = ["Stream 1", "Stream 2", "Stream 3", "Stream 4", "Stream 5", "Stream 6", "Stream 7", "Stream 8", "Stream 9"]

	while True:
		# 从网络视频流读取帧并将其发送到 Video Capturer
		for (path, rpiName) in zip(paths, rpiNames):
			vs = VideoStream(path).start()
			frame = vs.read()
			try:
				sender.send_image(rpiName, frame)
			except AttributeError:
				pass

			continue

def stopStream():
	i = 1
	sys.exit(0)
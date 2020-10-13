# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 201013.2100

# 导入必要的包
import sys									  # 将终端输出保存到日志
import datetime								  # 时间戳
import imutils								  # 图像操作简便函数集
import time									  # 时间操作
import cv2									  # OpenCV
import os									  # 文件和文件夹操作
import fnmatch								  # 计算文件个数
import csv									  # 读取和保存 CSV 文件
import numpy as np							  # 计算轮廓坐标
import matplotlib.pyplot as plt				  # 绘图并保存
import xml.etree.ElementTree as ET			  # 保存 XML 文件
import tkinter as tk                          # 用户界面
import tkinter.ttk as ttk                     # 高级用户界面
from tkinter import *                         # 滚动条
from tkinter import messagebox                # 对话框
from tkinter.ttk import *                     # 进度条
from pyimagesearch.tempimage import TempImage # 保存临时文件
from pyimagesearch.basicmotiondetector import BasicMotionDetector
											  # 多帧加权平均法侦测器
from xiangzhenlu.biframemotiondetector import BiFrameMotionDetector
											  # 二帧差分法侦测器
from xiangzhenlu.triframemotiondetector import TriFrameMotionDetector
											  # 三帧差分法侦测器
from xiangzhenlu.videostream import *		  # 串流网络视频流
from imagezmq import imagezmq				  # 网络视频流设置
from imutils import build_montages			  # 网络视频流分屏显示
from imutils.video import VideoStream		  # 摄像头作为输入源
from imutils.video import count_frames	      # 计算帧数
from imutils.video import FPS				  # 计算采集时的平均帧率
from colorama import init, Fore, Back, Style  # 在终端输出彩色文字

def startCapture(fileList, jsonPath, showVideo, saveLog, inputType, inputFiles, inputFolder, savePath, annotationType, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i):
	# 进程开始
	startTime = datetime.datetime.now()

	# 如果为 Windows 操作系统，则导入 keyboard 包
	if os.name == 'nt':
		import keyboard
	else:
		class keyboard:
			def is_pressed(self, *args):
				return False

	# 同时在终端显示结果，并保存到日志文件
	class __redirection__:
		
		def __init__(self):
			self.__console__=sys.stdout
			
		def write(self, output_stream):
			pass
			
		def to_console(self):
			sys.stdout=self.__console__
		
		def flush(self):
			pass
			
		def reset(self):
			sys.stdout=self.__console__
			
	if __name__=="__main__":
		# 重定向
		r_obj=__redirection__()
		sys.stdout=r_obj
		
		# 重定向到控制台
		r_obj.to_console()
		
		# 刷新缓冲区
		r_obj.flush()
		
		# 重置
		r_obj.reset()

	class Logger(object):
		def __init__(self, logFile ="Default.log"):
			self.terminal = sys.stdout
			self.log = open(logFile,'a')
	
		def write(self,message):
			self.terminal.write(message)
			self.log.write(message)
	
		def flush(self):
			pass

	class StdoutRedirector(object):
		def __init__(self,text_widget):
			self.text_space = text_widget

		def write(self,string):
			self.text_space.insert('end', string)
			self.text_space.see('end')

	# 停止采集函数
	def stopCapture():
		finishTime1 = datetime.datetime.now()

		if inputType == "network":
			print(Fore.RED + "\n    用户于 {} 选择中断本次采集。".format(finishTime1))
			print("\a")
			stopStream()
			window.destroy()
			cv2.destroyAllWindows()
			window.after(100, stopCapture)
			raise Exception
			sys.exit(0)

		try:
			fpsTimer.stop()
			print(Fore.RED + "\n    用户于 {} 选择中断本次采集。".format(finishTime1))

			if inputType == "folder" or inputType == "files":
				print(Style.RESET_ALL + "    {} 的采集提前结束。".format(f))
				print("\a")
				fvs.release()
			elif inputType == "webcam":
				print("\a")
				cv2.destroyAllWindows()
				raise Exception

			window.destroy()
			cv2.destroyAllWindows()
			window.after(100, stopCapture)

		except:
			sys.exit(0)

	# 如果使用图形界面，则加载它
	if gui:
		# 跳过采集函数
		def skipCapture(event):
			try:
				fpsTimer.stop()
				finishTime2 = datetime.datetime.now()

				print(Fore.RED + "\n    用户于 {} 选择跳过当前视频。".format(finishTime2))

				if inputType == "folder" or inputType == "files":
					print(Style.RESET_ALL + "    {} 的采集提前结束。".format(f))
					fvs.release()

				elif inputType == "webcam":
					fvs.stop()

				cv2.destroyAllWindows()
				return

			except _tkinter.TclError:
				pass

		# 各类提示函数
		def successInfo():
			messagebox.showinfo(title='已完成采集', message='图像采集已全部完成。')

		def webcamError():
			messagebox.showerror(title='摄像头错误', message='无法从摄像头获取视频。\n请检查摄像头设置是否正确。\n\n图像采集已中止。')

		def networkError():
			messagebox.showerror(title='网络视频流错误', message='无法获取网络视频流。\n请检查网络连接是否正常。\n\n图像采集已中止。')

		# 用户界面
		window = tk.Tk()
		window.title("正在采集图像...")
		window.configure(background="#ffffff")
		window.rowconfigure(0, minsize=600, weight=1)
		window.columnconfigure(1, minsize=800, weight=1)
		window.geometry('800x250+320+610')
		window.resizable(0, 0)

		# 设置主题样式
		currentHour = datetime.datetime.now().hour

		if currentHour >= 19 or currentHour <= 7:
			window.configure(background="#383838")

		else:
			window.configure(background="#ffffff")

		# 写入日志的隐藏文本域
		hiddenTxt = tk.Text(window)

		# 状态标签
		statusLbl = tk.Label(window)
		statusLbl.place(relx=0.025, rely=0.056, height=21, width=757)
		statusLbl.configure(text='''准备就绪''')

		# 跳过当前视频链接
		skipLnk = tk.Label(window)
		skipLnk.configure(text='''跳过''')
		skipLnk.configure(cursor="hand2")
		skipLnk.bind('<Button-1>', skipCapture)

		# 进度条
		progressBar = ttk.Progressbar(window)
		progressBar.configure(length="760")

		# 进度标签
		progressLbl = tk.Label(progressBar)
		progressLbl.pack()
		progressLbl.configure(text='''0.0%''')

		if inputType == "folder" or inputType == "files":
			skipLnk.place(relx=0.025, rely=0.16, height=21, width=300)
			progressBar.place(relx=0.025, rely=0.32, relwidth=0.95, relheight=0.0
					, height=22)

		# 其他实时数据标签
		timeElapsedLbl = tk.Label(window)
		timeElapsedLbl.place(relx=0.025, rely=0.48, height=21, width=136)
		timeElapsedLbl.configure(text='''已用时间：''')

		timeElapsedCountLbl = tk.Label(window)
		timeElapsedCountLbl.place(relx=0.2, rely=0.48, height=21
				, width=228)

		timeEstLbl = tk.Label(window)
		timeEstLbl.configure(text='''估计剩余时间：''')

		timeEstCountLbl = tk.Label(window)

		fpsLbl = tk.Label(window)

		fpsCountLbl = tk.Label(window)

		if inputType == "folder" or inputType == "files": 
			fpsLbl.place(relx=0.513, rely=0.48, height=21, width=136)
			fpsLbl.configure(text='''实时采集帧率：''')
			fpsCountLbl.place(relx=0.688, rely=0.48, height=21, width=228)
			timeEstLbl.place(relx=0.025, rely=0.58, height=21, width=136)
			timeEstCountLbl.place(relx=0.2, rely=0.58, height=21, width=228)
		elif inputType == "webcam":
			fpsLbl.place(relx=0.513, rely=0.48, height=21, width=136)
			fpsLbl.configure(text='''已采集图片：''')
			fpsCountLbl.place(relx=0.688, rely=0.48, height=21, width=228)
		elif inputType == "network":
			fpsLbl.place(relx=0.513, rely=0.48, height=21, width=136)
			fpsLbl.configure(text='''已连接的流：''')
			fpsCountLbl.place(relx=0.688, rely=0.48, height=21, width=228)

		imgLbl = tk.Label(window)
		imgLbl.configure(text='''已采集图片：''')

		imgCountLbl = tk.Label(window)

		# 停止采集按钮
		stopBtn = tk.Button(window)
		stopBtn.place(relx=0.413, rely=0.760, height=38, width=139)
		stopBtn.configure(relief="flat")
		stopBtn.configure(text='''█  停止采集''')
		stopBtn.configure(command=stopCapture)

		if currentHour >= 19 or currentHour <= 7:
			statusLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
			skipLnk.configure(font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0", foreground="#63ACE5", background="#383838", anchor="w")
			statusLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeElapsedLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeElapsedCountLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeEstLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeEstCountLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			fpsLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			fpsCountLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			imgLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			imgCountLbl.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			stopBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
		else:
			statusLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
			skipLnk.configure(font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0", foreground="#1497EE", background="#ffffff", anchor="w")
			statusLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeElapsedLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeElapsedCountLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeEstLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			timeEstCountLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			fpsLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			fpsCountLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			imgLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			imgCountLbl.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0", anchor="w")
			stopBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")

	# 为网络视频流初始化 ImageHub 对象
	imageHub = imagezmq.ImageHub()

	# 初始化 JSON 设置项
	if showVideo:
		showVideo1 = "是"
	else:
		showVideo1 = "否"

	if saveLog:
		saveLog1 = "是"
	else:
		saveLog1 = "否"

	if annotationType == "pascalvoc":
		annotationType1 = "PascalVOC"
	elif annotationType == "yolo":
		annotationType1 = "YOLO"

	if captureType == "avg":
		captureType1 = "多帧加权平均法"
	elif captureType == "two":
		captureType1 = "二帧差分法"
	elif captureType == "three":
		captureType1 = "三帧差分法"

	if captureImages[0] == "all":
		captureImagesPara1 = "应采尽采"
		captureImagesPara2 = "，每 {} 帧取一帧保存".format(captureImages[1])
		captureImagesPara3 = ""
	elif captureImages[0] == "frame":
		captureImagesPara1 = "按帧采集"
		captureImagesPara2 = "，采集 {} 帧".format(captureImages[1])
		captureImagesPara3 = ""
	elif captureImages[0] == "second":
		captureImagesPara1 = "按秒采集"
		captureImagesPara2 = "，采集 {} 秒".format(captureImages[1])
		captureImagesPara3 = "，每 {} 帧取一帧保存".format(captureImages[2])

	captureImages1 = "{}{}{}".format(captureImagesPara1, captureImagesPara2, captureImagesPara3)

	# 如果用户指定了保存日志文件，则在 log/ 目录下保存
	if saveLog:
		try:
			os.mkdir("log/")
		except FileExistsError:
			pass

		logFileName = time.strftime("%Y %m %d %H:%M:%S").replace(':', '_').replace(' ', '_')

		if gui:
			sys.stdout = StdoutRedirector(hiddenTxt)
		else:
			sys.stdout = Logger("log/{}.log".format(logFileName))

	# 根据用户指定的采集来源进行图像采集
	if inputType == "folder" or inputType == "files":
		print("\n\n[i] 将从 {} 个视频中采集图像。".format(len(fileList)))

	elif inputType == "webcam":
		print("\n\n[i] 将从摄像头中采集图像。")

	elif inputType == "network":
		print("\n\n[i] 将从网络视频流中采集图像。")

	else:
		print(Fore.RED + "\n\n[x] 图像采集已中止，因为 input_type 参数无效。")
		print(Fore.RED + "    采集来源：folder（文件夹），files（视频文件列表），webcam（摄像头），network（网络视频流）。")
		print(Style.RESET_ALL + "\a") 
		sys.exit(0)

	print("    使用 {} 中的设置采集：".format(jsonPath))
	print('''     - 显示采集窗口：　　{}
     - 保存采集日志：　　{}
     - 输出目录：　　　　{}
     - 标注格式：　　　　{}
     - 视频读法：　　　　每 {} 帧取一帧读
     - 采集算法：　　　　{}
     - 采集方式：　　　　{}
     - 运动帧最小值：　　{}
     - 阈值增量最小值：　{}
     - 轮廓区域最小值：　{}
     - 设置文件创建时间：{}
     - 设置文件备注：　　{}\n'''.format(showVideo1, saveLog1, savePath, annotationType1, readFrames, captureType1, captureImages1, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes))

	if inputType == "network":
		print("\n[i] 本次采集开始于 {}。".format(startTime))
		print("    正在连接网络视频流...\n")
		
		if gui: 
			statusLbl.configure(text="正在连接网络视频流...")
			statusLbl.update()
			stopBtn.configure(state="disabled")

	else:
		print("\n[i] 本次采集开始于 {}。\n".format(startTime))

	# 遍历所有视频文件
	for n in range(len(fileList)):
		f = fileList[n]

		if inputType == "folder" or inputType == "files":
			print("\n[i] 正在读取文件...")
			if gui: 
				statusLbl.configure(text="正在读取文件...")
				statusLbl.update()
				skipLnk.configure(state="disabled")
				skipLnk.update()
		elif inputType == "webcam":
			print("\n[i] 正在读取摄像头...")
			if gui: 
				statusLbl.configure(text="正在读取摄像头...")

		if inputType == "folder":
			file = inputFolder + f
		elif inputType == "files":
			file = f

		# 创建采集图片保存目录
		if inputType == "folder" or inputType == "files":
			autoPath = f.split("/")[-1].replace(":", "_").replace(" ", "_") + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"
		elif inputType == "webcam":
			autoPath = "webcam" + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"
		elif inputType == "network":
			autoPath = "network" + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"

		# 创建图片标注保存目录
		annotationPath = "annotations/"

		# 如果用户未指定保存目录，将图像直接保存在当前目录下、以视频 + 设置名称命名的子文件夹中
		if savePath == "":
			try:
				os.mkdir(autoPath + annotationPath)
			except FileExistsError:
				pass

		# 否则，将图像保存在用户指定目录下的、以视频 + 设置名称命名的子文件夹中
		else:
			if inputType == "folder" or inputType == "files" or inputType == "webcam":
				try:
					os.makedirs(savePath + autoPath + annotationPath)
				except FileExistsError:
					pass
			elif inputType == "network":
				try:
					os.makedirs(savePath + autoPath)
				except FileExistsError:
					pass				

		# 计算所有待采集视频的帧数之和
		if inputType == "folder" or inputType == "files":
			totalFrameCount = 0

			for m in fileList:
				if inputType == "folder":
					mFile = inputFolder + m
				elif inputType == "files":
					mFile = m

				mVideo = cv2.VideoCapture(mFile)
				frameCount = int(mVideo.get(cv2.CAP_PROP_FRAME_COUNT))
				mVideo.release()

				if frameCount == 0:
					frameCount = int(count_frames(mFile, override=False))

				totalFrameCount += frameCount

		# 计算累计采集帧数和累计保存文件数
		if n > 0:
			if inputType == "folder" or inputType == "files":
				if inputType == "folder":
					lastFile = inputFolder + fileList[n-1]
				elif inputType == "files":
					lastFile = fileList[n-1]
				
				lVideo = cv2.VideoCapture(lastFile)
				lastFileFrameCount = int(lVideo.get(cv2.CAP_PROP_FRAME_COUNT))
				lVideo.release()

				if lastFileFrameCount == 0:
					lastFileFrameCount = int(count_frames(lastFile, override=False))

				cumulatedFrameCount += lastFileFrameCount

				lastFileAutoPath = lastFile.split("/")[-1].replace(":", "_").replace(" ", "_") + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"
				lastFileSaveCount = len(fnmatch.filter(os.listdir(savePath + lastFileAutoPath), '*.jpg'))
				cumulatedSaveCount += lastFileSaveCount
			
			else:
				lastFileAutoPath = autoPath
				lastFileSaveCount = len(fnmatch.filter(os.listdir(savePath + autoPath), '*.jpg'))
				cumulatedSaveCount += lastFileSaveCount

		else:
			cumulatedFrameCount = 0
			cumulatedSaveCount = 0

		# 开始将当前视频信息写入 CSV 文件
		with open(savePath + autoPath + 'vinfo.csv', 'w', newline='', encoding='utf-8') as fOutput:
			try:
				csvOutput = csv.writer(
					fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csvOutput.writerow(["帧", "时间码", "按设定标准采集的运动"])
			except ValueError:
				pass

			if inputType == "network":
				fOutput.close()
				os.remove(savePath + autoPath + 'vinfo.csv')

			if gui:
				if inputType == "folder" or inputType == "files":
					statusLbl.configure(text="正在采集 ({}/{})：{}...".format(n + 1, len(fileList), f.split("/")[-1]))
					statusLbl.update()
					skipLnk.configure(state="normal")

			if inputType == "folder" or inputType == "files":
				# 从视频文件中读取
				print("    正在采集 ({}/{})：{}...".format(n + 1, len(fileList), f))
				fvs = cv2.VideoCapture(file)
				time.sleep(1.0)
			elif inputType == "webcam":
				fvs = VideoStream(src=0).start()
				time.sleep(2.0)

			# 初始化平均帧、当前帧的前两帧、最后保存的时间戳、读帧计数器、帧运动计数器、保存文件计数器和读帧计时器
			avg = None
			lastFrame1 = None
			lastFrame2 = None
			readFrameCounter = 0
			motionCounter = 0
			fpsTimer = FPS().start()
			saveCounter = 0
			allSaveCounter = 0

			# 为网络视频流初始化帧记录
			frameDict = {}

			# 初始化包含网络视频流上次处于活动状态的时间信息的记录，并存储上次进行检查的时间
			lastActive = {}
			lastActiveCheck = datetime.datetime.now()
			lastActiveStreams = {}
			lastActiveMotion = {}

			# 存储估计网络视频流的数量、活动检查周期，并计算在检查视频流是否处于活动状态之前等待的持续时间秒数
			ESTIMATED_NUM_PIS = 4
			ACTIVE_CHECK_PERIOD = 5
			ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

			# 分配每个网络视频流分屏的宽度和高度，以便我们可以在单个“仪表板”中查看所有传入帧
			mW = 3
			mH = 2

			if captureType == "avg":
				motions = BasicMotionDetector(deltaThresh=minDeltaThresh, minArea=minArea)
			elif captureType == "two":
				motions = BiFrameMotionDetector(deltaThresh=minDeltaThresh, minArea=minArea)
			elif captureType == "three":
				motions = TriFrameMotionDetector(deltaThresh=minDeltaThresh, minArea=minArea)

			# 遍历视频帧
			while True:
				if gui:
					window.update()

				currentTime = datetime.datetime.now()

				if inputType == "folder" or inputType == "files":
					readFrameCounter += readFrames
					fvs.set(1, readFrameCounter)
					fps = fvs.get(cv2.CAP_PROP_FPS)
					frame = fvs.read()
					frame = frame[1]

					currentFrameInFile = int(fvs.get(cv2.CAP_PROP_POS_FRAMES))
					fileFrameCount = int(fvs.get(cv2.CAP_PROP_FRAME_COUNT))

				elif inputType == "webcam":
					readFrameCounter += 1
					frame = fvs.read()
					frame = frame

				elif inputType == "network":
					# 从网络视频流接收帧，并确认已接收
					readFrameCounter += 1
					fvs = imageHub.recv_image()
					rpiName = fvs[0]
					streams = fvs[1]
					frame = streams
					imageHub.send_reply(b'OK')
					try:
						os.makedirs(savePath + autoPath + rpiName + "/" + annotationPath)
					except FileExistsError:
						pass

					# 如果视频流不在上一个活动记录中，则意味着它是新连接的视频流
					if rpiName not in lastActive.keys():
						print(Fore.GREEN + "\n[v] 已连接到 {}。".format(rpiName))
						print(Style.RESET_ALL + "    正在读取网络视频流...\n")

						if gui:
							statusLbl.configure(text="正在读取网络视频流...")
							statusLbl.update()
							stopBtn.configure(state="normal")
							
					# 记录活动视频流的最近活跃时间
					lastActive[rpiName] = datetime.datetime.now()
					lastActiveStreams[rpiName] = streams
					lastActiveMotion[rpiName] = motions

					if gui:
						fpsCountLbl.configure(text="{} 个".format(len(lastActive.keys())))

					if len(lastActive.keys()) == 0:
						fpsTimer.stop()

						if gui:
							stopBtn.configure(state="disabled")
							networkError()

						print(Fore.RED + "\n[x] 无法从摄像头获取视频。请检查摄像头设置是否正确。")
						print("    图像采集已中止。")
						print(Style.RESET_ALL + "\a")

						stopCapture()

				timestamp = datetime.datetime.now()
				text = ""

				# 如果用户指定了无效的采集算法，则中止图像采集
				if (captureType == "avg") or (captureType == "two") or (captureType == "three"):
					pass
				else:
					if inputType == "folder" or inputType == "files":
						fvs.release()
					elif inputType == "webcam":
						fvs.stop()

					print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_type 参数无效。")
					print(Fore.RED + "    采集算法：avg（多帧加权平均法），two（二帧差分法），three（三帧差分法）。")
					print(Style.RESET_ALL + "\a") 
					break

				# 如果用户指定了无效的采集方式，则中止图像采集
				if (captureImages[0] == "all") or (captureImages[0] == "frame") or (captureImages[0] == "second"):
					pass
				else:
					if inputType == "folder" or inputType == "files":
						fvs.release()
					elif inputType == "webcam":
						fvs.stop()

					print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_images 参数无效。")
					print(Fore.RED + "    参数格式：['采集方式', 采集数值 1, 采集数值 2]。")
					print(Fore.RED + "    采集方式：all（应采尽采），frame（按帧采集），second（按秒采集）。")
					print(Style.RESET_ALL + "\a") 
					i = 5
					break

				# 计算当前视频的采集进度和估计剩余时间
				for a in range(1):
					elapsedTime = currentTime - startTime
					elapsedTime = elapsedTime.total_seconds()

				if inputType == "folder" or inputType == "files":
					try:
						percent = (currentFrameInFile + cumulatedFrameCount) / totalFrameCount * 100.0
						currentFps = (currentFrameInFile + cumulatedFrameCount) / elapsedTime
						remainingTime = (totalFrameCount - cumulatedFrameCount - currentFrameInFile) / currentFps

					except ZeroDivisionError:
						pass

					except:
						print(Fore.RED + "\n\n[x] 图像采集已中止，因为指定的目录或文件无法读取。")
						print(Fore.RED + "    请确保指定的目录或文件可用，并提供正确的路径。")
						print(Style.RESET_ALL + "\a") 
						sys.exit(0)

					if gui:
						progressBar.configure(value=percent)
						progressLbl.configure(text="{}%".format(str('%.1f'%percent)))
						timeEstCountLbl.configure(text="{}".format(datetime.timedelta(seconds = remainingTime)))
						fpsCountLbl.configure(text="{:.2f} fps".format(currentFps))

					print("\r    总进度 {}%    估计剩余时间 {}".format(str('%.1f'%percent), datetime.timedelta(seconds = remainingTime)), end="")

				if gui:
					timeElapsedCountLbl.configure(text="{}".format(datetime.timedelta(seconds = elapsedTime)))

					if inputType == "folder" or inputType == "files":
						imgLbl.place(relx=0.513, rely=0.58, height=21, width=136)
						imgCountLbl.place(relx=0.688, rely=0.58, height=21, width=228)
						imgCountLbl.configure(text="{} 张".format(cumulatedSaveCount + saveCounter))
					
					elif inputType == "webcam":
						fpsCountLbl.configure(text="{} 张".format(saveCounter))

				# 如果无法抓取帧，则视频已播完
				if frame is None:
					if inputType == "folder" or inputType == "files":
						n += 1
						fpsTimer.stop()
						print("\n    采集完毕。")

						if saveCounter != 0:
							print("     - 总共采集：{} 张图像".format(saveCounter))
							print("     - 保存位置：{}{}".format(savePath, autoPath))
							print("     - 采集用时：{}".format(datetime.timedelta(seconds = fpsTimer.elapsed())))
							print("     - 平均帧率：{:.2f} fps\n".format(fpsTimer.fps()))
						else:
							print(Style.RESET_ALL + "    本次没有采集到图像。")

						if n == len(fileList):
							if gui:
								skipLnk.configure(state="disabled")
								stopBtn.configure(state="disabled")
								successInfo()

							print(Fore.GREEN + "\n[v] 图像采集已全部完成。")
							
							# 进程结束时间
							finishTime = datetime.datetime.now()
							timePassed = finishTime - startTime
							print(Fore.GREEN + "    本次采集完成于 {}，共耗时 {}。".format(finishTime, timePassed))
							print(Style.RESET_ALL + "\a") 

						break

					elif inputType == "webcam":
						fpsTimer.stop()

						if gui:
							stopBtn.configure(state="disabled")
							webcamError()

						print(Fore.RED + "\n[x] 无法从摄像头获取视频。请检查摄像头设置是否正确。")
						print("    图像采集已中止。")
						print(Style.RESET_ALL + "\a")

						break

				# 存储原始宽度、高度、深度，以及采集过程中的帧宽度、高度和转换比率
				ow = frame.shape[1]
				oh = frame.shape[0]
				od = frame.shape[2]
				fw = 500
				ratio = fw / ow
				fh = oh * ratio
				xratio = 1 / fw
				yratio = 1 / fh

				# 复制当前帧（为了保存无标注的图片）、并使用选定的侦测器对帧进行处理和识别
				if inputType == "network":
					for rpiName in lastActive.keys():
						# 从视频流中读取下一帧
						try:
							frame = lastActiveStreams[rpiName]
							motion = lastActiveMotion[rpiName]
							frameOriginal = frame.copy()
							frame = imutils.resize(frame, width=fw)
							(h1, w1) = frame.shape[:2]
							gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
							gray = cv2.GaussianBlur(gray, (21, 21), 0)

							if captureType == "avg":
								locs = motion.update(gray)
							else:
								locs = motion.update(frame)

						except:
							pass

						if len(locs) > 0:
							# 分别初始化最小和最大 (x, y) 坐标
							(minX, minY) = (np.inf, np.inf)
							(maxX, maxY) = (-np.inf, -np.inf)

							# 遍历运动的位置，并累积边界框的最小和最大位置
							for l in locs:
								(x, y, w, h) = cv2.boundingRect(l)
								(minX, maxX) = (min(minX, x), max(maxX, x + w))
								(minY, maxY) = (min(minY, y), max(maxY, y + h))

							# 绘制边界框
							cv2.rectangle(frame, (minX, minY), (maxX, maxY),
								(0, 255, 0), 2)
							text = "Motion"

							# 准备图像标注信息
							xmin = minX / ratio
							xmax = maxX / ratio
							ymin = minY / ratio
							ymax = maxY / ratio

							n1 = (minX * xratio) + ((maxX - minX) * xratio / 2)
							n2 = (minY * yratio) + ((maxY - minY) * yratio / 2)
							n3 = (maxX - minX) * xratio
							n4 = (maxY - minY) * yratio

				else:
					frameOriginal = frame.copy()
					frame = imutils.resize(frame, width=fw)
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					gray = cv2.GaussianBlur(gray, (21, 21), 0)

					if captureType == "avg":
						locs = motions.update(gray)
					else:
						locs = motions.update(frame)

					if len(locs) > 0:
						# 分别初始化最小和最大 (x, y) 坐标
						(minX, minY) = (np.inf, np.inf)
						(maxX, maxY) = (-np.inf, -np.inf)

						# 遍历运动的位置，并累积边界框的最小和最大位置
						for l in locs:
							(x, y, w, h) = cv2.boundingRect(l)
							(minX, maxX) = (min(minX, x), max(maxX, x + w))
							(minY, maxY) = (min(minY, y), max(maxY, y + h))

						# 绘制边界框
						cv2.rectangle(frame, (minX, minY), (maxX, maxY),
							(0, 255, 0), 2)
						text = "Motion"

						# 准备图像标注信息
						xmin = minX / ratio
						xmax = maxX / ratio
						ymin = minY / ratio
						ymax = maxY / ratio

						n1 = (minX * xratio) + ((maxX - minX) * xratio / 2)
						n2 = (minY * yratio) + ((maxY - minY) * yratio / 2)
						n3 = (maxX - minX) * xratio
						n4 = (maxY - minY) * yratio

				if inputType == "folder" or inputType == "files":
					# 在帧上绘制帧编号、文本和时间戳
					timer = currentFrameInFile / fps
					ts = time.strftime("%H:%M:%S.", time.gmtime(timer)) + str(timer).split('.')[1][:3]
					cv2.putText(frame, "Frame: {} of {}".format(currentFrameInFile, fileFrameCount), (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
						0.45, (0, 0, 255), 1)
					cv2.putText(frame, "Time: {}".format(ts), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
						0.45, (0, 0, 255), 1)

				elif inputType == "webcam":
					# 在帧上绘制时间戳
					ts = currentTime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
					cv2.putText(frame, "{}".format(ts), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
						0.45, (0, 0, 255), 1)

				elif inputType == "network":
					# 在帧上绘制对应的网络视频流名称和时间戳
					ts = currentTime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
					cv2.putText(frame, rpiName, (10, 20),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
					cv2.putText(frame, "{}".format(ts), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
						0.45, (0, 0, 255), 1)

					# 更新帧记录中的新帧
					frameDict[rpiName] = frame

					# 使用帧记录中的图像构建分屏显示
					montages = build_montages(frameDict.values(), (w1, h1), (mW, mH))

				# 如果画面中有运动
				if text == "Motion":
					# 增加运动计数
					motionCounter += 1
					motionBeginTime = datetime.datetime.now()

					# 检查运动一致的帧数是否足够高
					if motionCounter >= minMotionFrames:

						# 将图像写入临时文件
						t = TempImage()

						if inputType == "folder" or inputType == "files":
							# 如果用户设定应采尽采，则按照用户设定的频率采集图像
							if captureImages[0] == "all":
								readFrameCounter += captureImages[1] - 10
								fvs.set(1, readFrameCounter)
								cv2.imwrite(t.path, frame)

							# 如果用户设定按帧采集，则按照用户设定的帧数采集图像
							elif captureImages[0] == "frame":
								readFrameCounter += 1 - 10
								fvs.set(1, readFrameCounter)

								while readFrameCounter <= captureImages[1]:
									cv2.imwrite(t.path, frame)

							# 如果用户设定按秒采集，则按照用户设定的秒数和频率采集图像
							elif captureImages[0] == "second":
								readFrameCounter += captureImages[2] - 10
								fvs.set(1, readFrameCounter)
		
								while (timestamp - motionBeginTime).seconds <= captureImages[1]:
									cv2.imwrite(t.path, frame)

						elif inputType == "webcam" or inputType == "network":
							cv2.imwrite(t.path, frame)

						naming = "{savePath}{autoPath}{timestamp}".format(
							savePath=savePath, autoPath=autoPath, timestamp=ts.replace(':', '_').replace('.', '_').replace(' ', '_').replace('-', '_'))
						namingAndAnnotation = "{savePath}{autoPath}{annotationPath}{timestamp}".format(
							savePath=savePath, autoPath=autoPath, annotationPath=annotationPath, timestamp=ts.replace(':', '_').replace('.', '_').replace(' ', '_').replace('-', '_'))

						try:
							naming2 = "{savePath}{autoPath}{rpiName}{timestamp}".format(
								savePath=savePath, autoPath=autoPath, rpiName=rpiName + "/", timestamp=ts.replace(':', '_').replace('.', '_').replace(' ', '_').replace('-', '_'))
							namingAndAnnotation2 = "{savePath}{autoPath}{rpiName}{annotationPath}{timestamp}".format(
								savePath=savePath, autoPath=autoPath, rpiName=rpiName + "/", annotationPath=annotationPath, timestamp=ts.replace(':', '_').replace('.', '_').replace(' ', '_').replace('-', '_'))
						except UnboundLocalError:
							pass

						# 保存图像
						if inputType == "folder" or inputType == "files" or inputType == "webcam":
							path = "{}.jpg".format(naming)
							cv2.imencode('.jpg', frameOriginal)[1].tofile(path)

						elif inputType == "network":
							path = "{}.jpg".format(naming2)
							cv2.imencode('.jpg', frameOriginal)[1].tofile(path)

						saveCounter += 1

						# 清除临时文件
						try:
							t.cleanup()
						except FileNotFoundError:
							pass
						except PermissionError:
							pass

						# 将图像标注写入文件
						if annotationType == "pascalvoc":
							# 创建文件结构
							annotation = ET.Element('annotation')
							folder = ET.SubElement(annotation, 'folder')
							filename = ET.SubElement(annotation, 'filename')
							pathTag = ET.SubElement(annotation, 'path')
							source = ET.SubElement(annotation, 'source')
							database = ET.SubElement(source, 'database')
							size = ET.SubElement(annotation, 'size')
							width = ET.SubElement(size, 'width')
							height = ET.SubElement(size, 'height')
							depth = ET.SubElement(size, 'depth')
							segmented = ET.SubElement(annotation, 'segmented')
							objectTag = ET.SubElement(annotation, 'object')
							name = ET.SubElement(objectTag, 'name')
							pose = ET.SubElement(objectTag, 'pose')
							truncated = ET.SubElement(objectTag, 'truncated')
							difficult = ET.SubElement(objectTag, 'difficult')
							bndbox = ET.SubElement(objectTag, 'bndbox')
							xminTag = ET.SubElement(bndbox, 'xmin')
							yminTag = ET.SubElement(bndbox, 'ymin')
							xmaxTag = ET.SubElement(bndbox, 'xmax')
							ymaxTag = ET.SubElement(bndbox, 'ymax')

							folder.text = savePath + autoPath
							filename.text = naming + ".jpg"
							pathTag.text = path
							database.text = "Default"
							width.text = str(ow)
							height.text = str(oh)
							depth.text = str(od)
							segmented.text = "0"
							name.text = "Object"
							pose.text = "Unspecified"

							if xmin == 0 or ymin == 0 or xmax == ow or ymax == oh:
								truncated.text = "1"
							else:
								truncated.text = "0"

							difficult.text = "0"
							xminTag.text = str(int(xmin))
							yminTag.text = str(int(ymin))
							xmaxTag.text = str(int(xmax))
							ymaxTag.text = str(int(ymax))

							# 使用结果创建新的 XML 文件
							annotationData = ET.tostring(annotation)
							if inputType == "folder" or inputType == "files" or inputType == "webcam":
								annotationFile = open("{}.xml".format(namingAndAnnotation), "wb")
							elif inputType == "network":
								annotationFile = open("{}.xml".format(namingAndAnnotation2), "wb")
							annotationFile.write(annotationData)
							annotationFile.close()
						
						elif annotationType == "yolo":
							if inputType == "folder" or inputType == "files" or inputType == "webcam":
								annotationFile = open("{}.txt".format(namingAndAnnotation), "w")
								annotationClassFile = open("{savePath}{autoPath}{annotationPath}classes.txt".format(
									savePath=savePath, autoPath=autoPath, annotationPath=annotationPath), "w")
							elif inputType == "network":
								annotationFile = open("{}.txt".format(namingAndAnnotation2), "w")
								annotationClassFile = open("{savePath}{autoPath}{rpiName}{annotationPath}classes.txt".format(
									savePath=savePath, autoPath=autoPath, rpiName=rpiName + "/", annotationPath=annotationPath), "w")
							
							annotationFile.write("{} {} {} {} {}".format(0, n1, n2, n3, n4))
							annotationFile.close()
							
							annotationClassFile.write("Object")
							annotationClassFile.close()

						# 重置运动计数器、重置为用户设定的读法
						motionCounter = 0	
						readFrameCounter += readFrames

						if inputType == "folder" or inputType == "files":
							fvs.set(1, readFrameCounter)

				# 如果画面中无运动
				else:
					motionCounter = 0

				# 在帧上绘制运动侦测状态
				cv2.putText(frame, "{}".format(text), (frame.shape[1] - 65, 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				fpsTimer.update()

				# 如果当前时间减去最近活视频流检查的时间大于规定的阈值，则检查网络视频流状态
				if (datetime.datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
					# 循环遍历所有以前处于活动状态的视频流

					for (rpiName, ts) in list(lastActive.items()):

						# 如果视频流最近未处于活动状态，从上一个活动记录和帧记录中删除该视频流
						if (datetime.datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
							print(Fore.RED + "\n[x] 断开连接 {}。".format(rpiName))
							print(Style.RESET_ALL) 
							lastActive.pop(rpiName)
							frameDict.pop(rpiName)

					# 将最近活动视频流检查时间设置为当前时间
					lastActiveCheck = datetime.datetime.now()

				# 检查用户是否设置在屏幕上显示视频画面
				if showVideo:
					if inputType == "files" or inputType == "folder":
						cv2.imshow("Input: Video", frame)

					elif inputType == "webcam":
						cv2.imshow("Input: Webcam", frame)

					elif inputType == "network":
						# 在屏幕上显示网络视频流的分屏
						for (b, montage) in enumerate(montages):
							cv2.imshow("Input: Network", montage)

				if not gui:
					# 如果用户按下 S 键，则跳过当前视频
					key = cv2.waitKey(1) & 0xFF

					if key == ord("s") or key == ord("q") or keyboard.is_pressed('s') or keyboard.is_pressed('q'):
						fpsTimer.stop()
						finishTime = datetime.datetime.now()

						if key == ord("s") or keyboard.is_pressed('s'):
							print(Fore.RED + "\n    用户于 {} 选择跳过当前视频。".format(finishTime))

						if key == ord("q") or keyboard.is_pressed('q'):
							print(Fore.RED + "\n    用户于 {} 选择中断本次采集。".format(finishTime))

						if inputType == "files" or inputType == "folder":
							print(Style.RESET_ALL + "    {} 的采集提前结束。".format(f))

						if inputType == "network":
							stopCapture()

						if saveCounter != 0:
							print(Style.RESET_ALL + "     - 总共采集：{} 张图像".format(saveCounter))
							print("     - 保存位置：{}{}".format(savePath, autoPath))
							print("     - 采集用时：{}".format(datetime.timedelta(seconds = fpsTimer.elapsed())))
							print("     - 平均帧率：{:.2f} fps".format(fpsTimer.fps()))
						else:
							print(Style.RESET_ALL + "    本次没有采集到图像。")

						print("\a")
						break

				# 写入 CSV 文件
				try:
					csvOutput.writerow([readFrameCounter, ts, len(locs)])
				except ValueError:
					pass

			# 停止进程
			if inputType == "folder" or inputType == "files":
				fvs.release()
			elif inputType == "webcam":
				fvs.stop()
			elif inputType == "network":
				sys.exit()

			if not gui:
				# 如果用户按下 Q 键，则中断进程
				try: 
					if key == ord("q") or keyboard.is_pressed('q'):
						break
				except UnboundLocalError:
					pass

		# 绘制视频信息图
		x1 = []
		x2 = []
		y1 = []

		# 用来正常显示中文
		plt.rcParams['font.sans-serif']=['Microsoft YaHei']

		if inputType == "files" or inputType == "folder":
			with open(savePath + autoPath + 'vinfo.csv', 'r', encoding='utf-8') as csvfile:
				plots = csv.reader(csvfile, delimiter=',')

				for row in plots:
					x1.append(row[0])
					x2.append(row[1])
					y1.append(row[2])

			x1n = x1[1:]
			x2n = x2[1:]
			y1n = y1[1:]
			y1n = [int(x) for x in y1n]

			plt.subplot(111)
			plt.figure(figsize=(15, 7))
			plt.bar(x1n,y1n)

			plt.title(u'视频信息: {}'.format(f))
			plt.legend([y1[0]])
			plt.grid(axis="y")
			plt.xlabel(u'时间码', labelpad=20)
			plt.ylabel(u'计数')

			try:
				plt.xticks(range(0, len(x1n), int(len(x1n)/20)), x2n[0:len(x2n):int(len(x2n)/20)], rotation=-45, ha="left", rotation_mode="anchor")
			except ValueError:
				break

			plt.subplots_adjust(bottom=0.25)
			plt.savefig(savePath + autoPath + 'vinfo.png')

	# 关闭所有打开的窗口
	cv2.destroyAllWindows()
	i = 1

	if gui:
		if saveLog:
			hiddenTxtText = hiddenTxt.get("1.0", "end-1c")
			with open("log/{}.log".format(logFileName), "w") as saveText:
				saveText.writelines(hiddenTxtText)
				saveText.close()
			hiddenTxt.delete("1.0", "end")
		progressBar.configure(value=100)
		progressLbl.configure(text="100.0%")
		progressBar.update()
		progressLbl.update()
		window.destroy()
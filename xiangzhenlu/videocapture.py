# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200625.2340

# 导入必要的包
import sys									  # 将终端输出保存到日志
import datetime								  # 时间戳
import imutils								  # 图像操作简便函数集
import time									  # 时间操作
import cv2									  # OpenCV
import os									  # 文件和文件夹操作
import fnmatch								  # 计算文件个数
import csv									  # 读取和保存 CSV 文件
import matplotlib.pyplot as plt				  # 绘图并保存
import tkinter as tk                          # 用户界面
import tkinter.ttk as ttk                     # 高级用户界面
from tkinter import *                         # 滚动条
from tkinter import messagebox                # 对话框
from tkinter.ttk import *                     # 进度条
from pyimagesearch.tempimage import TempImage # 保存临时文件
from imutils.video import count_frames	      # 计算帧数
from imutils.video import FPS				  # 计算采集时的平均帧率
from colorama import init, Fore, Back, Style  # 在终端输出彩色文字

def startCapture(fileList, jsonPath, showVideo, saveAnnotations, saveLog, inputType, inputFiles, inputFolder, savePath, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i):
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
		# redirection
		r_obj=__redirection__()
		sys.stdout=r_obj
		
		# redirect to console
		r_obj.to_console()
		
		# flush buffer
		r_obj.flush()
		
		# reset
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
		try:
			fpsTimer.stop()
			fvs.release()
			cv2.destroyAllWindows()
			window.after(100, stopCapture)
		except:
			pass

	# 如果使用图形界面，则加载它
	if gui:
		# 跳过采集函数
		def skipCapture(event):
			try:
				fpsTimer.stop()
				fvs.release()
				cv2.destroyAllWindows()
				return
			except _tkinter.TclError:
				pass

		# 各类提示函数
		def successInfo():
			messagebox.showinfo(title='已完成采集', message='图像采集已全部完成。')

		# 用户界面
		window = tk.Tk()
		window.title("")
		window.configure(background="#ffffff")
		window.rowconfigure(0, minsize=600, weight=1)
		window.columnconfigure(1, minsize=800, weight=1)
		window.geometry('800x250+320+610')
		window.resizable(0, 0)

		# 写入日志的隐藏文本域
		hiddenTxt = tk.Text(window)

		# 状态标签
		statusLbl = tk.Label(window)
		statusLbl.place(relx=0.025, rely=0.056, height=21, width=757)
		statusLbl.configure(activebackground="#f9f9f9")
		statusLbl.configure(activeforeground="black")
		statusLbl.configure(anchor='w')
		statusLbl.configure(background="#ffffff")
		statusLbl.configure(disabledforeground="#a3a3a3")
		statusLbl.configure(font="-family {Microsoft YaHei UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		statusLbl.configure(foreground="#000000")
		statusLbl.configure(highlightbackground="#d9d9d9")
		statusLbl.configure(highlightcolor="black")
		statusLbl.configure(text='''准备就绪''')

		# 跳过当前视频链接
		skipLnk = tk.Label(window)
		skipLnk.place(relx=0.025, rely=0.16, height=21, width=300)
		skipLnk.configure(activebackground="#f9f9f9")
		skipLnk.configure(activeforeground="black")
		skipLnk.configure(anchor='w')
		skipLnk.configure(background="#ffffff")
		skipLnk.configure(disabledforeground="#a3a3a3")
		skipLnk.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 1 -overstrike 0")
		skipLnk.configure(foreground="#0080ff")
		skipLnk.configure(highlightbackground="#d9d9d9")
		skipLnk.configure(highlightcolor="black")
		skipLnk.configure(justify='left')
		skipLnk.configure(text='''跳过''')
		skipLnk.configure(cursor="hand2")
		skipLnk.bind('<Button-1>', skipCapture)

		# 进度条
		progressBar = ttk.Progressbar(window)
		progressBar.place(relx=0.025, rely=0.32, relwidth=0.95, relheight=0.0
				, height=22)
		progressBar.configure(length="760")

		# 进度标签
		progressLbl = tk.Label(progressBar)
		progressLbl.pack()
		progressLbl.configure(text='''0.0%''')

		# 其他实时数据标签
		timeElapsedLbl = tk.Label(window)
		timeElapsedLbl.place(relx=0.025, rely=0.48, height=21, width=136)
		timeElapsedLbl.configure(activebackground="#f9f9f9")
		timeElapsedLbl.configure(activeforeground="black")
		timeElapsedLbl.configure(anchor='w')
		timeElapsedLbl.configure(background="#ffffff")
		timeElapsedLbl.configure(disabledforeground="#a3a3a3")
		timeElapsedLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		timeElapsedLbl.configure(foreground="#000000")
		timeElapsedLbl.configure(highlightbackground="#d9d9d9")
		timeElapsedLbl.configure(highlightcolor="black")
		timeElapsedLbl.configure(text='''已用时间：''')

		timeElapsedCountLbl = tk.Label(window)
		timeElapsedCountLbl.place(relx=0.2, rely=0.48, height=21
				, width=228)
		timeElapsedCountLbl.configure(activebackground="#f9f9f9")
		timeElapsedCountLbl.configure(activeforeground="black")
		timeElapsedCountLbl.configure(anchor='w')
		timeElapsedCountLbl.configure(background="#ffffff")
		timeElapsedCountLbl.configure(disabledforeground="#a3a3a3")
		timeElapsedCountLbl.configure(font="-family {Microsoft YaHei UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		timeElapsedCountLbl.configure(foreground="#000000")
		timeElapsedCountLbl.configure(highlightbackground="#d9d9d9")
		timeElapsedCountLbl.configure(highlightcolor="black")

		timeEstLbl = tk.Label(window)
		timeEstLbl.place(relx=0.025, rely=0.58, height=21, width=136)
		timeEstLbl.configure(activebackground="#f9f9f9")
		timeEstLbl.configure(activeforeground="black")
		timeEstLbl.configure(anchor='w')
		timeEstLbl.configure(background="#ffffff")
		timeEstLbl.configure(disabledforeground="#a3a3a3")
		timeEstLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		timeEstLbl.configure(foreground="#000000")
		timeEstLbl.configure(highlightbackground="#d9d9d9")
		timeEstLbl.configure(highlightcolor="black")
		timeEstLbl.configure(text='''估计剩余时间：''')

		timeEstCountLbl = tk.Label(window)
		timeEstCountLbl.place(relx=0.2, rely=0.58, height=21, width=228)
		timeEstCountLbl.configure(activebackground="#f9f9f9")
		timeEstCountLbl.configure(activeforeground="black")
		timeEstCountLbl.configure(anchor='w')
		timeEstCountLbl.configure(background="#ffffff")
		timeEstCountLbl.configure(disabledforeground="#a3a3a3")
		timeEstCountLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		timeEstCountLbl.configure(foreground="#000000")
		timeEstCountLbl.configure(highlightbackground="#d9d9d9")
		timeEstCountLbl.configure(highlightcolor="black")

		fpsLbl = tk.Label(window)
		fpsLbl.place(relx=0.513, rely=0.48, height=21, width=136)
		fpsLbl.configure(activebackground="#f9f9f9")
		fpsLbl.configure(activeforeground="black")
		fpsLbl.configure(anchor='w')
		fpsLbl.configure(background="#ffffff")
		fpsLbl.configure(disabledforeground="#a3a3a3")
		fpsLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		fpsLbl.configure(foreground="#000000")
		fpsLbl.configure(highlightbackground="#d9d9d9")
		fpsLbl.configure(highlightcolor="black")
		fpsLbl.configure(text='''实时采集帧率：''')

		fpsCountLbl = tk.Label(window)
		fpsCountLbl.place(relx=0.688, rely=0.48, height=21, width=228)
		fpsCountLbl.configure(activebackground="#f9f9f9")
		fpsCountLbl.configure(activeforeground="black")
		fpsCountLbl.configure(anchor='w')
		fpsCountLbl.configure(background="#ffffff")
		fpsCountLbl.configure(disabledforeground="#a3a3a3")
		fpsCountLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		fpsCountLbl.configure(foreground="#000000")
		fpsCountLbl.configure(highlightbackground="#d9d9d9")
		fpsCountLbl.configure(highlightcolor="black")

		imgLbl = tk.Label(window)
		imgLbl.place(relx=0.513, rely=0.58, height=21, width=136)
		imgLbl.configure(activebackground="#f9f9f9")
		imgLbl.configure(activeforeground="black")
		imgLbl.configure(anchor='w')
		imgLbl.configure(background="#ffffff")
		imgLbl.configure(disabledforeground="#a3a3a3")
		imgLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		imgLbl.configure(foreground="#000000")
		imgLbl.configure(highlightbackground="#d9d9d9")
		imgLbl.configure(highlightcolor="black")
		imgLbl.configure(text='''已采集图片：''')

		imgCountLbl = tk.Label(window)
		imgCountLbl.place(relx=0.688, rely=0.58, height=21, width=228)
		imgCountLbl.configure(activebackground="#f9f9f9")
		imgCountLbl.configure(activeforeground="black")
		imgCountLbl.configure(anchor='w')
		imgCountLbl.configure(background="#ffffff")
		imgCountLbl.configure(disabledforeground="#a3a3a3")
		imgCountLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		imgCountLbl.configure(foreground="#000000")
		imgCountLbl.configure(highlightbackground="#d9d9d9")
		imgCountLbl.configure(highlightcolor="black")

		# 停止采集按钮
		stopBtn = tk.Button(window)
		stopBtn.place(relx=0.413, rely=0.760, height=38, width=139)
		stopBtn.configure(activebackground="#ececec")
		stopBtn.configure(activeforeground="#000000")
		stopBtn.configure(background="#d9d9d9")
		stopBtn.configure(disabledforeground="#a3a3a3")
		stopBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
		stopBtn.configure(foreground="#000000")
		stopBtn.configure(highlightbackground="#d9d9d9")
		stopBtn.configure(highlightcolor="black")
		stopBtn.configure(pady="0")
		stopBtn.configure(text='''█  停止采集''')
		stopBtn.configure(command=stopCapture)

	if showVideo:
		showVideo1 = "是"
	else:
		showVideo1 = "否"

	if saveAnnotations:
		saveAnnotations1 = "是"
	else:
		saveAnnotations1 = "否"

	if saveLog:
		saveLog1 = "是"
	else:
		saveLog1 = "否"

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

	print("\n\n[i] 将从 {} 个视频中采集图像。".format(len(fileList)))
	print("    使用 {} 中的设置采集：".format(jsonPath))
	print('''     - 显示采集窗口：　　{}
     - 保存图像中的标注：{}
     - 保存采集日志：　　{}
     - 输出目录：　　　　{}
     - 视频读法：　　　　每 {} 帧取一帧读
     - 采集算法：　　　　{}
     - 采集方式：　　　　{}
     - 运动帧最小值：　　{}
     - 阈值增量最小值：　{}
     - 轮廓区域最小值：　{}
     - 设置文件创建时间：{}
     - 设置文件备注：　　{}\n'''.format(showVideo1, saveAnnotations1, saveLog1, savePath, readFrames, captureType1, captureImages1, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes))
	print("\n[i] 本次采集开始于 {}。\n".format(startTime))

	# 如果用户指定了无效的采集来源，则中止图像采集
	if (inputType == "folder") or (inputType == "files"):
		pass
	else:
		print(Fore.RED + "\n\n[x] 图像采集已中止，因为 input_type 参数无效。")
		print(Fore.RED + "    采集来源：folder（文件夹），files（视频文件列表）。")
		print(Style.RESET_ALL + "\a") 
		sys.exit(0)

	# 遍历所有视频文件
	for n in range(len(fileList)):
		f = fileList[n]
		
		if inputType == "folder":
			file = inputFolder + f
		elif inputType == "files":
			file = f

		# 创建采集图片保存目录
		autoPath = f.split("/")[-1].replace(":", "_").replace(" ", "_") + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"
		
		# 如果用户未指定保存目录，将图像直接保存在当前目录下、以视频 + 设置名称命名的子文件夹中
		if savePath == "":
			try:
				os.mkdir(autoPath)
			except FileExistsError:
				pass

		# 否则，将图像保存在用户指定目录下的、以视频 + 设置名称命名的子文件夹中
		else:
			try:
				os.makedirs(savePath + autoPath)
			except FileExistsError:
				pass

		# 计算所有待采集视频的帧数之和
		totalFrameCount = 0

		for m in fileList:
			if inputType == "folder":
				mFile = inputFolder + m
			elif inputType == "files":
				mFile = m

			frameCount = int(count_frames(mFile, override=False))
			totalFrameCount += frameCount

		# 计算累计采集帧数和累计保存文件数
		if n > 0:
			if inputType == "folder":
				lastFile = inputFolder + fileList[n-1]
			elif inputType == "files":
				lastFile = fileList[n-1]
			
			lastFileFrameCount = int(count_frames(lastFile, override=False))
			cumulatedFrameCount += lastFileFrameCount

			lastFileAutoPath = lastFile.split("/")[-1].replace(":", "_").replace(" ", "_") + "__" + jsonPath.split("/")[-1].split(".")[0].replace(":", "_").replace(" ", "_") + "/"
			lastFileSaveCount = len(fnmatch.filter(os.listdir(savePath + lastFileAutoPath), '*.jpg'))
			cumulatedSaveCount += lastFileSaveCount
		else:
			cumulatedFrameCount = 0
			cumulatedSaveCount = 0

		# 开始将当前视频信息写入 CSV 文件
		with open(savePath + autoPath + 'vinfo.csv', 'w', newline='', encoding='utf-8') as fOutput:
			csvOutput = csv.writer(
				fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csvOutput.writerow(["帧", "时间码", "侦测到的全部运动", "按设定标准采集的运动"])

			# 从视频文件中读取
			print("\n[i] 正在采集 ({}/{})：{}...".format(n + 1, len(fileList), f))

			if gui:
				statusLbl.configure(text="正在采集 ({}/{})：{}...".format(n + 1, len(fileList), f.split("/")[-1]))
				statusLbl.update()

			fvs = cv2.VideoCapture(file)
			time.sleep(1.0)

			# 初始化平均帧、当前帧的前两帧、最后保存的时间戳、读帧计数器、帧运动计数器、保存文件计数器和读帧计时器
			avg = None
			lastFrame1 = None
			lastFrame2 = None
			readFrameCounter = 0
			motionCounter = 0
			fpsTimer = FPS().start()

			saveCounter = 0
			allSaveCounter = 0

			# 遍历视频帧
			while True:
				if gui:
					window.update()

				# 按照用户设定的读法抓取帧，初始化时间戳和有动作 / 无动作的文本
				frame = fvs.read()
				frame = frame[1]

				readFrameCounter += readFrames
				fvs.set(1, readFrameCounter)

				currentFrameInFile = int(fvs.get(cv2.CAP_PROP_POS_FRAMES))
				fileFrameCount = int(fvs.get(cv2.CAP_PROP_FRAME_COUNT))
				fps = fvs.get(cv2.CAP_PROP_FPS)

				timestamp = datetime.datetime.now()
				text = ""

				# 如果用户指定了无效的采集算法，则中止图像采集
				if (captureType == "avg") or (captureType == "two") or (captureType == "three"):
					pass
				else:
					fvs.release()
					print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_type 参数无效。")
					print(Fore.RED + "    采集算法：avg（多帧加权平均法），two（二帧差分法），three（三帧差分法）。")
					print(Style.RESET_ALL + "\a") 
					break

				# 如果用户指定了无效的采集方式，则中止图像采集
				if (captureImages[0] == "all") or (captureImages[0] == "frame") or (captureImages[0] == "second"):
					pass
				else:
					fvs.release()
					print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_images 参数无效。")
					print(Fore.RED + "    参数格式：['采集方式', 采集数值 1, 采集数值 2]。")
					print(Fore.RED + "    采集方式：all（应采尽采），frame（按帧采集），second（按秒采集）。")
					print(Style.RESET_ALL + "\a") 
					i = 5
					break

				# 计算当前视频的采集进度和估计剩余时间
				for a in range(1):
					percent = (currentFrameInFile + cumulatedFrameCount) / totalFrameCount * 100.0
					currentTime = datetime.datetime.now()
					elapsedTime = currentTime - startTime
					elapsedTime = elapsedTime.total_seconds()

					try:
						currentFps = (currentFrameInFile + cumulatedFrameCount) / elapsedTime
						remainingTime = (totalFrameCount - cumulatedFrameCount - currentFrameInFile) / currentFps

					except ZeroDivisionError:
						pass

					print("\r    总进度 {}%    估计剩余时间 {}".format(str('%.1f'%percent), datetime.timedelta(seconds = remainingTime)), end="")

					if gui:
						progressBar.configure(value=percent)
						progressLbl.configure(text="{}%".format(str('%.1f'%percent)))
						timeElapsedCountLbl.configure(text="{}".format(datetime.timedelta(seconds = elapsedTime)))
						timeEstCountLbl.configure(text="{}".format(datetime.timedelta(seconds = remainingTime)))
						fpsCountLbl.configure(text="{:.2f} fps".format(currentFps))
						imgCountLbl.configure(text="{} 张".format(cumulatedSaveCount + saveCounter))

				# 如果无法抓取帧，则视频已播完
				if frame is None:
					n += 1
					fpsTimer.stop()
					print("\n    采集完毕。")

					if saveCounter != 0:
						print("     - 总共采集：{} 张图像".format(saveCounter))
						print("     - 保存位置：{}{}".format(savePath, autoPath))
						print("     - 采集用时：{}".format(datetime.timedelta(seconds = fpsTimer.elapsed())))
						print("     - 平均帧率：{:.2f} fps\n".format(fpsTimer.fps()))
					else:
						print("    本次没有采集到图像。")

					if n == len(fileList):
						if gui:
							successInfo()
						print(Fore.GREEN + "\n[v] 图像采集已全部完成。")
						
						# 进程结束时间
						finishTime = datetime.datetime.now()
						timePassed = finishTime - startTime
						print(Fore.GREEN + "    本次采集完成于 {}，共耗时 {}。".format(finishTime, timePassed))
						print(Style.RESET_ALL + "\a") 

					break

				# 复制当前帧（为了保存无标注的图片）、调整帧大小、将其转换为灰度，然后使其模糊
				frameOriginal = frame.copy()
				frame = imutils.resize(frame, width=500)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (21, 21), 0)

				# 如果用户指定的图像采集算法为多帧加权平均法
				if captureType == "avg":

					# 如果平均帧为 None，则将其初始化
					if avg is None:
						avg = gray.copy().astype("float")
						continue

					# 累加当前帧和先前帧之间的加权平均值，然后计算当前帧和此动态平均值之间的差
					cv2.accumulateWeighted(gray, avg, 0.5)
					frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

					# 对增量图像进行阈值处理，对阈值图像进行扩张以填充孔洞
					thresh = cv2.threshold(frameDelta, minDeltaThresh, 255,
						cv2.THRESH_BINARY)[1]
					thresh = cv2.dilate(thresh, None, iterations=2)

				# 如果用户指定的图像采集算法为二帧差分法
				elif captureType == "two":
					
					# 如果前一帧为 None，则将其初始化 
					if lastFrame1 is None: 
						lastFrame1 = frame
						continue 
				
					# 计算当前帧和前一帧的不同 
					frameDelta = cv2.absdiff(lastFrame1, frame) 
				
					# 当前帧设置为下一帧的前一帧 
					lastFrame1 = frame.copy() 
				
					# 结果转为灰度图 
					thresh = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY) 
				
					# 图像二值化 
					thresh = cv2.threshold(thresh, minDeltaThresh, 255, cv2.THRESH_BINARY)[1] 
				
				# 如果用户指定的图像采集算法为三帧差分法
				elif captureType == "three":

					# 如果前二帧为 None，则将其初始化，并计算前两帧的不同
					if lastFrame2 is None:
						if lastFrame1 is None:
							lastFrame1 = frame
						else:
							lastFrame2 = frame
							global frameDelta1  # 全局变量
							frameDelta1 = cv2.absdiff(lastFrame1, lastFrame2)  # 帧差一
						continue

					# 计算当前帧和前两帧的不同，计算三帧差分
					frameDelta = cv2.absdiff(lastFrame2, frame)  # 帧差二
					thresh = cv2.bitwise_and(frameDelta1, frameDelta)  # 图像与运算
					thresh2 = thresh.copy()

					# 当前帧设置为下一帧的前一帧，前一帧设为下一帧的前二帧，帧差二设为帧差一
					lastFrame1 = lastFrame2
					lastFrame2 = frame.copy()
					frameDelta1 = frameDelta

					# 结果转为灰度图
					thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

					# 图像二值化
					thresh = cv2.threshold(thresh, minDeltaThresh, 255, cv2.THRESH_BINARY)[1]

					# 去除图像噪声，先腐蚀再膨胀（形态学开运算）
					thresh = cv2.dilate(thresh, None, iterations=3)
					thresh = cv2.erode(thresh, None, iterations=1)

				# 对阈值图像取轮廓
				cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
					cv2.CHAIN_APPROX_SIMPLE)
				cnts = imutils.grab_contours(cnts)
				cntsValid = 0

				# 遍历轮廓
				for c in cnts:
					# 如果轮廓太小，则忽略它
					if cv2.contourArea(c) < minArea:
						cntsValid -= 1
						continue

					# 计算轮廓的边界框，将其绘制在帧上，并更新文本
					(x, y, w, h) = cv2.boundingRect(c)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					text = "Motion"

				# 使用视频播放时间，并显示帧编号
				timer = currentFrameInFile / fps
				cv2.putText(frame, "Frame: {} of {}".format(currentFrameInFile, fileFrameCount), (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
					0.45, (0, 0, 255), 1)

				# 在帧上绘制文本和时间戳
				ts = time.strftime("%H:%M:%S.", time.gmtime(timer)) + str(timer).split('.')[1][:3]
				cv2.putText(frame, "Time: {}".format(ts), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
					0.45, (0, 0, 255), 1)

				# 如果画面中有运动
				if text == "Motion":

					# 增加运动计数
					motionCounter += 1
					motionBeginTime = datetime.datetime.now()

					# 检查运动一致的帧数是否足够高
					if motionCounter >= minMotionFrames:

						# 将图像写入临时文件
						t = TempImage()

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

						path = "{savePath}{autoPath}{timestamp}.jpg".format(
										savePath=savePath, autoPath=autoPath, timestamp=ts.replace(':', '_').replace('.', '_'))

						# 如果用户设定保存采集批注，则保存带有批注的压缩图像
						if saveAnnotations:
							cv2.imencode('.jpg', frame)[1].tofile(path)

						# 如果用户设定不保存采集批注，则保存不带批注的原始图像
						else:
							cv2.imencode('.jpg', frameOriginal)[1].tofile(path)

						saveCounter += 1

						# 清除临时文件
						try:
							t.cleanup()
						except FileNotFoundError:
							pass
						except PermissionError:
							pass

						# 重置运动计数器、重置为用户设定的读法
						motionCounter = 0	
						readFrameCounter += readFrames
						fvs.set(1, readFrameCounter)

				# 如果画面中无运动
				else:
					motionCounter = 0

				# 在帧上绘制运动侦测状态
				cv2.putText(frame, "{}".format(text), (frame.shape[1] - 65, 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				fpsTimer.update()

				# 检查用户是否设置在屏幕上显示视频画面
				if showVideo:
					# 在三个窗口中显示视频回放、阈值和帧增量
					cv2.imshow("Video", frame)
					cv2.imshow("Thresh", thresh)
					cv2.imshow("Frame Delta", frameDelta)

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

						print(Style.RESET_ALL + "    {} 的采集提前结束。".format(f))

						if saveCounter != 0:
							print("     - 总共采集：{} 张图像".format(saveCounter))
							print("     - 保存位置：{}{}".format(savePath, autoPath))
							print("     - 采集用时：{}".format(datetime.timedelta(seconds = fpsTimer.elapsed())))
							print("     - 平均帧率：{:.2f} fps".format(fpsTimer.fps()))
						else:
							print("    本次没有采集到图像。")

						print("\a")
						break

				# 写入 CSV 文件
				csvOutput.writerow([readFrameCounter, ts, len(cnts), len(cnts) + cntsValid])

			# 停止进程
			fvs.release()

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
		y2 = []

		plt.rcParams['font.sans-serif']=['Microsoft YaHei'] # 用来正常显示中文

		with open(savePath + autoPath + 'vinfo.csv', 'r', encoding='utf-8') as csvfile:
			plots = csv.reader(csvfile, delimiter=',')

			for row in plots:
				x1.append(row[0])
				x2.append(row[1])
				y1.append(row[2])
				y2.append(row[3])

		x1n = x1[1:]
		x2n = x2[1:]
		y1n = y1[1:]
		y2n = y2[1:]
		y1n = [int(x) for x in y1n]
		y2n = [int(x) for x in y2n]

		plt.subplot(111)
		plt.figure(figsize=(15, 7))
		plt.bar(x1n,y1n,alpha=0.5)
		plt.bar(x1n,y2n)

		plt.title(u'视频信息: {}'.format(f))
		plt.legend([y1[0], y2[0]])
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
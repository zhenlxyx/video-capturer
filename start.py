# 用法
# 正常启动，加载 conf.json 配置文件 python start.py
# 静默启动，加载 conf.json 配置文件 pythonw start.py
# 正常启动，加载用户自定义的配置文件 python start.py --conf conf_2.json
# 静默启动，加载用户自定义的配置文件 pythonw start.py --conf conf_2.json

# 导入必要的包
import argparse								  # 支持命令行参数
import warnings								  # 支持系统警告信息操作
import sys									  # 支持日志等系统操作
import datetime								  # 支持时间戳
import imutils								  # OpenCV 和 Python 进行图像操作的简便函数集
import json									  # 支持用户配置
import time									  # 支持时间操作
import cv2									  # OpenCV
import os									  # 支持文件和文件夹操作
from os import listdir						  # 支持文件列表
from os.path import isfile, join			  # 支持文件操作
from pyimagesearch.tempimage import TempImage # 支持保存临时文件
from imutils.video import FPS				  # 支持计算采集时的平均帧率
from colorama import init, Fore, Back, Style  # 支持在终端输出彩色文字

# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", 
	help="JSON 用户配置文件的路径")
args = vars(ap.parse_args())

# 过滤警告并加载配置
warnings.filterwarnings("ignore")

init(convert=True)

if args.get("conf", None) is None:
	conf = json.load(open("conf.json"))
else:
	conf = json.load(open(args["conf"]))

save_path = conf["output_folder"]
fileList = [f for f in listdir(conf["input_folder"]) if isfile(join(conf["input_folder"], f)) and not f.startswith('.')]

startTime = datetime.datetime.now()
logFileName = time.strftime("%H:%M:%S.").replace(':', '_').replace('.', '_')

# 同时在终端显示结果，并保存到日志文件
class __redirection__:
    
    def __init__(self):
        self.buflist =[]
        self.__console__=sys.stdout
        
    def write(self, output_stream):
        self.buflist.append(out_stream)
        
    def to_console(self):
        sys.stdout=self.__console__
        print(self.buflist)
    
    def flush(self):
        self.buflist=[]
        
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

# 如果用户指定了保存日志文件，则在 log/ 目录下保存
if conf["save_log"]:
	try:
		os.mkdir("log/")
	except FileExistsError:
		pass

	sys.stdout = Logger("log/{}.log".format(logFileName))

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
""")

# 进程开始时间
print("\n[i] 本次采集开始于 {}。\n".format(startTime))

for n in range(len(fileList)):
	f = fileList[n]
	file = conf["input_folder"] + f

	# 从视频文件中读取
	print("\n[i] 正在采集 ({}/{})：{}...".format(n + 1, len(fileList), f))
	fvs = cv2.VideoCapture(file)
	auto_path = f.split(".")[0] + "/"
	time.sleep(1.0)

	# 初始化平均帧、当前帧的前两帧、最后保存的时间戳、读帧计数器、帧运动计数器、保存文件计数器和读帧计时器
	avg = None
	lastFrame1 = None
	lastFrame2 = None
	readFrameCounter = 0
	motionCounter = 0
	saveCounter = 0
	fpsTimer = FPS().start()

	# 遍历视频帧
	while True:
		# 按照用户设定的读法抓取帧，初始化时间戳和 Motion / No Motion 的文本
		frame = fvs.read()
		frame = frame[1]

		readFrameCounter += conf["read_frames"]
		fvs.set(1, readFrameCounter)

		cf = int(fvs.get(cv2.CAP_PROP_POS_FRAMES))
		fc = int(fvs.get(cv2.CAP_PROP_FRAME_COUNT))
		fps = fvs.get(cv2.CAP_PROP_FPS)

		timestamp = datetime.datetime.now()
		text = ""

		# 如果用户指定了无效的采集算法，则中止图像采集
		if (conf["capture_type"] == "avg") or (conf["capture_type"] == "two") or (conf["capture_type"] == "three"):
			pass
		else:
			fvs.release()
			print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_type 参数无效。")
			print(Fore.RED + "    采集算法：avg（多帧加权平均法），two（二帧差分法），three（三帧差分法）。")
			print(Style.RESET_ALL + "\a") 
			break

		# 如果用户指定了无效的采集方式，则中止图像采集
		if (conf["capture_images"][0] == "all") or (conf["capture_images"][0] == "frame") or (conf["capture_images"][0] == "second"):
			pass
		else:
			fvs.release()
			print(Fore.RED + "\n\n[x] 图像采集已中止，因为 capture_images 参数无效。")
			print(Fore.RED + "    参数格式：['采集方式', 采集数值 1, 采集数值 2]。")
			print(Fore.RED + "    采集方式：all（应采尽采），frame（按帧采集），second（按秒采集）。")
			print(Style.RESET_ALL + "\a") 
			break

		# 计算当前视频的采集进度
		for i in range(1):
			try:
				percent = cf / fc * 100.0
				print("\r    "+str('%.1f'%percent)+"%", end="")
			except ZeroDivisionError:
				pass

		# 如果无法抓取帧，则视频已播完
		if frame is None:
			n += 1
			fpsTimer.stop()
			print("\r    100.0%...采集完毕。")

			if saveCounter != 0:
				print("    总共采集：{} 张图像".format(saveCounter))
				print("    保存位置：{}{}".format(save_path, auto_path))
				print("    采集用时：{:.2f} 秒".format(fpsTimer.elapsed()))
				print("    平均帧率：{:.2f} fps\n".format(fpsTimer.fps()))
			else:
				print("    本次没有采集到图像。")

			if n == len(fileList):
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
		if conf["capture_type"] == "avg":

			# 如果平均帧为 None，则将其初始化
			if avg is None:
				avg = gray.copy().astype("float")
				continue

			# 累加当前帧和先前帧之间的加权平均值，然后计算当前帧和此动态平均值之间的差
			cv2.accumulateWeighted(gray, avg, 0.5)
			frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

			# 对增量图像进行阈值处理，对阈值图像进行扩张以填充孔洞
			thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
				cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh, None, iterations=2)

		# 如果用户指定的图像采集算法为二帧差分法
		elif conf["capture_type"] == "two":
			
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
			thresh = cv2.threshold(thresh, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1] 
		
		# 如果用户指定的图像采集算法为三帧差分法
		elif conf["capture_type"] == "three":

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
			thresh = cv2.threshold(thresh, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]

			# 去除图像噪声，先腐蚀再膨胀（形态学开运算）
			thresh = cv2.dilate(thresh, None, iterations=3)
			thresh = cv2.erode(thresh, None, iterations=1)

		# 对阈值图像取轮廓
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# 遍历轮廓
		for c in cnts:
			# 如果轮廓太小，则忽略它
			if cv2.contourArea(c) < conf["min_area"]:
				continue

			# 计算轮廓的边界框，将其绘制在帧上，并更新文本
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "Motion"

		# 使用视频播放时间，并显示帧编号
		timer = cf / fps
		cv2.putText(frame, "Frame: {} of {}".format(cf, fc), (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
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

			# 将图像写入临时文件
			t = TempImage()

			# 如果用户设定应采尽采，则按照用户设定的频率采集图像
			if conf["capture_images"][0] == "all":
				readFrameCounter += conf["capture_images"][1] - 10
				fvs.set(1, readFrameCounter)
				cv2.imwrite(t.path, frame)

			# 如果用户设定按帧采集，则按照用户设定的帧数采集图像
			elif conf["capture_images"][0] == "frame":
				readFrameCounter += 1 - 10
				fvs.set(1, readFrameCounter)
				while readFrameCounter <= conf["capture_images"][1]:
					cv2.imwrite(t.path, frame)

			# 如果用户设定按秒采集，则按照用户设定的秒数和频率采集图像
			elif conf["capture_images"][0] == "second":
				readFrameCounter += conf["capture_images"][2] - 10
				fvs.set(1, readFrameCounter)
				while (timestamp - motionBeginTime).seconds <= conf["capture_images"][1]:
					cv2.imwrite(t.path, frame)

			# 如果用户未指定存储目录，将图像直接存储在当前目录下、以视频名称命名的子文件夹中
			if save_path == "":
				try:
					os.mkdir(auto_path)
				except FileExistsError:
					pass

			# 否则，将图像存储在用户指定目录下的、以视频名称命名的子文件夹中
			else:
				try:
					os.makedirs(save_path + auto_path)
				except FileExistsError:
					pass

			path = "{save_path}{auto_path}{timestamp}.jpg".format(
							save_path=save_path, auto_path=auto_path, timestamp=ts.replace(':', '_').replace('.', '_'))

			# 如果用户设定保存采集批注，则保存带有批注的压缩图像
			if conf["save_annotations"]:
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

			# 重置运动计数器、重置为用户设定的读法
			if conf["show_detail"]:
				print("... 采集 {}".format(ts))

			motionCounter = 0	
			readFrameCounter += conf["read_frames"]
			fvs.set(1, readFrameCounter)

		# 如果画面中无运动
		else:
			motionCounter = 0

		# 在帧上绘制读取进度和运动侦测状态
		percent = cf / fc * 100.0
		cv2.putText(frame, str('%.1f'%percent)+"%", (frame.shape[1] - 60, 20), cv2.FONT_HERSHEY_SIMPLEX,
			0.45, (0, 255, 0), 2)
		cv2.putText(frame, "{}".format(text), (frame.shape[1] - 65, 40),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		# 检查用户是否设置在屏幕上显示视频画面
		if conf["show_video"]:
			# 在三个窗口中显示视频回放、阈值和帧增量
			cv2.imshow("Video Playback", frame)
			cv2.imshow("Thresh", thresh)
			cv2.imshow("Frame Delta", frameDelta)
			key = cv2.waitKey(1) & 0xFF
			fpsTimer.update()

		# 如果用户按下 S 键，则跳过当前视频
		if key == ord("s") or key == ord("q"):
			fpsTimer.stop()
			finishTime = datetime.datetime.now()

			if key == ord("s"):
				print(Fore.RED + "\n    用户于 {} 选择跳过当前视频。".format(finishTime))

			if key == ord("q"):
				print(Fore.RED + "\n    用户于 {} 中断进程。".format(finishTime))

			print(Style.RESET_ALL + "    {} 的采集提前结束。".format(f))

			if saveCounter != 0:
				print("    总共采集：{} 张图像".format(saveCounter))
				print("    保存位置：{}{}".format(save_path, auto_path))
				print("    采集用时：{:.2f} 秒".format(fpsTimer.elapsed()))
				print("    平均帧率：{:.2f} fps".format(fpsTimer.fps()))
			else:
				print("    本次没有采集到图像。")

			print("\a")
			break

	# 停止进程
	fvs.release()

	# 如果用户按下 Q 键，则中断进程
	if key == ord("q"):
		break

# 关闭所有打开的窗口
cv2.destroyAllWindows()
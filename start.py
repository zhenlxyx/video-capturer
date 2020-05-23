# 用法
# 通过网络摄像头获取视频 python start.py
# 通过文件获取视频并加载用户配置 python start.py --video input/example_01.mp4 --conf conf.json

# 导入必要的包
from pyimagesearch.tempimage import TempImage # 支持保存临时文件
from imutils.video import VideoStream 		  # 支持读取网络摄像头
import argparse								  # 支持命令行参数
import warnings								  # 支持系统警告信息操作
import datetime								  # 支持时间戳
import imutils								  # OpenCV 和 Python 进行图像操作的简便函数集
import json									  # 支持用户配置
import time									  # 支持时间操作
import cv2									  # OpenCV
import os									  # 支持文件和文件夹操作

# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="视频文件的路径")
ap.add_argument("-c", "--conf", required=True,
	help="JSON 用户配置文件的路径")
args = vars(ap.parse_args())

# 过滤警告并加载配置
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

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

# 如果 video 参数为 None，从网络摄像头中读取
if args.get("video", None) is None:
	print("[信息] 正在读取网络摄像头...")
	vs = VideoStream(src=0).start()
	auto_path = "webcam/"
	time.sleep(2.0)

# 否则，从视频文件中读取
else:
	print("[信息] 正在读取视频文件...")
	vs = cv2.VideoCapture(args["video"])
	# auto_path = args.get("video", None).split("/")[1] + "/"
	auto_path = args.get("video", None).split("/")[1].split(".")[0] + "/"

# 初始化平均帧、最后保存的时间戳和帧运动计数器
avg = None
lastSaved = datetime.datetime.now()
motionCounter = 0

# 遍历视频帧
while True:
	# 抓取当前帧并初始化时间戳和 Motion / No Motion 的文本
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	timestamp = datetime.datetime.now()
	text = "No Motion"

	# 如果无法抓取帧，则视频已播完
	if frame is None:
		print("\n[成功] 图像采集完毕。\n")
		break

	# 调整帧大小，将其转换为灰度，然后使其模糊
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# 如果平均帧为 None，则将其初始化
	if avg is None:
		print("[信息] 正在采集图像...\n")
		avg = gray.copy().astype("float")
		continue

	# 累加当前帧和先前帧之间的加权平均值，然后计算当前帧和此动态平均值之间的差
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	# 对增量图像进行阈值处理，对阈值图像进行扩张以填充孔洞，然后对阈值图像取轮廓
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# 遍历轮廓
	for c in cnts:
		# 如果轮廓太小，则忽略它
		if cv2.contourArea(c) < conf["min_area"]:
			continue

		# 计算轮廓的边界框，将其绘制在帧上，并更新文本
		# (x, y, w, h) = cv2.boundingRect(c)
		# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Motion"

	# 在帧上绘制文本和时间戳
	ts = timestamp.strftime("%A %d %B %Y %I %M %S %f %p")
	# cv2.putText(frame, "Status: {}".format(text), (10, 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	# 	0.35, (0, 0, 255), 1)

	# 如果画面中有运动
	if text == "Motion":
		# 检查保存之间是否经过了足够的时间
		if (timestamp - lastSaved).seconds >= conf["min_save_seconds"]:
			# 增加运动计数
			motionCounter += 1

			# 检查连贯运动的帧数是否足够多
			if motionCounter >= conf["min_motion_frames"]:
				# 将图像写入临时文件
				t = TempImage()
				cv2.imwrite(t.path, frame)

				# 将图像保存到本地磁盘并清理临时图像
				print("[保存] {}".format(ts))
				save_path = conf["output_folder"]

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
						save_path=save_path, auto_path=auto_path, timestamp=ts)
				cv2.imencode('.jpg', frame)[1].tofile(path)
				t.cleanup()

				# 更新上次保存的时间戳并重置运动计数器
				lastSaved = timestamp
				motionCounter = 0

	# 如果画面中无运动
	else:
		motionCounter = 0

	# 检查用户是否设置在屏幕上显示视频画面
	if conf["show_video"]:
		# 在三个窗口中显示视频回放、阈值和帧增量
		cv2.imshow("Video Playback", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF

		# 如果用户按下 Q 键，则中断进程
		if key == ord("q"):
			print("\n[信息] 用户中断进程。\n")
			break

# 停止进程并关闭所有打开的窗口
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
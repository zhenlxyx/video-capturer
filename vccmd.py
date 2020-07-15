# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200715.1435

# 用法

'''
正常采集，加载 conf.json 配置文件，[采集单个文件]
python vccmd.py -i files -p input/example_01.mp4

正常采集，加载 conf.json 配置文件，[采集整个目录]
python vccmd.py -i folder -p input/

正常采集，加载 conf.json 配置文件，[采集摄像头]
python vccmd.py -i webcam

正常采集，加载 conf.json 配置文件，[采集网络视频流]
python vccmd.py -i network

正常采集，[加载用户自定义的配置文件]，采集单个文件
python vccmd.py -c conf_2.json -i files -p input/example_01.mp4

[静默采集]，加载 conf.json 配置文件，采集单个文件
pythonw vccmd.py -i files -p input/example_01.mp4
'''

# 导入必要的包
import argparse								  # 命令行参数
import warnings								  # 系统警告信息
import sys									  # 系统操作
import json									  # 用户配置
import time									  # 时间操作
import os									  # 文件和文件夹操作
import socket								  # 网络操作
from os import listdir						  # 文件列表
from os.path import isfile, join			  # 文件操作
from colorama import init, Fore, Back, Style  # 在终端输出彩色文字
from xiangzhenlu import videocapture as vc	  # 采集视频中动态的图像

# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", 
	help="JSON 用户设置文件的路径")
ap.add_argument("-i", "--input", required=True,
	help="指定采集来源：folder（文件夹），files（单个视频文件），webcam（摄像头），network（网络视频流）")
ap.add_argument("-p", "--path", 
	help="待采集目录或单个文件的路径")
args = vars(ap.parse_args())

# 过滤警告并加载配置
warnings.filterwarnings("ignore")

init(convert=True)

if (args.get("input") == "folder" or args.get("input") == "files") and args.get("path") is None:
	print(Fore.RED + "\n\n[x] 图像采集已中止，因为未指定要读取的目录或文件。")
	print(Fore.RED + "    请在键入的命令中补充 -p 参数并重试。")
	print(Style.RESET_ALL + "\a") 
	sys.exit(0)
else:
	pass

# 获取本机的 IP 地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

try:
	ipaddr = get_host_ip()
except:
	ipaddr = "（未知）"

# 从参数读取并决定用户设置文件
if args.get("conf", None) is None:
	jsonPath = "conf.json"
else:
	jsonPath = args["conf"]

with open(jsonPath, 'r', encoding='utf-8') as j:
	conf = json.load(j)

showVideo = conf["show_video"]
saveLog = conf["save_log"]
inputType = args["input"]

if inputType == "folder":
	inputFolder = args["path"]
	inputFiles = []
elif inputType == "files":
	inputFiles = args["path"]
	inputFolder = ""
elif inputType == "webcam" or inputType == "network":
	inputFiles = []
	inputFolder = ""

savePath = conf["output_folder"]
annotationType = conf["annotation_type"]
readFrames = conf["read_frames"]
captureType = conf["capture_type"]
captureImages = conf["capture_images"]
minMotionFrames = conf["min_motion_frames"]
minDeltaThresh = conf["min_delta_thresh"]
minArea = conf["min_area"]
jsonCreated = conf["json_created"]
jsonNotes = conf["json_notes"]
fileList = []

try:
	if inputType == "folder":
		fileList = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f)) and not f.startswith('.') and f.endswith(('.mp4','.avi','.mov','.mpeg','.flv','.wmv'))]
	elif inputType == "files":
		fileList.append(inputFiles)
	elif inputType == "webcam" or inputType == "network":
		fileList = [""]

except NameError:
	pass

# 确保 pythonw 静默模式可以在 Windows 上运行
if sys.executable.endswith("pythonw.exe"):
	sys.stdout = open(os.devnull, "w")
	sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")

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
（主程序 / 服务器端）


[i] 本程序将采集指定输入源中包含动态的图像。

    如果选择了网络视频流作为输入源，您需要：
     1. 按 y 运行本程序
     2. 在相应设备上运行 video-capturer 客户端：client.py
     3. 通过客户端连接到本机的 IP 地址：{}
""".format(ipaddr))

# 设置循环
i = 0

while i == 0:
	# 询问用户是否开始采集
	answer = input("    现在开始采集？[y/n]").lower()

	if answer == "y":
		gui = False
		i = 1
		vc.startCapture(fileList, jsonPath, showVideo, saveLog, inputType, inputFiles, inputFolder, savePath, annotationType, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i)

	elif answer == "n":
		print("\n\n[x] 您已取消采集。")
		print("\a")
		i = 1

	else:
		print("    请输入 y 开始采集，或输入 n 取消采集。")
		print("\a")
		i = 0
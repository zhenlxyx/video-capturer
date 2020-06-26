# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200626.2326

# 用法

'''
正常采集，加载 conf.json 配置文件，[采集单个文件]
python vccmd.py -i file -p example_01.mp4

正常采集，加载 conf.json 配置文件，[采集整个目录]
python vccmd.py -i folder -p input/

[静默采集]，加载 conf.json 配置文件，采集单个文件
pythonw vccmd.py -i file -p example_01.mp4

正常采集，[加载用户自定义的配置文件]，采集单个文件
python vccmd.py -c conf_2.json -i file -p example_01.mp4
'''

# 导入必要的包
import argparse								  # 命令行参数
import warnings								  # 系统警告信息
import sys									  # 将终端输出保存到日志
import json									  # 用户配置
import time									  # 时间操作
import os									  # 文件和文件夹操作
from os import listdir						  # 文件列表
from os.path import isfile, join			  # 文件操作
from colorama import init, Fore, Back, Style  # 在终端输出彩色文字
from xiangzhenlu import videocapture as vc	  # 采集视频中动态的图像

# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", 
	help="JSON 用户设置文件的路径")
ap.add_argument("-i", "--input", required=True,
	help="指定采集来源：目录或单个文件")
ap.add_argument("-p", "--path", required=True,
	help="待采集目录或单个文件的路径")
args = vars(ap.parse_args())

# 过滤警告并加载配置
warnings.filterwarnings("ignore")

init(convert=True)

if args.get("conf", None) is None:
	jsonPath = "conf.json"
else:
	jsonPath = args["conf"]

with open(jsonPath, 'r', encoding='utf-8') as j:
	conf = json.load(j)

showVideo = conf["show_video"]
saveAnnotations = conf["save_annotations"]
saveLog = conf["save_log"]
inputType = args["input"]

if inputType == "folder":
	inputFolder = args["path"]
	inputFiles = []
elif inputType == "files":
	inputFiles = args["path"]
	inputFolder = ""

savePath = conf["output_folder"]
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


[i] 这个程序将采集指定视频中包含动态的图像。
""")

# 设置循环
i = 0

while i == 0:
	# 询问用户是否开始采集
	answer = input("    现在开始采集？[y/n]").lower()

	if answer == "y":
		gui = False
		i = 1
		vc.startCapture(fileList, jsonPath, showVideo, saveAnnotations, saveLog, inputType, inputFiles, inputFolder, savePath, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i)

	elif answer == "n":
		print("\n\n[x] 您已取消采集。")
		print("\a")
		i = 1

	else:
		print("    请输入 y 开始采集，或输入 n 取消采集。")
		print("\a")
		i = 0
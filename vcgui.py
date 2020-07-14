# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200714.1200

# 用法

'''
运行 video-capturer 图形用户界面（GUI）版本
pythonw vcgui.py
'''

# 导入必要的包
import warnings								  # 系统警告信息
import datetime								  # 时间戳
import sys						    		  # 系统操作
import platform                               # 多操作系统支持
import json									  # 用户配置
import time									  # 时间操作
import os									  # 文件和文件夹操作
import socket								  # 网络操作
import tkinter as tk                          # 用户界面
import tkinter.ttk as ttk                     # 高级用户界面
from os import listdir						  # 文件列表
from os.path import isfile, join			  # 文件操作
from tkinter import *                         # 滚动条
from tkinter import messagebox                # 对话框
from tkinter.ttk import *                     # 进度条
from tkinter.filedialog import askdirectory, askopenfilenames, askopenfilename, asksaveasfilename
                                              # 打开和保存文件
from colorama import init, Fore, Back, Style  # 在终端输出彩色文字
from xiangzhenlu import videocapture as vc	  # 采集视频中动态的图像

# 初始化
i = 0
warnings.filterwarnings("ignore")
init(convert=True)
fileList = []
fileCount = len(fileList)

# 确保 pythonw 静默模式可以在 Windows 上运行
if sys.executable.endswith("pythonw.exe"):
	sys.stdout = open(os.devnull, "w")
	sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")

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

# 开始采集函数
def start():
    startBtn.configure(state="disabled")
    inputFolderRBtn.configure(state="disabled")
    inputFolderEnt.configure(state="disabled")
    inputFolderBtn.configure(state="disabled")
    inputFilesRBtn.configure(state="disabled")
    fileLb.configure(state="disabled")
    inputFilesBtn.configure(state="disabled")
    inputFilesClearBtn.configure(state="disabled")
    webcamRBtn.configure(state="disabled")
    networkRBtn.configure(state="disabled")
    openJsonRBtn.configure(state="disabled")
    openJsonEnt.configure(state="disabled")
    openJsonBtn.configure(state="disabled")
    newJsonRBtn.configure(state="disabled")
    newJsonEnt.configure(state="disabled")
    newJsonBtn.configure(state="disabled")
    modifyLnk.bind("<Button-1>", doNothing)
    modifyLnk.configure(foreground="grey")
    capture()

def capture():
    jsonPath = openJsonEnt2.get()

    with open(jsonPath, 'r', encoding='utf-8') as j:
        conf = json.load(j)

    showVideo = conf["show_video"]
    saveLog = conf["save_log"]
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

    inputType = inputVar.get()
    inputFolder = inputFolderEnt.get()
    inputFiles = fileLb2.get(0, "end")

    try:
        if inputType == "folder":
            fileList = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f)) and not f.startswith('.') and f.endswith(('.mp4','.avi','.mov','.mpeg','.flv','.wmv'))]
        elif inputType == "files":
            fileList = inputFiles
        elif inputType == "webcam" or inputType == "network":
            fileList = [""]

    except NameError:
        pass

    gui = True
    i = 1
    vc.startCapture(fileList, jsonPath, showVideo, saveLog, inputType, inputFiles, inputFolder, savePath, annotationType, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i)
    startBtn.configure(state="normal")
    inputFolderRBtn.configure(state="normal")
    inputFolderEnt.configure(state="normal")
    inputFolderBtn.configure(state="normal")
    inputFilesRBtn.configure(state="normal")
    fileLb.configure(state="normal")
    inputFilesBtn.configure(state="normal")
    inputFilesClearBtn.configure(state="normal")
    webcamRBtn.configure(state="normal")
    networkRBtn.configure(state="normal")
    openJsonRBtn.configure(state="normal")
    openJsonEnt.configure(state="normal")
    openJsonBtn.configure(state="normal")
    newJsonRBtn.configure(state="normal")
    newJsonEnt.configure(state="normal")
    newJsonBtn.configure(state="normal")
    modifyLnk.bind("<Button-1>", modifyJson)
    modifyLnk.configure(foreground="#0080ff")
    return

# 闲置函数
def doNothing(event):
    pass

# 添加输入文件夹函数
def addFolder():
    filePath = askdirectory()

    if not filePath:
        return

    inputFolderVar.set(filePath+"/")
    inputVar.set("folder")

    normalizer()

# 添加输出文件夹函数
def addOutputFolder():
    filePath = askdirectory()

    if not filePath:
        return

    outputFolderEnt.delete(0, "end")
    outputFolderEnt.insert("end", filePath+"/")

# 更新文件创建时间函数
def updateTime():
    currentTime = time.strftime("%Y-%m-%d %H:%M")
    jsonCreatedEnt.delete(0, "end")
    jsonCreatedEnt.insert("end", currentTime)

# 添加输入文件函数
def addFiles():
    filePath = askopenfilenames(filetypes=[('视频文件', ('.mp4','.avi','.mov','.mpeg','.flv','.wmv'))])

    if not filePath:
        return

    for p in filePath:
        if p not in fileList:
            fileList.append(p)
    
    fileCount = len(fileList)
    inputFilesVar.set("以下 {} 个视频：".format(fileCount))
    fileLb.delete(0, "end")
    fileLb2.delete(0, "end")

    for f in fileList:
        fileLb.insert("end", f.split("/")[-1])
        fileLb2.insert("end", f)

    inputVar.set("files")

    normalizer()

def selectAddFolder():
    inputVar.set("folder")
    if inputFolderEnt.get() != "" and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    else:
        startBtn.configure(state="disabled")

def selectAddFiles():
    inputVar.set("files")
    if len(fileLb.get("0", "end")) == 0:
        startBtn.configure(state="disabled")
    elif len(fileLb.get("0", "end")) != 0 and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")

def selectWebcam():
    inputVar.set("webcam")
    if jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    else:
        startBtn.configure(state="disabled")

def selectNetwork():
    inputVar.set("network")
    if jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    else:
        startBtn.configure(state="disabled")

def selectOpenJson():
    jsonVar.set("open")
    if inputVar.get() == "folder" and inputFolderEnt.get() != "" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "files" and len(fileLb.get("0", "end")) != 0 and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "webcam" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "network" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")

def selectNewJson():
    jsonVar.set("new")
    startBtn.configure(state="disabled")

def clearFiles():
    fileLb.delete(0, "end")
    fileLb2.delete(0, "end")
    del fileList[:]
    inputFilesVar.set("以下 {} 个视频：".format(fileCount))
    inputVar.set("files")
    startBtn.configure(state="disabled")

# 打开设置文件函数
def addJson():
    jsonPath = askopenfilename(filetypes=[('JSON 设置文件', ('.json'))])

    if not jsonPath:
        return
    
    openJson(jsonPath)

# 新建设置文件函数
def newJson():
    currentTime = time.strftime("%Y-%m-%d %H:%M")

    if newJsonEnt.get() == "为设置文件命名，例如 my_conf.json":
        return
    elif newJsonEnt.get()[-5:] != ".json":
        jsonNameError()
        return
    else:
        jsonPath = newJsonEnt.get()
    
    jsonDict = {
        "show_video": True,
        "save_log": False,
        "output_folder": "output/",
        "annotation_type": "pascalvoc",
        "read_frames": 5,
        "capture_type": "avg",
        "capture_images": ["all", 2, 0],
        "min_motion_frames": 1,
        "min_delta_thresh": 5,
        "min_area": 1500,
        "json_created": currentTime,
        "json_notes": "在此输入本设置文件的注释"
    }

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(jsonDict, f, ensure_ascii=False, indent=4)

    openJson(jsonPath)

# 修改设置文件函数
def modifyJson(event):
    modifyLnk.place_forget()
    paraFrm.place(relx=0.04, rely=0.464, relheight=0.513
            , relwidth=0.931, bordermode='ignore')
    paraFrm2.place_forget()
    saveLnk.place(relx=0.16, rely=0.384, height=26, width=307
                , bordermode='ignore')
    startBtn.configure(state="disabled")

# 保存设置文件函数
def saveJson(event):
    jsonPath = openJsonEnt2.get()
    savePath = outputFolderEnt.get()
    readFrames = readFramesSb.get()
    minMotionFrames = minMotionFramesSb.get()
    minDeltaThresh = minDeltaThreshSb.get()
    minArea = minAreaSb.get()
    jsonCreated = jsonCreatedEnt.get()
    jsonNotes = jsonNotesTxt.get(1.0, "end-1c")

    if showVideoVar.get() == "是":
        showVideo = True
    else:
        showVideo = False

    if saveLogVar.get() == "是":
        saveLog = True
    else:
        saveLog = False

    if annotationTypeVar.get() == "PascalVOC":
        annotationType = "pascalvoc"
    elif annotationTypeVar.get() == "YOLO":
        annotationType = "yolo"

    if captureTypeVar.get() == "多帧加权平均法":
        captureType = "avg"
    elif captureTypeVar.get() == "二帧差分法":
        captureType = "two"
    else:
        captureType = "three"

    if captureImagesPara1Var.get() == "应采尽采":
        captureImagesPara1 = "all"
        captureImagesPara2 = captureImagesPara2Sb_all.get()
        captureImagesPara3 = 0
    elif captureImagesPara1Var.get() == "按帧采集":
        captureImagesPara1 = "frame"
        captureImagesPara2 = captureImagesPara2Sb_frame.get()
        captureImagesPara3 = 0
    elif captureImagesPara1Var.get() == "按秒采集":
        captureImagesPara1 = "second"
        captureImagesPara2 = captureImagesPara2Sb_second.get()
        captureImagesPara3 = captureImagesPara3Sb.get()

    jsonDict = {
        "show_video": showVideo,
        "save_log": saveLog,
        "output_folder": savePath,
        "annotation_type": annotationType,
        "read_frames": int(readFrames),
        "capture_type": captureType,
        "capture_images": [captureImagesPara1, int(captureImagesPara2), int(captureImagesPara3)],
        "min_motion_frames": int(minMotionFrames),
        "min_delta_thresh": int(minDeltaThresh),
        "min_area": int(minArea),
        "json_created": jsonCreated,
        "json_notes": jsonNotes
    }

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(jsonDict, f, ensure_ascii=False, indent=4)

    jsonVar.set("open")

    openJson(jsonPath)

    saveLnk.place_forget()
    paraFrm.place_forget()
    paraFrm2.place(relx=0.04, rely=0.464, relheight=0.513
            , relwidth=0.931, bordermode='ignore')

def openJson(jsonPath):
    try:
        with open(jsonPath, 'r', encoding='utf-8') as j:
            conf = json.load(j)

        showVideo = conf["show_video"]
        saveLog = conf["save_log"]

        savePath = conf["output_folder"]
        if type(savePath) != str:
            savePathError()
            return

        annotationType = conf["annotation_type"]

        readFrames = conf["read_frames"]
        if type(readFrames) != int:
            readFramesError()
            return

        captureType = conf["capture_type"]
        captureImages = conf["capture_images"]

        minMotionFrames = conf["min_motion_frames"]
        if type(minMotionFrames) != int:
            minMotionFramesError()
            return

        minDeltaThresh = conf["min_delta_thresh"]
        if type(minDeltaThresh) != int:
            minDeltaThreshError()
            return

        minArea = conf["min_area"]
        if type(minArea) != int:
            minAreaError()
            return

        jsonCreated = conf["json_created"]
        if type(jsonCreated) != str:
            jsonError()
            return

        jsonNotes = conf["json_notes"]
        if type(jsonNotes) != str:
            jsonError()
            return

        if type(showVideo) != bool:
            captureOptionsError()
            return
        if showVideo:
            showVideo1 = "是"
        elif not showVideo:
            showVideo1 = "否"

        if type(saveLog) != bool:
            captureOptionsError()
            return
        if saveLog:
            saveLog1 = "是"
        elif not saveLog:
            saveLog1 = "否"

        if annotationType == "pascalvoc":
            annotationType1 = "PascalVOC"
        elif annotationType == "yolo":
            annotationType1 = "YOLO"
        else:
            annotationTypeError()

        if captureType == "avg":
            captureType1 = "多帧加权平均法"
        elif captureType == "two":
            captureType1 = "二帧差分法"
        elif captureType == "three":
            captureType1 = "三帧差分法"
        else:
            captureTypeError()
            return

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
            captureImagesPara3 = "，\n　　　　　　　　　每 {} 帧取一帧保存".format(captureImages[2])
        else:
            captureImagesError()
            return

        captureImages1 = "{}{}{}".format(captureImagesPara1, captureImagesPara2, captureImagesPara3)

        paraFrm2.place(relx=0.04, rely=0.464, relheight=0.513, relwidth=0.931
                , bordermode='ignore')
        modifyLnk.place(relx=0.16, rely=0.384, height=26, width=307
                , bordermode='ignore')
        paraLbl.place(relx=0.027, rely=0.384, height=26, width=357
                , bordermode='ignore')

        openJsonEnt2.delete(0, "end")
        openJsonVar.set(jsonPath.split("/")[-1])
        openJsonEnt2.insert("end", jsonPath)

        showVideoVar.set(showVideo1)
        showVideoMenu = tk.OptionMenu(innerFrm, showVideoVar, *showVideoOptions)
        showVideoMenu.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        saveLogVar.set(saveLog1)
        saveLogMenu = tk.OptionMenu(innerFrm, saveLogVar, *saveLogOptions)
        saveLogMenu.grid(row=1, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        outputFolderEnt.delete(0, "end")
        outputFolderEnt.insert("end", savePath)
        outputFolderEnt.grid(row=2, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        annotationTypeVar.set(annotationType1)
        annotationTypeMenu = tk.OptionMenu(innerFrm, annotationTypeVar, *annotationTypeOptions)
        annotationTypeMenu.grid(row=3, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        captureTypeVar.set(captureType1)
        captureTypeMenu = tk.OptionMenu(innerFrm, captureTypeVar, *captureTypeOptions)
        captureTypeMenu.grid(row=5, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        captureImagesPara1Var.set(captureImagesPara1)
        captureImagesPara1Menu = tk.OptionMenu(innerFrm, captureImagesPara1Var, *captureImagesPara1Options)
        captureImagesPara1Menu.grid(row=6, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        readFramesSb.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        readFramesSb.delete(0,"end")
        readFramesSb.insert(0,readFrames)

        captureImagesPara2Sb_all.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Sb_all.delete(0,"end")
        captureImagesPara2Sb_all.insert(0,captureImages[1])

        captureImagesPara2Sb_frame.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Sb_frame.delete(0,"end")
        captureImagesPara2Sb_frame.insert(0,captureImages[1])

        captureImagesPara2Sb_second.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Sb_second.delete(0,"end")
        captureImagesPara2Sb_second.insert(0,captureImages[1])

        captureImagesPara3Sb.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara3Sb.delete(0,"end")
        captureImagesPara3Sb.insert(0,captureImages[2])

        minMotionFramesSb.grid(row=9, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        minMotionFramesSb.delete(0,"end")
        minMotionFramesSb.insert(0,minMotionFrames)

        minDeltaThreshSb.grid(row=10, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        minDeltaThreshSb.delete(0,"end")
        minDeltaThreshSb.insert(0,minDeltaThresh)

        minAreaSb.grid(row=11, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        minAreaSb.delete(0,"end")
        minAreaSb.insert(0,minArea)

        jsonCreatedEnt.delete(0, "end")
        jsonCreatedEnt.insert("end", jsonCreated)
        jsonCreatedEnt.grid(row=12, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        jsonNotesTxt.delete("1.0", "end-1c")
        jsonNotesTxt.insert("end", jsonNotes)
        jsonNotesTxt.grid(row=13, columnspan=3, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        paraTxt.configure(state="normal")
        paraTxt.delete("1.0", "end")
        paraTxt.insert(
            "end", 
            '''显示采集窗口：　　{}
保存采集日志：　　{}
输出目录：　　　　{}
图像标注：　　　　{}
视频读法：　　　　每 {} 帧取一帧读
采集算法：　　　　{}
采集方式：　　　　{}
运动帧最小值：　　{}
阈值增量最小值：　{}
轮廓区域最小值：　{}
创建时间：　　　　{}
备注：　　　　　　{}'''
            .format(showVideo1, saveLog1, savePath, annotationType1, readFrames, captureType1, captureImages1, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes)
            )
        paraTxt.configure(state="disabled")

        jsonVar.set("open")

        if currentHour >= 19 or currentHour <= 7:
            showVideoMenu.configure(background="#383838", activebackground="#606060", foreground="#C0C0C0", activeforeground="#C0C0C0", highlightcolor="#606060", borderwidth=0, relief="flat")
            showVideoMenu["menu"].configure(background="#383838", foreground="#C0C0C0")
            saveLogMenu.configure(background="#383838", activebackground="#606060", foreground="#C0C0C0", activeforeground="#C0C0C0", borderwidth=0, relief="flat")
            saveLogMenu["menu"].configure(background="#383838", foreground="#C0C0C0")
            outputFolderEnt.configure(background="#000000", highlightbackground="#ffffff", disabledbackground="#383838", foreground="#ffffff", highlightthickness=1, relief="flat")
            annotationTypeMenu.configure(background="#383838", activebackground="#606060", foreground="#C0C0C0", activeforeground="#C0C0C0", borderwidth=0, relief="flat")
            annotationTypeMenu["menu"].configure(background="#383838", foreground="#C0C0C0")
            readFramesSb.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            captureTypeMenu.configure(background="#383838", activebackground="#606060", foreground="#C0C0C0", activeforeground="#C0C0C0", borderwidth=0, relief="flat")                                 
            captureTypeMenu["menu"].configure(background="#383838", foreground="#C0C0C0")
            captureImagesPara1Menu.configure(background="#383838", activebackground="#606060", foreground="#C0C0C0", activeforeground="#C0C0C0", borderwidth=0, relief="flat")
            captureImagesPara1Menu["menu"].configure(background="#383838", foreground="#C0C0C0")
            captureImagesPara2Sb_all.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            captureImagesPara2Sb_frame.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            captureImagesPara2Sb_second.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            captureImagesPara3Sb.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            minMotionFramesSb.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            minDeltaThreshSb.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            minAreaSb.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff")
            jsonCreatedEnt.configure(background="#000000", highlightbackground="#ffffff", disabledbackground="#383838", foreground="#ffffff", highlightthickness=1, relief="flat")

        else:
            showVideoMenu.configure(background="#ffffff", activebackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", highlightcolor="#E4E4E4", borderwidth=0, relief="flat")
            showVideoMenu["menu"].configure(background="#ffffff", foreground="#1F1C19")
            saveLogMenu.configure(background="#ffffff", activebackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
            saveLogMenu["menu"].configure(background="#ffffff", foreground="#1F1C19")
            outputFolderEnt.configure(background="#ffffff", highlightbackground="#1F1C19", foreground="#1F1C19", highlightthickness=1, relief="flat")
            annotationTypeMenu.configure(background="#ffffff", activebackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
            annotationTypeMenu["menu"].configure(background="#ffffff", foreground="#1F1C19")
            readFramesSb.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            captureTypeMenu.configure(background="#ffffff", activebackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")                                 
            captureTypeMenu["menu"].configure(background="#ffffff", foreground="#1F1C19")
            captureImagesPara1Menu.configure(background="#ffffff", activebackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
            captureImagesPara1Menu["menu"].configure(background="#ffffff", foreground="#1F1C19")
            captureImagesPara2Sb_all.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            captureImagesPara2Sb_frame.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            captureImagesPara2Sb_second.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            captureImagesPara3Sb.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            minMotionFramesSb.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            minDeltaThreshSb.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            minAreaSb.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19")
            jsonCreatedEnt.configure(background="#ffffff", highlightbackground="#1F1C19", foreground="#1F1C19", highlightthickness=1, relief="flat")

        normalizer()

    except json.decoder.JSONDecodeError:
        jsonError()
        return

# 各类错误函数
def jsonError():
    messagebox.showerror(title='JSON 设置文件错误', message='无法读取您的设置文件中的内容。\n请检查文件格式和参数是否正确。\n\n如果此问题持续，请新建一个设置文件。')

def jsonNameError():
    messagebox.showerror(title='JSON 设置文件命名错误', message='新建设置文件的名称须以 .json 结尾。\n请检查文件命名是否正确。')

def captureOptionsError():
    messagebox.showerror(title='图像采集设置错误', message='无法读取您的设置文件中的内容。\n请检查 show_video、show_detail、save_annotations、save_log 四项参数是否正确，它们应该为 True（是）或 False（否）。\n\n如果此问题持续，请新建一个设置文件。')

def savePathError():
    messagebox.showerror(title='“采集图像保存目录”设置错误', message='无法读取“采集图像保存目录”的设置项。\n请检查 output_folder 参数是否正确，它应该是一个路径。\n\n如果此问题持续，请新建一个设置文件。')

def annotationTypeError():
    messagebox.showerror(title='“图像标注”设置错误', message='无法读取“图像标注”的设置项。\n请检查 annotation_type 参数是否正确。\n标注类型：pascalvoc，yolo。\n\n如果此问题持续，请新建一个设置文件。')

def readFramesError():
    messagebox.showerror(title='“视频读法”设置错误', message='无法读取“视频读法”的设置项。\n请检查 read_frames 参数是否正确，它应该是一个整数。\n\n如果此问题持续，请新建一个设置文件。')

def captureTypeError():
    messagebox.showerror(title='“采集算法”设置错误', message='无法读取“采集算法”的设置项。\n请检查 capture_type 参数是否正确。\n采集算法：avg（多帧加权平均法），two（二帧差分法），three（三帧差分法）。\n\n如果此问题持续，请新建一个设置文件。')

def captureImagesError():
    messagebox.showerror(title='“采集方式”设置错误', message='无法读取“采集方式”的设置项。\n请检查 capture_images 参数是否正确。\n参数格式：[\'采集方式\', 采集数值 1, 采集数值 2]。\n采集方式：all（应采尽采），frame（按帧采集），second（按秒采集）。\n\n如果此问题持续，请新建一个设置文件。')

def minMotionFramesError():
    messagebox.showerror(title='“运动帧最小值”设置错误', message='无法读取“运动帧最小值”的设置项。\n请检查 min_motion_frames 参数是否正确，它应该是一个整数。\n\n如果此问题持续，请新建一个设置文件。')

def minDeltaThreshError():
    messagebox.showerror(title='“阈值增量最小值”设置错误', message='无法读取“阈值增量最小值”的设置项。\n请检查 min_delta_thresh 参数是否正确，它应该是一个整数。\n\n如果此问题持续，请新建一个设置文件。')

def minAreaError():
    messagebox.showerror(title='“轮廓区域最小值”设置错误', message='无法读取“轮廓区域最小值”的设置项。\n请检查 min_area 参数是否正确，它应该是一个整数。\n\n如果此问题持续，请新建一个设置文件。')

# 显示采集窗口函数
def changeShowVideo(*args):
    showVideoVar.get()

# 保存图像中的标注函数
def changeAnnotationType(*args):
    annotationTypeVar.get()

# 保存采集日志函数
def changeSaveLog(*args):
    saveLogVar.get()

# 修改视频读法函数
def changeReadFrames(*args):
    readFramesVar.get()

# 修改采集算法函数
def changeCaptureType(*args):
    captureTypeVar.get()

# 修改采集方式函数
def changeCaptureImagesPara1(*args):
    captureImagesPara1Var.get()
    if captureImagesPara1Var.get() == "应采尽采":
        captureImagesPara2Frm_all.grid(row=7, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Frm_frame.grid_forget()
        captureImagesPara2Frm_second.grid_forget()
        captureImagesPara3Frm.grid_forget()
    elif captureImagesPara1Var.get() == "按帧采集":
        captureImagesPara2Frm_frame.grid(row=7, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Frm_all.grid_forget()
        captureImagesPara2Frm_second.grid_forget()
        captureImagesPara3Frm.grid_forget()
    else:
        captureImagesPara2Frm_second.grid(row=7, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara3Frm.grid(row=8, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
        captureImagesPara2Frm_all.grid_forget()
        captureImagesPara2Frm_frame.grid_forget()

# 决定各界面控件的启用和禁用的一般原则
def normalizer():
    if inputVar.get() == "folder" and inputFolderEnt.get() != "" and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "files" and len(fileLb.get("0", "end")) != 0 and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "webcam" and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "network" and jsonVar.get() == "open" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    else:
        startBtn.configure(state="disabled")

# 参数文本框滚动事件函数
def scrollEvent(event):
    paraCvs.configure(scrollregion=paraCvs.bbox("all"),width=400,height=200)
    paraCvs2.configure(scrollregion=paraCvs2.bbox("all"),width=400,height=200)

# 新建设置文件文本框占位符清空函数
def clearContent(event):
    newJsonEnt.delete(0, "end")
    jsonVar.set("new")

window = tk.Tk()

# 设置主题样式
currentHour = datetime.datetime.now().hour

if currentHour >= 19 or currentHour <= 7:
    window.configure(background="#383838")
    
else:
    window.configure(background="#ffffff")

# 窗口设置
window.geometry("800x530+320+50")
window.minsize(120, 1)
window.maxsize(3364, 1061)
window.resizable(0, 0)
window.title("视频图像采集器（主程序 / 服务器端）")
window.iconphoto(True, tk.PhotoImage(file='./xiangzhenlu/app_icon.png'))

# 采集来源标签框架
sourceLf = tk.LabelFrame(window)
sourceLf.place(relx=0.025, rely=0.026, relheight=0.821
        , relwidth=0.469)
sourceLf.configure(text='''采集来源：''')

# 输入文件夹单选框
inputVar = StringVar(window)
inputVar.set("folder")
inputFolderRBtn = tk.Radiobutton(sourceLf)
inputFolderRBtn.place(relx=0.027, rely=0.062, relheight=0.069
        , relwidth=0.925, bordermode='ignore')
inputFolderRBtn.configure(text='''以下文件夹中的全部视频：''')
inputFolderRBtn.configure(value="folder")
inputFolderRBtn.configure(variable=inputVar)
inputFolderRBtn.configure(command=selectAddFolder)

# 输入文件夹文本框
inputFolderVar = tk.StringVar()
inputFolderEnt = tk.Entry(sourceLf)
inputFolderEnt.place(relx=0.107, rely=0.14, height=27
        , relwidth=0.677, bordermode='ignore')
inputFolderEnt.configure(textvariable=inputFolderVar)
inputFolderEnt.configure(state="readonly")

# 输入文件夹选择按钮
inputFolderBtn = tk.Button(sourceLf)
inputFolderBtn.place(relx=0.789, rely=0.14, height=28, width=65
        , bordermode='ignore')
inputFolderBtn.configure(text='''选择''')
inputFolderBtn.configure(command=addFolder)

# 输入文件单选框
inputFilesVar = tk.StringVar()
inputFilesVar.set("以下 {} 个视频：".format(fileCount))
inputFilesRBtn = tk.Radiobutton(sourceLf)
inputFilesRBtn.place(relx=0.027, rely=0.223, relheight=0.069
        , relwidth=0.925, bordermode='ignore')
inputFilesRBtn.configure(value="files")
inputFilesRBtn.configure(variable=inputVar)
inputFilesRBtn.configure(textvariable=inputFilesVar)
inputFilesRBtn.configure(command=selectAddFiles)

# 输入文件列表框
fileLb = Listbox(sourceLf)
fileLb.place(relx=0.107, rely=0.303, relheight=0.384, relwidth=0.669
        , bordermode='ignore')
fileLb.configure(relief="flat")
scrollBar = Scrollbar(fileLb)
scrollBar.pack(side="right", fill="y")
scrollBar.config(command=fileLb.yview)
fileLb.config(yscrollcommand=scrollBar.set)
fileLb.delete(0, "end")

fileLb2 = Listbox(sourceLf)
fileLb2.delete(0, "end")

# 输入文件选择按钮
inputFilesBtn = tk.Button(sourceLf)
inputFilesBtn.place(relx=0.789, rely=0.303, height=28, width=65
        , bordermode='ignore')
inputFilesBtn.configure(text='''选择''')
inputFilesBtn.configure(command=addFiles)

# 清除输入文件选择按钮
inputFilesClearBtn = tk.Button(sourceLf)
inputFilesClearBtn.place(relx=0.789, rely=0.383, height=28, width=65
        , bordermode='ignore')
inputFilesClearBtn.configure(text='''清空''')
inputFilesClearBtn.configure(command=clearFiles)

webcamRBtn = tk.Radiobutton(sourceLf)
webcamRBtn.place(relx=0.027, rely=0.708, relheight=0.069
        , relwidth=0.925, bordermode='ignore')
webcamRBtn.configure(text='''本机摄像头''')
webcamRBtn.configure(value="webcam")
webcamRBtn.configure(variable=inputVar)
webcamRBtn.configure(command=selectWebcam)

networkRBtn = tk.Radiobutton(sourceLf)
networkRBtn.place(relx=0.027, rely=0.789, relheight=0.069
        , relwidth=0.925, bordermode='ignore')
networkRBtn.configure(text='''网络视频流''')
networkRBtn.configure(value="network")
networkRBtn.configure(variable=inputVar)
networkRBtn.configure(command=selectNetwork)

networkMsg = tk.Message(sourceLf)
networkMsg.place(relx=0.053, rely=0.871, relheight=0.108
        , relwidth=0.925, bordermode='ignore')
networkMsg.configure(width=347)
networkMsg.configure(text='''您需要：
  1. 在相应设备上运行 video-capturer 客户端：client.py
  2. 通过客户端连接到本机的 IP 地址：{}'''.format(ipaddr))

# 采集选项标签框架
configLf = tk.LabelFrame(window)
configLf.place(relx=0.506, rely=0.026, relheight=0.821
        , relwidth=0.47)
configLf.configure(text='''采集选项：''')

# 打开设置文件单选框
jsonVar = StringVar(window)
jsonVar.set("open")
openJsonRBtn = tk.Radiobutton(configLf)
openJsonRBtn.place(relx=0.027, rely=0.062, relheight=0.069
        , relwidth=0.926, bordermode='ignore')
openJsonRBtn.configure(text='''使用以下设置文件：''')
openJsonRBtn.configure(value="open")
openJsonRBtn.configure(variable=jsonVar)
openJsonRBtn.configure(command=selectOpenJson)

# 打开设置文件文本框
openJsonVar = tk.StringVar()
openJsonEnt = tk.Entry(configLf)
openJsonEnt.place(relx=0.106, rely=0.14, height=27, relwidth=0.676
        , bordermode='ignore')
openJsonEnt.configure(background="white")
openJsonEnt.configure(textvariable=openJsonVar)
openJsonEnt.configure(state="readonly")

openJsonEnt2 = tk.Entry(configLf)
openJsonEnt2.configure(background="white")

# 打开设置文件选择按钮
openJsonBtn = tk.Button(configLf)
openJsonBtn.place(relx=0.79, rely=0.14, height=28, width=65
        , bordermode='ignore')
openJsonBtn.configure(text='''选择''')
openJsonBtn.configure(command=addJson)

# 新建设置文件单选框
newJsonRBtn = tk.Radiobutton(configLf)
newJsonRBtn.place(relx=0.027, rely=0.223, relheight=0.069
        , relwidth=0.926, bordermode='ignore')
newJsonRBtn.configure(text='''新建设置文件（.json）：''')
newJsonRBtn.configure(value="new")
newJsonRBtn.configure(variable=jsonVar)
newJsonRBtn.configure(command=selectNewJson)

# 新建设置文件文本框
newJsonEnt = tk.Entry(configLf)
newJsonEnt.place(relx=0.106, rely=0.303, height=27, relwidth=0.676
        , bordermode='ignore')
newJsonEnt.insert("end", "为设置文件命名，例如 my_conf.json")
newJsonEnt.bind('<Button-1>', clearContent)

# 新建设置文件选择按钮
newJsonBtn = tk.Button(configLf)
newJsonBtn.place(relx=0.79, rely=0.303, height=28, width=65
        , bordermode='ignore')
newJsonBtn.configure(text='''新建''')
newJsonBtn.configure(command=newJson)

# 参数标签
paraLbl = tk.Label(configLf)
paraLbl.configure(text='''参数：''')

# 修改参数链接
modifyLnk = tk.Label(configLf)
modifyLnk.configure(text='''修改''')
modifyLnk.configure(cursor="hand2")
modifyLnk.bind('<Button-1>', modifyJson)

# 保存参数链接
saveLnk = tk.Label(configLf)
saveLnk.configure(text='''保存修改''')
saveLnk.configure(cursor="hand2")
saveLnk.bind('<Button-1>', saveJson)

# 修改参数框架
paraFrm = tk.Frame(configLf)
paraCvs = tk.Canvas(paraFrm)
paraCvs.configure(borderwidth="0")
paraCvs.configure(relief="flat")
paraCvs.configure(highlightthickness="0")

innerFrm = tk.Frame(paraCvs)
innerFrm.configure(width="400")

scrollBar2=tk.Scrollbar(paraFrm,orient="vertical",command=paraCvs.yview)
paraCvs.configure(yscrollcommand=scrollBar2.set)

scrollBar2.pack(side="right",fill="y")
paraCvs.pack(side="left",fill="both")
paraCvs.create_window((0,0),window=innerFrm,anchor='nw')
innerFrm.bind("<Configure>", scrollEvent)

# 浏览参数框架
paraFrm2 = tk.Frame(configLf)
paraCvs2 = tk.Canvas(paraFrm2)
paraCvs2.configure(borderwidth="0")
paraCvs2.configure(relief="flat")
paraCvs2.configure(highlightthickness="0")

paraTxt = tk.Text(paraCvs2)
paraTxt.configure(width="44")
paraTxt.configure(height="15")
paraTxt.configure(borderwidth="0")
paraTxt.configure(relief="flat")
paraTxt.configure(font="TkTextFont")
paraTxt.configure(wrap="word")
paraTxt.configure(spacing1="3")
paraTxt.configure(spacing2="4")
paraTxt.configure(spacing3="5")

scrollBar3=tk.Scrollbar(paraFrm2,orient="vertical",command=paraCvs2.yview)
paraCvs2.configure(yscrollcommand=scrollBar3.set)

scrollBar3.pack(side="right",fill="y")
paraCvs2.pack(side="left",fill="both")
paraCvs2.create_window((0,0),window=paraTxt,anchor='nw')
paraTxt.bind("<Configure>", scrollEvent)

# 参数标签和控件
showVideoLbl = tk.Label(innerFrm)
showVideoLbl.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

showVideoLbl.configure(text='''显示采集窗口：''')

showVideoVar = StringVar(window)
showVideoOptions = ["是", "否"]
showVideoVar.trace('w', changeShowVideo)

saveLogLbl = tk.Label(innerFrm)
saveLogLbl.grid(row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
saveLogLbl.configure(text='''保存采集日志：''')

saveLogVar = StringVar(window)
saveLogOptions = ["是", "否"]
saveLogVar.trace('w', changeSaveLog)

outputFolderLbl = tk.Label(innerFrm)
outputFolderLbl.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
outputFolderLbl.configure(text='''输出目录：''')

outputFolderEnt = tk.Entry(innerFrm)

outputFolderBtn = tk.Button(innerFrm)
outputFolderBtn.grid(row=2, column=3, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
outputFolderBtn.configure(text='''选择''')
outputFolderBtn.configure(command=addOutputFolder)

annotationTypeLbl = tk.Label(innerFrm)
annotationTypeLbl.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
annotationTypeLbl.configure(text='''图像标注：''')

annotationTypeVar = StringVar(window)
annotationTypeOptions = ["PascalVOC", "YOLO"]
annotationTypeVar.trace('w', changeAnnotationType)

readFramesLbl = tk.Label(innerFrm)
readFramesLbl.grid(row=4, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl.configure(text='''视频读法：''')

readFramesInnerFrm = tk.Frame(innerFrm)
readFramesInnerFrm.grid(row=4, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesInnerFrm.configure(width="400")

readFramesLbl_1 = tk.Label(readFramesInnerFrm)
readFramesLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl_1.configure(text='''每 ''')

readFramesSb = tk.Spinbox(readFramesInnerFrm, from_=1.0, to=1000.0)
readFramesSb.configure(width="4")

readFramesLbl_2 = tk.Label(readFramesInnerFrm)
readFramesLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl_2.configure(text=''' 帧取一帧读''')

captureTypeLbl = tk.Label(innerFrm)
captureTypeLbl.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureTypeLbl.configure(text='''采集算法：''')

captureTypeVar = StringVar(window)
captureTypeOptions = ["多帧加权平均法", "二帧差分法", "三帧差分法"]
captureTypeVar.trace('w', changeCaptureType)

captureImagesLbl = tk.Label(innerFrm)
captureImagesLbl.grid(row=6, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesLbl.configure(text='''采集方式：''')

captureImagesPara1Var = StringVar(window)
captureImagesPara1Options = ["应采尽采", "按帧采集", "按秒采集"]
captureImagesPara1Var.trace('w', changeCaptureImagesPara1)

captureImagesPara2Frm_all = tk.Frame(innerFrm)
captureImagesPara2Frm_all.configure(width="400")

captureImagesPara2Frm_allLbl_1 = tk.Label(captureImagesPara2Frm_all)
captureImagesPara2Frm_allLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_allLbl_1.configure(text='''每 ''')

captureImagesPara2Sb_all = tk.Spinbox(captureImagesPara2Frm_all, from_=1.0, to=1000.0)
captureImagesPara2Sb_all.configure(width="4")

captureImagesPara2Frm_allLbl_2 = tk.Label(captureImagesPara2Frm_all)
captureImagesPara2Frm_allLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_allLbl_2.configure(text=''' 帧取一帧保存''')

captureImagesPara2Frm_frame = tk.Frame(innerFrm)
captureImagesPara2Frm_frame.configure(width="400")

captureImagesPara2Frm_frameLbl_1 = tk.Label(captureImagesPara2Frm_frame)
captureImagesPara2Frm_frameLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_frameLbl_1.configure(text='''采集 ''')

captureImagesPara2Sb_frame = tk.Spinbox(captureImagesPara2Frm_frame, from_=1.0, to=1000.0)
captureImagesPara2Sb_frame.configure(width="4")

captureImagesPara2Frm_frameLbl_2 = tk.Label(captureImagesPara2Frm_frame)
captureImagesPara2Frm_frameLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_frameLbl_2.configure(text='''帧''')

captureImagesPara2Frm_second = tk.Frame(innerFrm)
captureImagesPara2Frm_second.configure(width="400")

captureImagesPara2Frm_secondLbl_1 = tk.Label(captureImagesPara2Frm_second)
captureImagesPara2Frm_secondLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_secondLbl_1.configure(text='''采集''')

captureImagesPara2Sb_second = tk.Spinbox(captureImagesPara2Frm_second, from_=1.0, to=1000.0)
captureImagesPara2Sb_second.configure(width="4")

captureImagesPara2Frm_secondLbl_2 = tk.Label(captureImagesPara2Frm_second)
captureImagesPara2Frm_secondLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_secondLbl_2.configure(text=''' 秒''')

captureImagesPara3Frm = tk.Frame(innerFrm)
captureImagesPara3Frm.configure(width="400")

captureImagesPara3FrmLbl_1 = tk.Label(captureImagesPara3Frm)
captureImagesPara3FrmLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara3FrmLbl_1.configure(text='''每 ''')

captureImagesPara3Sb = tk.Spinbox(captureImagesPara3Frm, from_=1.0, to=1000.0)
captureImagesPara3Sb.configure(width="4")

captureImagesPara3FrmLbl_2 = tk.Label(captureImagesPara3Frm)
captureImagesPara3FrmLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara3FrmLbl_2.configure(text=''' 帧取一帧保存''')

minMotionFramesLbl = tk.Label(innerFrm)
minMotionFramesLbl.grid(row=9, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minMotionFramesLbl.configure(text='''运动帧最小值：''')

minMotionFramesSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minMotionFramesSb.configure(width="4")

minDeltaThreshLbl = tk.Label(innerFrm)
minDeltaThreshLbl.grid(row=10, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minDeltaThreshLbl.configure(text='''阈值增量最小值：''')

minDeltaThreshSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minDeltaThreshSb.configure(width="4")

minAreaLbl = tk.Label(innerFrm)
minAreaLbl.grid(row=11, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minAreaLbl.configure(text='''轮廓区域最小值：''')

minAreaSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minAreaSb.configure(width="4")

jsonCreatedLbl = tk.Label(innerFrm)
jsonCreatedLbl.grid(row=12, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonCreatedLbl.configure(text='''创建时间：''')

jsonCreatedEnt = tk.Entry(innerFrm)

jsonCreatedBtn = tk.Button(innerFrm)
jsonCreatedBtn.grid(row=12, column=3, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonCreatedBtn.configure(text='''更新''')
jsonCreatedBtn.configure(command=updateTime)

jsonNotesLbl = tk.Label(innerFrm)
jsonNotesLbl.grid(row=13, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonNotesLbl.configure(text='''备注：''')

jsonNotesTxt = Text(innerFrm)
jsonNotesTxt.configure(width="27")
jsonNotesTxt.configure(height="2")
jsonNotesTxt.configure(borderwidth="1")
jsonNotesTxt.configure(font="TkTextFont")
jsonNotesTxt.configure(highlightthickness="1")

jsonNotesTxt.configure(relief="flat")
jsonNotesTxt.configure(wrap="word")
jsonNotesTxt.configure(spacing1="1")
jsonNotesTxt.configure(spacing2="1")
jsonNotesTxt.configure(spacing3="1")
    
# 开始采集按钮
startBtn = tk.Button(window)
startBtn.place(relx=0.413, rely=0.887, height=38, width=139)
startBtn.configure(text='''▶  开始采集''')
startBtn.configure(command=start)
startBtn.configure(state="disabled")

# 根据时间切换深色 / 浅色模式
if currentHour >= 19 or currentHour <= 7:
    sourceLf.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    inputFolderRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    inputFolderEnt.configure(background="#383838", readonlybackground="#383838", disabledbackground="#383838", highlightbackground="#ffffff", foreground="#ffffff", highlightthickness=1, relief="flat")
    inputFolderBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    inputFilesRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    fileLb.configure(background="#383838", foreground="#ffffff")
    inputFilesBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    inputFilesClearBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    webcamRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    networkRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    networkMsg.configure(background="#383838", foreground="#ffffff")
    configLf.configure(background="#383838", foreground="#ffffff", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    openJsonRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    openJsonEnt.configure(background="#383838", readonlybackground="#383838", disabledbackground="#383838", highlightbackground="#ffffff", foreground="#ffffff", highlightthickness=1, relief="flat")
    openJsonBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    newJsonRBtn.configure(background="#383838", activebackground="#606060", highlightbackground="#383838", foreground="#ffffff", activeforeground="#ffffff", selectcolor="#383838", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    newJsonEnt.configure(background="#000000", highlightbackground="#ffffff", disabledbackground="#383838", foreground="#ffffff", highlightthickness=1, relief="flat")
    newJsonBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    paraTxt.configure(background="#383838", highlightbackground="#383838", foreground="#ffffff", highlightcolor="#ffffff")
    paraCvs.configure(background="#383838")
    paraCvs2.configure(background="#383838")
    paraFrm.configure(background="#383838")
    paraFrm2.configure(background="#383838")
    innerFrm.configure(background="#383838")
    paraLbl.configure(background="#383838", foreground="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    modifyLnk.configure(background="#383838", foreground="#63ACE5", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0")
    saveLnk.configure(background="#383838", foreground="#63ACE5", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0")
    captureImagesPara2Frm_all.configure(background="#383838")
    captureImagesPara2Frm_second.configure(background="#383838")
    captureImagesPara2Frm_frame.configure(background="#383838")
    showVideoLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    saveLogLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    outputFolderLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    outputFolderBtn.configure(width=6, background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    annotationTypeLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    readFramesLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    readFramesLbl_1.configure(background="#383838", foreground="#ffffff", anchor="w")
    readFramesLbl_2.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureTypeLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_allLbl_1.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_allLbl_2.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_frameLbl_1.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_frameLbl_2.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_secondLbl_1.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara2Frm_secondLbl_2.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara3FrmLbl_1.configure(background="#383838", foreground="#ffffff", anchor="w")
    captureImagesPara3FrmLbl_2.configure(background="#383838", foreground="#ffffff", anchor="w")
    minMotionFramesLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    minDeltaThreshLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    minAreaLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    jsonCreatedLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    jsonCreatedBtn.configure(width=6, background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat")
    jsonNotesLbl.configure(background="#383838", foreground="#ffffff", anchor="w")
    jsonNotesTxt.configure(background="#383838", foreground="#ffffff", highlightcolor="#ffffff")
    readFramesInnerFrm.configure(background="#383838")
    captureImagesPara2Frm_all.configure(background="#383838")
    captureImagesPara2Frm_frame.configure(background="#383838")
    captureImagesPara2Frm_second.configure(background="#383838")
    captureImagesPara3Frm.configure(background="#383838")
    startBtn.configure(background="#606060", activebackground="#909090", highlightbackground="#606060", foreground="#ffffff", activeforeground="#ffffff", borderwidth=0, relief="flat", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")

else:
    sourceLf.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    inputFolderRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    inputFolderEnt.configure(background="#F0F0F0", readonlybackground="#F0F0F0", highlightbackground="#1F1C19", foreground="#1F1C19", highlightthickness=1, relief="flat")
    inputFolderBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    inputFilesRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    fileLb.configure(background="#ffffff", foreground="#1F1C19")
    inputFilesBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    inputFilesClearBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    webcamRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    networkRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    networkMsg.configure(background="#ffffff", foreground="#1F1C19")
    configLf.configure(background="#ffffff", foreground="#1F1C19", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    openJsonRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    openJsonEnt.configure(background="#F0F0F0", readonlybackground="#F0F0F0", highlightbackground="#1F1C19", foreground="#1F1C19", highlightthickness=1, relief="flat")
    openJsonBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    newJsonRBtn.configure(background="#ffffff", activebackground="#E4E4E4", highlightbackground="#ffffff", foreground="#1F1C19", activeforeground="#1F1C19", selectcolor="#ffffff", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    newJsonEnt.configure(background="#ffffff", highlightbackground="#1F1C19", foreground="#1F1C19", highlightthickness=1, relief="flat")
    newJsonBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    paraTxt.configure(background="#ffffff", highlightbackground="#ffffff", foreground="#1F1C19", highlightcolor="#1F1C19")
    paraCvs.configure(background="#ffffff")
    paraCvs2.configure(background="#ffffff")
    paraFrm.configure(background="#ffffff")
    paraFrm2.configure(background="#ffffff")
    innerFrm.configure(background="#ffffff")
    paraLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")
    modifyLnk.configure(background="#ffffff", foreground="#1497EE", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0")
    saveLnk.configure(background="#ffffff", foreground="#1497EE", anchor="w", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 1 -overstrike 0")
    captureImagesPara2Frm_all.configure(background="#ffffff")
    captureImagesPara2Frm_second.configure(background="#ffffff")
    captureImagesPara2Frm_frame.configure(background="#ffffff")
    showVideoLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    saveLogLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    outputFolderLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    outputFolderBtn.configure(width=6, background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    annotationTypeLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    readFramesLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    readFramesLbl_1.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    readFramesLbl_2.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureTypeLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_allLbl_1.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_allLbl_2.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_frameLbl_1.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_frameLbl_2.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_secondLbl_1.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara2Frm_secondLbl_2.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara3FrmLbl_1.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    captureImagesPara3FrmLbl_2.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    minMotionFramesLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    minDeltaThreshLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    minAreaLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    jsonCreatedLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    jsonCreatedBtn.configure(width=6, background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat")
    jsonNotesLbl.configure(background="#ffffff", foreground="#1F1C19", anchor="w")
    jsonNotesTxt.configure(background="#ffffff", foreground="#1F1C19", highlightcolor="#1F1C19")
    readFramesInnerFrm.configure(background="#ffffff")
    captureImagesPara2Frm_all.configure(background="#ffffff")
    captureImagesPara2Frm_frame.configure(background="#ffffff")
    captureImagesPara2Frm_second.configure(background="#ffffff")
    captureImagesPara3Frm.configure(background="#ffffff")
    startBtn.configure(background="#E4E4E4", activebackground="#909090", highlightbackground="#E4E4E4", foreground="#1F1C19", activeforeground="#1F1C19", borderwidth=0, relief="flat", font="-family {Microsoft YaHei} -size 11 -weight normal -slant roman -underline 0 -overstrike 0")

window.mainloop()
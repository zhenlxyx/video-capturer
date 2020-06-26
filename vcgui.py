# -*- coding: UTF-8 -*-
# Xiangzhen Lu
# ver 200626.2326

# 用法

'''
pythonw vcgui.py
'''

# 导入必要的包
import warnings								  # 系统警告信息
import sys						    		  # 判断系统环境
import platform                               # 多操作系统支持
import json									  # 用户配置
import time									  # 时间操作
import os									  # 文件和文件夹操作
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
    saveAnnotations = conf["save_annotations"]
    saveLog = conf["save_log"]
    savePath = conf["output_folder"]
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

    except NameError:
        pass

    gui = True
    i = 1
    vc.startCapture(fileList, jsonPath, showVideo, saveAnnotations, saveLog, inputType, inputFiles, inputFolder, savePath, readFrames, captureType, captureImages, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes, gui, i)
    startBtn.configure(state="normal")
    inputFolderRBtn.configure(state="normal")
    inputFolderEnt.configure(state="normal")
    inputFolderBtn.configure(state="normal")
    inputFilesRBtn.configure(state="normal")
    fileLb.configure(state="normal")
    inputFilesBtn.configure(state="normal")
    inputFilesClearBtn.configure(state="normal")
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
    inputFilesVar.set("采集以下 {} 个视频：".format(fileCount))
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

def selectOpenJson():
    jsonVar.set("open")
    if inputVar.get() == "folder" and inputFolderEnt.get() != "" and openJsonEnt.get() != "":
        startBtn.configure(state="normal")
    elif inputVar.get() == "files" and len(fileLb.get("0", "end")) != 0 and openJsonEnt.get() != "":
        startBtn.configure(state="normal")

def selectNewJson():
    jsonVar.set("new")
    startBtn.configure(state="disabled")

def clearFiles():
    fileLb.delete(0, "end")
    fileLb2.delete(0, "end")
    del fileList[:]
    inputFilesVar.set("采集以下 {} 个视频：".format(fileCount))
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
        "show_detail": False,
        "save_annotations": False,
        "save_log": False,
        "output_folder": "output/",
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
    paraFrm.place(relx=0.04, rely=0.6, relheight=0.349
            , relwidth=0.931, bordermode='ignore')
    paraFrm2.place_forget()
    saveLnk.place(relx=0.16, rely=0.524, height=26, width=307
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

    if saveAnnotationsVar.get() == "是":
        saveAnnotations = True
    else:
        saveAnnotations = False

    if saveLogVar.get() == "是":
        saveLog = True
    else:
        saveLog = False

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
        "save_annotations": saveAnnotations,
        "save_log": saveLog,
        "output_folder": savePath,
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
    paraFrm2.place(relx=0.04, rely=0.6, relheight=0.349
            , relwidth=0.931, bordermode='ignore')

def openJson(jsonPath):
    try:
        with open(jsonPath, 'r', encoding='utf-8') as j:
            conf = json.load(j)

        showVideo = conf["show_video"]
        saveAnnotations = conf["save_annotations"]
        saveLog = conf["save_log"]

        savePath = conf["output_folder"]
        if type(savePath) != str:
            savePathError()
            return

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

        if type(saveAnnotations) != bool:
            captureOptionsError()
            return
        if saveAnnotations:
            saveAnnotations1 = "是"
        elif not saveAnnotations:
            saveAnnotations1 = "否"

        if type(saveLog) != bool:
            captureOptionsError()
            return
        if saveLog:
            saveLog1 = "是"
        elif not saveLog:
            saveLog1 = "否"

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
            captureImagesPara3 = "，每 {} 帧取一帧保存".format(captureImages[2])
        else:
            captureImagesError()
            return

        captureImages1 = "{}{}{}".format(captureImagesPara1, captureImagesPara2, captureImagesPara3)

        paraFrm2.place(relx=0.04, rely=0.6, relheight=0.349, relwidth=0.931
                , bordermode='ignore')
        modifyLnk.place(relx=0.16, rely=0.524, height=26, width=307
                , bordermode='ignore')
        paraLbl.place(relx=0.027, rely=0.524, height=26, width=357
                , bordermode='ignore')

        openJsonEnt2.delete(0, "end")
        openJsonVar.set(jsonPath.split("/")[-1])
        openJsonEnt2.insert("end", jsonPath)

        showVideoVar.set(showVideo1)
        showVideoMenu = tk.OptionMenu(innerFrm, showVideoVar, *showVideoOptions)
        showVideoMenu.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        saveAnnotationsVar.set(saveAnnotations1)
        saveAnnotationsMenu = tk.OptionMenu(innerFrm, saveAnnotationsVar, *saveAnnotationsOptions)
        saveAnnotationsMenu.grid(row=1, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        saveLogVar.set(saveLog1)
        saveLogMenu = tk.OptionMenu(innerFrm, saveLogVar, *saveLogOptions)
        saveLogMenu.grid(row=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

        outputFolderEnt.delete(0, "end")
        outputFolderEnt.insert("end", savePath)
        outputFolderEnt.grid(row=3, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")

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
保存图像中的标注：{}
保存采集日志：　　{}
输出目录：　　　　{}
视频读法：　　　　每 {} 帧取一帧读
采集算法：　　　　{}
采集方式：　　　　{}
运动帧最小值：　　{}
阈值增量最小值：　{}
轮廓区域最小值：　{}
设置文件创建时间：{}
设置文件备注：　　{}'''
            .format(showVideo1, saveAnnotations1, saveLog1, savePath, readFrames, captureType1, captureImages1, minMotionFrames, minDeltaThresh, minArea, jsonCreated, jsonNotes)
            )
        paraTxt.configure(state="disabled")

        jsonVar.set("open")

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
def changeSaveAnnotations(*args):
    saveAnnotationsVar.get()

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

# 窗口设置
window.geometry("800x530+320+50")
window.minsize(120, 1)
window.maxsize(3364, 1061)
window.resizable(0, 0)
window.title("视频图像采集器 (Video Capturer)")
window.iconphoto(True, tk.PhotoImage(file='./xiangzhenlu/app_icon.png'))
window.configure(background="#ffffff")
window.configure(highlightbackground="#d9d9d9")
window.configure(highlightcolor="black")

# 采集来源标签框架
sourceLf = tk.LabelFrame(window)
sourceLf.place(relx=0.025, rely=0.026, relheight=0.821
        , relwidth=0.469)
sourceLf.configure(relief='groove')
sourceLf.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
sourceLf.configure(foreground="black")
sourceLf.configure(text='''采集来源：''')
sourceLf.configure(background="#ffffff")
sourceLf.configure(highlightbackground="#d9d9d9")
sourceLf.configure(highlightcolor="black")

# 输入文件夹单选框
inputVar = StringVar(window)
inputVar.set("folder")
inputFolderRBtn = tk.Radiobutton(sourceLf)
inputFolderRBtn.place(relx=0.027, rely=0.076, relheight=0.067
        , relwidth=0.925, bordermode='ignore')
inputFolderRBtn.configure(activebackground="#d9d9d9")
inputFolderRBtn.configure(activeforeground="#000000")
inputFolderRBtn.configure(anchor='w')
inputFolderRBtn.configure(background="#ffffff")
inputFolderRBtn.configure(disabledforeground="#a3a3a3")
inputFolderRBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
inputFolderRBtn.configure(foreground="#000000")
inputFolderRBtn.configure(highlightbackground="#d9d9d9")
inputFolderRBtn.configure(highlightcolor="black")
inputFolderRBtn.configure(highlightthickness="0")
inputFolderRBtn.configure(justify='left')
inputFolderRBtn.configure(text='''采集此文件夹下的全部视频：''')
inputFolderRBtn.configure(value="folder")
inputFolderRBtn.configure(variable=inputVar)
inputFolderRBtn.configure(command=selectAddFolder)

# 输入文件夹文本框
inputFolderVar = tk.StringVar()
inputFolderEnt = tk.Entry(sourceLf)
inputFolderEnt.place(relx=0.104, rely=0.175, height=27
        , relwidth=0.677, bordermode='ignore')
inputFolderEnt.configure(background="white")
inputFolderEnt.configure(disabledforeground="#a3a3a3")
inputFolderEnt.configure(font="TkFixedFont")
inputFolderEnt.configure(foreground="#000000")
inputFolderEnt.configure(highlightbackground="#d9d9d9")
inputFolderEnt.configure(highlightcolor="black")
inputFolderEnt.configure(insertbackground="black")
inputFolderEnt.configure(selectbackground="#c4c4c4")
inputFolderEnt.configure(selectforeground="black")
inputFolderEnt.configure(textvariable=inputFolderVar)
inputFolderEnt.configure(state="readonly")

# 输入文件夹选择按钮
inputFolderBtn = tk.Button(sourceLf)
inputFolderBtn.place(relx=0.789, rely=0.175, height=28, width=65
        , bordermode='ignore')
inputFolderBtn.configure(activebackground="#ececec")
inputFolderBtn.configure(activeforeground="#000000")
inputFolderBtn.configure(background="#d9d9d9")
inputFolderBtn.configure(disabledforeground="#a3a3a3")
inputFolderBtn.configure(foreground="#000000")
inputFolderBtn.configure(highlightbackground="#d9d9d9")
inputFolderBtn.configure(highlightcolor="black")
inputFolderBtn.configure(pady="0")
inputFolderBtn.configure(text='''选择''')
inputFolderBtn.configure(command=addFolder)

# 输入文件单选框
inputFilesVar = tk.StringVar()
inputFilesVar.set("采集以下 {} 个视频：".format(fileCount))
inputFilesRBtn = tk.Radiobutton(sourceLf)
inputFilesRBtn.place(relx=0.027, rely=0.301, relheight=0.067
        , relwidth=0.925, bordermode='ignore')
inputFilesRBtn.configure(activebackground="#d9d9d9")
inputFilesRBtn.configure(activeforeground="#000000")
inputFilesRBtn.configure(anchor='w')
inputFilesRBtn.configure(background="#ffffff")
inputFilesRBtn.configure(disabledforeground="#a3a3a3")
inputFilesRBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
inputFilesRBtn.configure(foreground="#000000")
inputFilesRBtn.configure(highlightbackground="#d9d9d9")
inputFilesRBtn.configure(highlightcolor="black")
inputFilesRBtn.configure(highlightthickness="0")
inputFilesRBtn.configure(justify='left')
inputFilesRBtn.configure(value="files")
inputFilesRBtn.configure(variable=inputVar)
inputFilesRBtn.configure(textvariable=inputFilesVar)
inputFilesRBtn.configure(command=selectAddFiles)

# 输入文件列表框
fileLb = Listbox(sourceLf)
fileLb.place(relx=0.104, rely=0.4, relheight=0.549, relwidth=0.669
        , bordermode='ignore')
fileLb.configure(background="white")
fileLb.configure(cursor="xterm")
fileLb.configure(disabledforeground="#a3a3a3")
fileLb.configure(font="TkFixedFont")
fileLb.configure(foreground="black")
fileLb.configure(highlightbackground="#d9d9d9")
fileLb.configure(highlightcolor="#d9d9d9")
fileLb.configure(selectbackground="#c4c4c4")
fileLb.configure(selectforeground="black")
scrollBar = Scrollbar(fileLb)
scrollBar.pack(side="right", fill="y")
scrollBar.config(command=fileLb.yview)
fileLb.config(yscrollcommand=scrollBar.set)
fileLb.delete(0, "end")

fileLb2 = Listbox(sourceLf)
fileLb2.configure(background="white")
fileLb2.configure(cursor="xterm")
fileLb2.configure(disabledforeground="#a3a3a3")
fileLb2.configure(font="TkFixedFont")
fileLb2.configure(foreground="black")
fileLb2.configure(highlightbackground="#d9d9d9")
fileLb2.configure(highlightcolor="#d9d9d9")
fileLb2.configure(selectbackground="#c4c4c4")
fileLb2.configure(selectforeground="black")
fileLb2.delete(0, "end")

# 输入文件选择按钮
inputFilesBtn = tk.Button(sourceLf)
inputFilesBtn.place(relx=0.789, rely=0.4, height=28, width=65
        , bordermode='ignore')
inputFilesBtn.configure(activebackground="#ececec")
inputFilesBtn.configure(activeforeground="#000000")
inputFilesBtn.configure(background="#d9d9d9")
inputFilesBtn.configure(disabledforeground="#a3a3a3")
inputFilesBtn.configure(foreground="#000000")
inputFilesBtn.configure(highlightbackground="#d9d9d9")
inputFilesBtn.configure(highlightcolor="black")
inputFilesBtn.configure(pady="0")
inputFilesBtn.configure(text='''选择''')
inputFilesBtn.configure(command=addFiles)

# 清除输入文件选择按钮
inputFilesClearBtn = tk.Button(sourceLf)
inputFilesClearBtn.place(relx=0.789, rely=0.48, height=28, width=65
        , bordermode='ignore')
inputFilesClearBtn.configure(activebackground="#ececec")
inputFilesClearBtn.configure(activeforeground="#000000")
inputFilesClearBtn.configure(background="#d9d9d9")
inputFilesClearBtn.configure(disabledforeground="#a3a3a3")
inputFilesClearBtn.configure(foreground="#000000")
inputFilesClearBtn.configure(highlightbackground="#d9d9d9")
inputFilesClearBtn.configure(highlightcolor="black")
inputFilesClearBtn.configure(pady="0")
inputFilesClearBtn.configure(text='''清空''')
inputFilesClearBtn.configure(command=clearFiles)

# 采集选项标签框架
configLf = tk.LabelFrame(window)
configLf.place(relx=0.506, rely=0.026, relheight=0.821
        , relwidth=0.47)
configLf.configure(relief='groove')
configLf.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
configLf.configure(foreground="black")
configLf.configure(text='''采集选项：''')
configLf.configure(background="#ffffff")
configLf.configure(highlightbackground="#d9d9d9")
configLf.configure(highlightcolor="black")

# 打开设置文件单选框
jsonVar = StringVar(window)
jsonVar.set("open")
openJsonRBtn = tk.Radiobutton(configLf)
openJsonRBtn.place(relx=0.027, rely=0.076, relheight=0.067
        , relwidth=0.926, bordermode='ignore')
openJsonRBtn.configure(activebackground="#d9d9d9")
openJsonRBtn.configure(activeforeground="#000000")
openJsonRBtn.configure(anchor='w')
openJsonRBtn.configure(background="#ffffff")
openJsonRBtn.configure(disabledforeground="#a3a3a3")
openJsonRBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
openJsonRBtn.configure(foreground="#000000")
openJsonRBtn.configure(highlightbackground="#d9d9d9")
openJsonRBtn.configure(highlightcolor="black")
openJsonRBtn.configure(highlightthickness="0")
openJsonRBtn.configure(justify='left')
openJsonRBtn.configure(text='''加载现有设置文件：''')
openJsonRBtn.configure(value="open")
openJsonRBtn.configure(variable=jsonVar)
openJsonRBtn.configure(command=selectOpenJson)

# 打开设置文件文本框
openJsonVar = tk.StringVar()
openJsonEnt = tk.Entry(configLf)
openJsonEnt.place(relx=0.104, rely=0.175, height=27, relwidth=0.676
        , bordermode='ignore')
openJsonEnt.configure(background="white")
openJsonEnt.configure(disabledforeground="#a3a3a3")
openJsonEnt.configure(font="TkFixedFont")
openJsonEnt.configure(foreground="#000000")
openJsonEnt.configure(highlightbackground="#d9d9d9")
openJsonEnt.configure(highlightcolor="black")
openJsonEnt.configure(insertbackground="black")
openJsonEnt.configure(selectbackground="#c4c4c4")
openJsonEnt.configure(selectforeground="black")
openJsonEnt.configure(textvariable=openJsonVar)
openJsonEnt.configure(state="readonly")

openJsonEnt2 = tk.Entry(configLf)
openJsonEnt2.configure(background="white")
openJsonEnt2.configure(disabledforeground="#a3a3a3")
openJsonEnt2.configure(font="TkFixedFont")
openJsonEnt2.configure(foreground="#000000")
openJsonEnt2.configure(highlightbackground="#d9d9d9")
openJsonEnt2.configure(highlightcolor="black")
openJsonEnt2.configure(insertbackground="black")
openJsonEnt2.configure(selectbackground="#c4c4c4")
openJsonEnt2.configure(selectforeground="black")

# 打开设置文件选择按钮
openJsonBtn = tk.Button(configLf)
openJsonBtn.place(relx=0.79, rely=0.175, height=28, width=65
        , bordermode='ignore')
openJsonBtn.configure(activebackground="#ececec")
openJsonBtn.configure(activeforeground="#000000")
openJsonBtn.configure(background="#d9d9d9")
openJsonBtn.configure(disabledforeground="#a3a3a3")
openJsonBtn.configure(foreground="#000000")
openJsonBtn.configure(highlightbackground="#d9d9d9")
openJsonBtn.configure(highlightcolor="black")
openJsonBtn.configure(pady="0")
openJsonBtn.configure(text='''选择''')
openJsonBtn.configure(command=addJson)

# 新建设置文件单选框
newJsonRBtn = tk.Radiobutton(configLf)
newJsonRBtn.place(relx=0.027, rely=0.301, relheight=0.067
        , relwidth=0.926, bordermode='ignore')
newJsonRBtn.configure(activebackground="#d9d9d9")
newJsonRBtn.configure(activeforeground="#000000")
newJsonRBtn.configure(anchor='w')
newJsonRBtn.configure(background="#ffffff")
newJsonRBtn.configure(disabledforeground="#a3a3a3")
newJsonRBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
newJsonRBtn.configure(foreground="#000000")
newJsonRBtn.configure(highlightbackground="#d9d9d9")
newJsonRBtn.configure(highlightcolor="black")
newJsonRBtn.configure(highlightthickness="0")
newJsonRBtn.configure(justify='left')
newJsonRBtn.configure(text='''新建设置文件：''')
newJsonRBtn.configure(value="new")
newJsonRBtn.configure(variable=jsonVar)
newJsonRBtn.configure(command=selectNewJson)

# 新建设置文件文本框
newJsonEnt = tk.Entry(configLf)
newJsonEnt.place(relx=0.104, rely=0.4, height=27, relwidth=0.676
        , bordermode='ignore')
newJsonEnt.configure(background="white")
newJsonEnt.configure(disabledforeground="#a3a3a3")
newJsonEnt.configure(font="TkFixedFont")
newJsonEnt.configure(foreground="#000000")
newJsonEnt.configure(highlightbackground="#d9d9d9")
newJsonEnt.configure(highlightcolor="black")
newJsonEnt.configure(insertbackground="black")
newJsonEnt.configure(selectbackground="#c4c4c4")
newJsonEnt.configure(selectforeground="black")
newJsonEnt.insert("end", "为设置文件命名，例如 my_conf.json")
newJsonEnt.bind('<Button-1>', clearContent)

# 新建设置文件选择按钮
newJsonBtn = tk.Button(configLf)
newJsonBtn.place(relx=0.79, rely=0.4, height=28, width=65
        , bordermode='ignore')
newJsonBtn.configure(activebackground="#ececec")
newJsonBtn.configure(activeforeground="#000000")
newJsonBtn.configure(background="#d9d9d9")
newJsonBtn.configure(disabledforeground="#a3a3a3")
newJsonBtn.configure(foreground="#000000")
newJsonBtn.configure(highlightbackground="#d9d9d9")
newJsonBtn.configure(highlightcolor="black")
newJsonBtn.configure(pady="0")
newJsonBtn.configure(text='''新建''')
newJsonBtn.configure(command=newJson)

# 参数标签
paraLbl = tk.Label(configLf)
paraLbl.configure(activebackground="#f9f9f9")
paraLbl.configure(activeforeground="black")
paraLbl.configure(anchor='w')
paraLbl.configure(background="#ffffff")
paraLbl.configure(disabledforeground="#a3a3a3")
paraLbl.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
paraLbl.configure(foreground="#000000")
paraLbl.configure(highlightbackground="#d9d9d9")
paraLbl.configure(highlightcolor="black")
paraLbl.configure(justify='left')
paraLbl.configure(text='''参数：''')

# 修改参数链接
modifyLnk = tk.Label(configLf)
modifyLnk.configure(activebackground="#f9f9f9")
modifyLnk.configure(activeforeground="black")
modifyLnk.configure(anchor='w')
modifyLnk.configure(background="#ffffff")
modifyLnk.configure(disabledforeground="#a3a3a3")
modifyLnk.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 1 -overstrike 0")
modifyLnk.configure(foreground="#0080ff")
modifyLnk.configure(highlightbackground="#d9d9d9")
modifyLnk.configure(highlightcolor="black")
modifyLnk.configure(justify='left')
modifyLnk.configure(text='''修改''')
modifyLnk.configure(cursor="hand2")
modifyLnk.bind('<Button-1>', modifyJson)

# 保存参数链接
saveLnk = tk.Label(configLf)
saveLnk.configure(activebackground="#f9f9f9")
saveLnk.configure(activeforeground="black")
saveLnk.configure(anchor='w')
saveLnk.configure(background="#ffffff")
saveLnk.configure(disabledforeground="#a3a3a3")
saveLnk.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 1 -overstrike 0")
saveLnk.configure(foreground="#0080ff")
saveLnk.configure(highlightbackground="#d9d9d9")
saveLnk.configure(highlightcolor="black")
saveLnk.configure(justify='left')
saveLnk.configure(text='''保存修改''')
saveLnk.configure(cursor="hand2")
saveLnk.bind('<Button-1>', saveJson)

# 修改参数框架
paraFrm = tk.Frame(configLf)
paraFrm.configure(background="white")
paraFrm.configure(highlightbackground="#d9d9d9")
paraFrm.configure(highlightcolor="black")
paraFrm.configure(relief="flat")

paraCvs = tk.Canvas(paraFrm)
paraCvs.configure(background="white")
paraCvs.configure(borderwidth="0")
paraCvs.configure(relief="flat")
paraCvs.configure(highlightthickness="0")

innerFrm = tk.Frame(paraCvs)
innerFrm.configure(width="400")
innerFrm.configure(background="white")
innerFrm.configure(borderwidth="0")
innerFrm.configure(relief="flat")

scrollBar2=tk.Scrollbar(paraFrm,orient="vertical",command=paraCvs.yview)
paraCvs.configure(yscrollcommand=scrollBar2.set)

scrollBar2.pack(side="right",fill="y")
paraCvs.pack(side="left",fill="both")
paraCvs.create_window((0,0),window=innerFrm,anchor='nw')
innerFrm.bind("<Configure>", scrollEvent)

# 浏览参数框架
paraFrm2 = tk.Frame(configLf)
paraFrm2.configure(background="white")
paraFrm2.configure(highlightbackground="#d9d9d9")
paraFrm2.configure(highlightcolor="black")
paraFrm2.configure(relief="flat")

paraCvs2 = tk.Canvas(paraFrm2)
paraCvs2.configure(background="white")
paraCvs2.configure(borderwidth="0")
paraCvs2.configure(relief="flat")
paraCvs2.configure(highlightthickness="0")

paraTxt = tk.Text(paraCvs2)
paraTxt.configure(width="44")
paraTxt.configure(height="15")
paraTxt.configure(background="white")
paraTxt.configure(borderwidth="0")
paraTxt.configure(relief="flat")
paraTxt.configure(font="TkTextFont")
paraTxt.configure(foreground="black")
paraTxt.configure(highlightbackground="#d9d9d9")
paraTxt.configure(highlightcolor="black")
paraTxt.configure(highlightthickness="0")
paraTxt.configure(insertbackground="black")
paraTxt.configure(selectbackground="#c4c4c4")
paraTxt.configure(selectforeground="black")
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
showVideoLbl.configure(anchor='w')
showVideoLbl.configure(background="#ffffff")
showVideoLbl.configure(disabledforeground="#a3a3a3")
showVideoLbl.configure(foreground="#000000")
showVideoLbl.configure(justify='left')
showVideoLbl.configure(text='''显示采集窗口：''')

showVideoVar = StringVar(window)
showVideoOptions = ["是", "否"]
showVideoVar.trace('w', changeShowVideo)

saveAnnotationsLbl = tk.Label(innerFrm)
saveAnnotationsLbl.grid(row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
saveAnnotationsLbl.configure(activebackground="#f9f9f9")
saveAnnotationsLbl.configure(activeforeground="black")
saveAnnotationsLbl.configure(anchor='w')
saveAnnotationsLbl.configure(background="#ffffff")
saveAnnotationsLbl.configure(disabledforeground="#a3a3a3")
saveAnnotationsLbl.configure(foreground="#000000")
saveAnnotationsLbl.configure(highlightbackground="#d9d9d9")
saveAnnotationsLbl.configure(highlightcolor="black")
saveAnnotationsLbl.configure(justify='left')
saveAnnotationsLbl.configure(text='''保存图像中的标注：''')

saveAnnotationsVar = StringVar(window)
saveAnnotationsOptions = ["是", "否"]
saveAnnotationsVar.trace('w', changeSaveAnnotations)

saveLogLbl = tk.Label(innerFrm)
saveLogLbl.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
saveLogLbl.configure(activebackground="#f9f9f9")
saveLogLbl.configure(activeforeground="black")
saveLogLbl.configure(anchor='w')
saveLogLbl.configure(background="#ffffff")
saveLogLbl.configure(disabledforeground="#a3a3a3")
saveLogLbl.configure(foreground="#000000")
saveLogLbl.configure(highlightbackground="#d9d9d9")
saveLogLbl.configure(highlightcolor="black")
saveLogLbl.configure(justify='left')
saveLogLbl.configure(text='''保存采集日志：''')

saveLogVar = StringVar(window)
saveLogOptions = ["是", "否"]
saveLogVar.trace('w', changeSaveLog)

outputFolderLbl = tk.Label(innerFrm)
outputFolderLbl.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
outputFolderLbl.configure(activebackground="#f9f9f9")
outputFolderLbl.configure(activeforeground="black")
outputFolderLbl.configure(anchor='w')
outputFolderLbl.configure(background="#ffffff")
outputFolderLbl.configure(disabledforeground="#a3a3a3")
outputFolderLbl.configure(foreground="#000000")
outputFolderLbl.configure(highlightbackground="#d9d9d9")
outputFolderLbl.configure(highlightcolor="black")
outputFolderLbl.configure(justify='left')
outputFolderLbl.configure(text='''输出目录：''')

outputFolderEnt = tk.Entry(innerFrm)

outputFolderBtn = tk.Button(innerFrm)
outputFolderBtn.grid(row=3, column=3, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
outputFolderBtn.configure(activebackground="#ececec")
outputFolderBtn.configure(activeforeground="#000000")
outputFolderBtn.configure(background="#d9d9d9")
outputFolderBtn.configure(disabledforeground="#a3a3a3")
outputFolderBtn.configure(foreground="#000000")
outputFolderBtn.configure(highlightbackground="#d9d9d9")
outputFolderBtn.configure(highlightcolor="black")
outputFolderBtn.configure(pady="0")
outputFolderBtn.configure(text='''选择''')
outputFolderBtn.configure(command=addOutputFolder)

readFramesLbl = tk.Label(innerFrm)
readFramesLbl.grid(row=4, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl.configure(activebackground="#f9f9f9")
readFramesLbl.configure(activeforeground="black")
readFramesLbl.configure(anchor='w')
readFramesLbl.configure(background="#ffffff")
readFramesLbl.configure(disabledforeground="#a3a3a3")
readFramesLbl.configure(foreground="#000000")
readFramesLbl.configure(highlightbackground="#d9d9d9")
readFramesLbl.configure(highlightcolor="black")
readFramesLbl.configure(justify='left')
readFramesLbl.configure(text='''视频读法：''')

readFramesInnerFrm = tk.Frame(innerFrm)
readFramesInnerFrm.grid(row=4, columnspan=2, column=1, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesInnerFrm.configure(width="400")
readFramesInnerFrm.configure(background="white")
readFramesInnerFrm.configure(borderwidth="0")
readFramesInnerFrm.configure(relief="flat")

readFramesLbl_1 = tk.Label(readFramesInnerFrm)
readFramesLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl_1.configure(activebackground="#f9f9f9")
readFramesLbl_1.configure(activeforeground="black")
readFramesLbl_1.configure(anchor='w')
readFramesLbl_1.configure(background="#ffffff")
readFramesLbl_1.configure(disabledforeground="#a3a3a3")
readFramesLbl_1.configure(foreground="#000000")
readFramesLbl_1.configure(highlightbackground="#d9d9d9")
readFramesLbl_1.configure(highlightcolor="black")
readFramesLbl_1.configure(justify='left')
readFramesLbl_1.configure(text='''每''')

readFramesSb = tk.Spinbox(readFramesInnerFrm, from_=1.0, to=1000.0)
readFramesSb.configure(width="4")
readFramesSb.configure(activebackground="#f9f9f9")
readFramesSb.configure(background="white")
readFramesSb.configure(buttonbackground="#d9d9d9")
readFramesSb.configure(disabledforeground="#a3a3a3")
readFramesSb.configure(font="TkDefaultFont")
readFramesSb.configure(foreground="black")
readFramesSb.configure(highlightbackground="black")
readFramesSb.configure(highlightcolor="black")
readFramesSb.configure(insertbackground="black")
readFramesSb.configure(selectbackground="#c4c4c4")
readFramesSb.configure(selectforeground="black")

readFramesLbl_2 = tk.Label(readFramesInnerFrm)
readFramesLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
readFramesLbl_2.configure(activebackground="#f9f9f9")
readFramesLbl_2.configure(activeforeground="black")
readFramesLbl_2.configure(anchor='w')
readFramesLbl_2.configure(background="#ffffff")
readFramesLbl_2.configure(disabledforeground="#a3a3a3")
readFramesLbl_2.configure(foreground="#000000")
readFramesLbl_2.configure(highlightbackground="#d9d9d9")
readFramesLbl_2.configure(highlightcolor="black")
readFramesLbl_2.configure(justify='left')
readFramesLbl_2.configure(text='''帧取一帧读''')

captureTypeLbl = tk.Label(innerFrm)
captureTypeLbl.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureTypeLbl.configure(activebackground="#f9f9f9")
captureTypeLbl.configure(activeforeground="black")
captureTypeLbl.configure(anchor='w')
captureTypeLbl.configure(background="#ffffff")
captureTypeLbl.configure(disabledforeground="#a3a3a3")
captureTypeLbl.configure(foreground="#000000")
captureTypeLbl.configure(highlightbackground="#d9d9d9")
captureTypeLbl.configure(highlightcolor="black")
captureTypeLbl.configure(justify='left')
captureTypeLbl.configure(text='''采集算法：''')

captureTypeVar = StringVar(window)
captureTypeOptions = ["多帧加权平均法", "二帧差分法", "三帧差分法"]
captureTypeVar.trace('w', changeCaptureType)

captureImagesLbl = tk.Label(innerFrm)
captureImagesLbl.grid(row=6, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesLbl.configure(activebackground="#f9f9f9")
captureImagesLbl.configure(activeforeground="black")
captureImagesLbl.configure(anchor='w')
captureImagesLbl.configure(background="#ffffff")
captureImagesLbl.configure(disabledforeground="#a3a3a3")
captureImagesLbl.configure(foreground="#000000")
captureImagesLbl.configure(highlightbackground="#d9d9d9")
captureImagesLbl.configure(highlightcolor="black")
captureImagesLbl.configure(justify='left')
captureImagesLbl.configure(text='''采集方式：''')

captureImagesPara1Var = StringVar(window)
captureImagesPara1Options = ["应采尽采", "按帧采集", "按秒采集"]
captureImagesPara1Var.trace('w', changeCaptureImagesPara1)

captureImagesPara2Frm_all = tk.Frame(innerFrm)
captureImagesPara2Frm_all.configure(width="400")
captureImagesPara2Frm_all.configure(background="white")
captureImagesPara2Frm_all.configure(borderwidth="0")
captureImagesPara2Frm_all.configure(relief="flat")

captureImagesPara2Frm_allLbl_1 = tk.Label(captureImagesPara2Frm_all)
captureImagesPara2Frm_allLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_allLbl_1.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_allLbl_1.configure(activeforeground="black")
captureImagesPara2Frm_allLbl_1.configure(anchor='w')
captureImagesPara2Frm_allLbl_1.configure(background="#ffffff")
captureImagesPara2Frm_allLbl_1.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_allLbl_1.configure(foreground="#000000")
captureImagesPara2Frm_allLbl_1.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_allLbl_1.configure(highlightcolor="black")
captureImagesPara2Frm_allLbl_1.configure(justify='left')
captureImagesPara2Frm_allLbl_1.configure(text='''每''')

captureImagesPara2Sb_all = tk.Spinbox(captureImagesPara2Frm_all, from_=1.0, to=1000.0)
captureImagesPara2Sb_all.configure(width="4")
captureImagesPara2Sb_all.configure(activebackground="#f9f9f9")
captureImagesPara2Sb_all.configure(background="white")
captureImagesPara2Sb_all.configure(buttonbackground="#d9d9d9")
captureImagesPara2Sb_all.configure(disabledforeground="#a3a3a3")
captureImagesPara2Sb_all.configure(font="TkDefaultFont")
captureImagesPara2Sb_all.configure(foreground="black")
captureImagesPara2Sb_all.configure(highlightbackground="black")
captureImagesPara2Sb_all.configure(highlightcolor="black")
captureImagesPara2Sb_all.configure(insertbackground="black")
captureImagesPara2Sb_all.configure(selectbackground="#c4c4c4")
captureImagesPara2Sb_all.configure(selectforeground="black")

captureImagesPara2Frm_allLbl_2 = tk.Label(captureImagesPara2Frm_all)
captureImagesPara2Frm_allLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_allLbl_2.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_allLbl_2.configure(activeforeground="black")
captureImagesPara2Frm_allLbl_2.configure(anchor='w')
captureImagesPara2Frm_allLbl_2.configure(background="#ffffff")
captureImagesPara2Frm_allLbl_2.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_allLbl_2.configure(foreground="#000000")
captureImagesPara2Frm_allLbl_2.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_allLbl_2.configure(highlightcolor="black")
captureImagesPara2Frm_allLbl_2.configure(justify='left')
captureImagesPara2Frm_allLbl_2.configure(text='''帧取一帧保存''')

captureImagesPara2Frm_frame = tk.Frame(innerFrm)
captureImagesPara2Frm_frame.configure(width="400")
captureImagesPara2Frm_frame.configure(background="white")
captureImagesPara2Frm_frame.configure(borderwidth="0")
captureImagesPara2Frm_frame.configure(relief="flat")

captureImagesPara2Frm_frameLbl_1 = tk.Label(captureImagesPara2Frm_frame)
captureImagesPara2Frm_frameLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_frameLbl_1.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_frameLbl_1.configure(activeforeground="black")
captureImagesPara2Frm_frameLbl_1.configure(anchor='w')
captureImagesPara2Frm_frameLbl_1.configure(background="#ffffff")
captureImagesPara2Frm_frameLbl_1.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_frameLbl_1.configure(foreground="#000000")
captureImagesPara2Frm_frameLbl_1.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_frameLbl_1.configure(highlightcolor="black")
captureImagesPara2Frm_frameLbl_1.configure(justify='left')
captureImagesPara2Frm_frameLbl_1.configure(text='''采集''')

captureImagesPara2Sb_frame = tk.Spinbox(captureImagesPara2Frm_frame, from_=1.0, to=1000.0)
captureImagesPara2Sb_frame.configure(width="4")
captureImagesPara2Sb_frame.configure(activebackground="#f9f9f9")
captureImagesPara2Sb_frame.configure(background="white")
captureImagesPara2Sb_frame.configure(buttonbackground="#d9d9d9")
captureImagesPara2Sb_frame.configure(disabledforeground="#a3a3a3")
captureImagesPara2Sb_frame.configure(font="TkDefaultFont")
captureImagesPara2Sb_frame.configure(foreground="black")
captureImagesPara2Sb_frame.configure(highlightbackground="black")
captureImagesPara2Sb_frame.configure(highlightcolor="black")
captureImagesPara2Sb_frame.configure(insertbackground="black")
captureImagesPara2Sb_frame.configure(selectbackground="#c4c4c4")
captureImagesPara2Sb_frame.configure(selectforeground="black")

captureImagesPara2Frm_frameLbl_2 = tk.Label(captureImagesPara2Frm_frame)
captureImagesPara2Frm_frameLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_frameLbl_2.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_frameLbl_2.configure(activeforeground="black")
captureImagesPara2Frm_frameLbl_2.configure(anchor='w')
captureImagesPara2Frm_frameLbl_2.configure(background="#ffffff")
captureImagesPara2Frm_frameLbl_2.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_frameLbl_2.configure(foreground="#000000")
captureImagesPara2Frm_frameLbl_2.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_frameLbl_2.configure(highlightcolor="black")
captureImagesPara2Frm_frameLbl_2.configure(justify='left')
captureImagesPara2Frm_frameLbl_2.configure(text='''帧''')

captureImagesPara2Frm_second = tk.Frame(innerFrm)
captureImagesPara2Frm_second.configure(width="400")
captureImagesPara2Frm_second.configure(background="white")
captureImagesPara2Frm_second.configure(borderwidth="0")
captureImagesPara2Frm_second.configure(relief="flat")

captureImagesPara2Frm_secondLbl_1 = tk.Label(captureImagesPara2Frm_second)
captureImagesPara2Frm_secondLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_secondLbl_1.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_secondLbl_1.configure(activeforeground="black")
captureImagesPara2Frm_secondLbl_1.configure(anchor='w')
captureImagesPara2Frm_secondLbl_1.configure(background="#ffffff")
captureImagesPara2Frm_secondLbl_1.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_secondLbl_1.configure(foreground="#000000")
captureImagesPara2Frm_secondLbl_1.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_secondLbl_1.configure(highlightcolor="black")
captureImagesPara2Frm_secondLbl_1.configure(justify='left')
captureImagesPara2Frm_secondLbl_1.configure(text='''采集''')

captureImagesPara2Sb_second = tk.Spinbox(captureImagesPara2Frm_second, from_=1.0, to=1000.0)
captureImagesPara2Sb_second.configure(width="4")
captureImagesPara2Sb_second.configure(activebackground="#f9f9f9")
captureImagesPara2Sb_second.configure(background="white")
captureImagesPara2Sb_second.configure(buttonbackground="#d9d9d9")
captureImagesPara2Sb_second.configure(disabledforeground="#a3a3a3")
captureImagesPara2Sb_second.configure(font="TkDefaultFont")
captureImagesPara2Sb_second.configure(foreground="black")
captureImagesPara2Sb_second.configure(highlightbackground="black")
captureImagesPara2Sb_second.configure(highlightcolor="black")
captureImagesPara2Sb_second.configure(insertbackground="black")
captureImagesPara2Sb_second.configure(selectbackground="#c4c4c4")
captureImagesPara2Sb_second.configure(selectforeground="black")

captureImagesPara2Frm_secondLbl_2 = tk.Label(captureImagesPara2Frm_second)
captureImagesPara2Frm_secondLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara2Frm_secondLbl_2.configure(activebackground="#f9f9f9")
captureImagesPara2Frm_secondLbl_2.configure(activeforeground="black")
captureImagesPara2Frm_secondLbl_2.configure(anchor='w')
captureImagesPara2Frm_secondLbl_2.configure(background="#ffffff")
captureImagesPara2Frm_secondLbl_2.configure(disabledforeground="#a3a3a3")
captureImagesPara2Frm_secondLbl_2.configure(foreground="#000000")
captureImagesPara2Frm_secondLbl_2.configure(highlightbackground="#d9d9d9")
captureImagesPara2Frm_secondLbl_2.configure(highlightcolor="black")
captureImagesPara2Frm_secondLbl_2.configure(justify='left')
captureImagesPara2Frm_secondLbl_2.configure(text='''秒''')

captureImagesPara3Frm = tk.Frame(innerFrm)
captureImagesPara3Frm.configure(width="400")
captureImagesPara3Frm.configure(background="white")
captureImagesPara3Frm.configure(borderwidth="0")
captureImagesPara3Frm.configure(relief="flat")

captureImagesPara3FrmLbl_1 = tk.Label(captureImagesPara3Frm)
captureImagesPara3FrmLbl_1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara3FrmLbl_1.configure(activebackground="#f9f9f9")
captureImagesPara3FrmLbl_1.configure(activeforeground="black")
captureImagesPara3FrmLbl_1.configure(anchor='w')
captureImagesPara3FrmLbl_1.configure(background="#ffffff")
captureImagesPara3FrmLbl_1.configure(disabledforeground="#a3a3a3")
captureImagesPara3FrmLbl_1.configure(foreground="#000000")
captureImagesPara3FrmLbl_1.configure(highlightbackground="#d9d9d9")
captureImagesPara3FrmLbl_1.configure(highlightcolor="black")
captureImagesPara3FrmLbl_1.configure(justify='left')
captureImagesPara3FrmLbl_1.configure(text='''每''')

captureImagesPara3Sb = tk.Spinbox(captureImagesPara3Frm, from_=1.0, to=1000.0)
captureImagesPara3Sb.configure(width="4")
captureImagesPara3Sb.configure(activebackground="#f9f9f9")
captureImagesPara3Sb.configure(background="white")
captureImagesPara3Sb.configure(buttonbackground="#d9d9d9")
captureImagesPara3Sb.configure(disabledforeground="#a3a3a3")
captureImagesPara3Sb.configure(font="TkDefaultFont")
captureImagesPara3Sb.configure(foreground="black")
captureImagesPara3Sb.configure(highlightbackground="black")
captureImagesPara3Sb.configure(highlightcolor="black")
captureImagesPara3Sb.configure(insertbackground="black")
captureImagesPara3Sb.configure(selectbackground="#c4c4c4")
captureImagesPara3Sb.configure(selectforeground="black")

captureImagesPara3FrmLbl_2 = tk.Label(captureImagesPara3Frm)
captureImagesPara3FrmLbl_2.grid(row=0, column=2, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
captureImagesPara3FrmLbl_2.configure(activebackground="#f9f9f9")
captureImagesPara3FrmLbl_2.configure(activeforeground="black")
captureImagesPara3FrmLbl_2.configure(anchor='w')
captureImagesPara3FrmLbl_2.configure(background="#ffffff")
captureImagesPara3FrmLbl_2.configure(disabledforeground="#a3a3a3")
captureImagesPara3FrmLbl_2.configure(foreground="#000000")
captureImagesPara3FrmLbl_2.configure(highlightbackground="#d9d9d9")
captureImagesPara3FrmLbl_2.configure(highlightcolor="black")
captureImagesPara3FrmLbl_2.configure(justify='left')
captureImagesPara3FrmLbl_2.configure(text='''帧取一帧保存''')

minMotionFramesLbl = tk.Label(innerFrm)
minMotionFramesLbl.grid(row=9, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minMotionFramesLbl.configure(activebackground="#f9f9f9")
minMotionFramesLbl.configure(activeforeground="black")
minMotionFramesLbl.configure(anchor='w')
minMotionFramesLbl.configure(background="#ffffff")
minMotionFramesLbl.configure(disabledforeground="#a3a3a3")
minMotionFramesLbl.configure(foreground="#000000")
minMotionFramesLbl.configure(highlightbackground="#d9d9d9")
minMotionFramesLbl.configure(highlightcolor="black")
minMotionFramesLbl.configure(justify='left')
minMotionFramesLbl.configure(text='''运动帧最小值：''')

minMotionFramesSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minMotionFramesSb.configure(width="4")
minMotionFramesSb.configure(activebackground="#f9f9f9")
minMotionFramesSb.configure(background="white")
minMotionFramesSb.configure(buttonbackground="#d9d9d9")
minMotionFramesSb.configure(disabledforeground="#a3a3a3")
minMotionFramesSb.configure(font="TkDefaultFont")
minMotionFramesSb.configure(foreground="black")
minMotionFramesSb.configure(highlightbackground="black")
minMotionFramesSb.configure(highlightcolor="black")
minMotionFramesSb.configure(insertbackground="black")
minMotionFramesSb.configure(selectbackground="#c4c4c4")
minMotionFramesSb.configure(selectforeground="black")

minDeltaThreshLbl = tk.Label(innerFrm)
minDeltaThreshLbl.grid(row=10, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minDeltaThreshLbl.configure(activebackground="#f9f9f9")
minDeltaThreshLbl.configure(activeforeground="black")
minDeltaThreshLbl.configure(anchor='w')
minDeltaThreshLbl.configure(background="#ffffff")
minDeltaThreshLbl.configure(disabledforeground="#a3a3a3")
minDeltaThreshLbl.configure(foreground="#000000")
minDeltaThreshLbl.configure(highlightbackground="#d9d9d9")
minDeltaThreshLbl.configure(highlightcolor="black")
minDeltaThreshLbl.configure(justify='left')
minDeltaThreshLbl.configure(text='''阈值增量最小值：''')

minDeltaThreshSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minDeltaThreshSb.configure(width="4")
minDeltaThreshSb.configure(activebackground="#f9f9f9")
minDeltaThreshSb.configure(background="white")
minDeltaThreshSb.configure(buttonbackground="#d9d9d9")
minDeltaThreshSb.configure(disabledforeground="#a3a3a3")
minDeltaThreshSb.configure(font="TkDefaultFont")
minDeltaThreshSb.configure(foreground="black")
minDeltaThreshSb.configure(highlightbackground="black")
minDeltaThreshSb.configure(highlightcolor="black")
minDeltaThreshSb.configure(insertbackground="black")
minDeltaThreshSb.configure(selectbackground="#c4c4c4")
minDeltaThreshSb.configure(selectforeground="black")

minAreaLbl = tk.Label(innerFrm)
minAreaLbl.grid(row=11, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
minAreaLbl.configure(activebackground="#f9f9f9")
minAreaLbl.configure(activeforeground="black")
minAreaLbl.configure(anchor='w')
minAreaLbl.configure(background="#ffffff")
minAreaLbl.configure(disabledforeground="#a3a3a3")
minAreaLbl.configure(foreground="#000000")
minAreaLbl.configure(highlightbackground="#d9d9d9")
minAreaLbl.configure(highlightcolor="black")
minAreaLbl.configure(justify='left')
minAreaLbl.configure(text='''轮廓区域最小值：''')

minAreaSb = tk.Spinbox(innerFrm, from_=1.0, to=1000.0)
minAreaSb.configure(width="4")
minAreaSb.configure(activebackground="#f9f9f9")
minAreaSb.configure(background="white")
minAreaSb.configure(buttonbackground="#d9d9d9")
minAreaSb.configure(disabledforeground="#a3a3a3")
minAreaSb.configure(font="TkDefaultFont")
minAreaSb.configure(foreground="black")
minAreaSb.configure(highlightbackground="black")
minAreaSb.configure(highlightcolor="black")
minAreaSb.configure(insertbackground="black")
minAreaSb.configure(selectbackground="#c4c4c4")
minAreaSb.configure(selectforeground="black")

jsonCreatedLbl = tk.Label(innerFrm)
jsonCreatedLbl.grid(row=12, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonCreatedLbl.configure(activebackground="#f9f9f9")
jsonCreatedLbl.configure(activeforeground="black")
jsonCreatedLbl.configure(anchor='w')
jsonCreatedLbl.configure(background="#ffffff")
jsonCreatedLbl.configure(disabledforeground="#a3a3a3")
jsonCreatedLbl.configure(foreground="#000000")
jsonCreatedLbl.configure(highlightbackground="#d9d9d9")
jsonCreatedLbl.configure(highlightcolor="black")
jsonCreatedLbl.configure(justify='left')
jsonCreatedLbl.configure(text='''设置文件创建时间：''')

jsonCreatedEnt = tk.Entry(innerFrm)

jsonCreatedBtn = tk.Button(innerFrm)
jsonCreatedBtn.grid(row=12, column=3, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonCreatedBtn.configure(activebackground="#ececec")
jsonCreatedBtn.configure(activeforeground="#000000")
jsonCreatedBtn.configure(background="#d9d9d9")
jsonCreatedBtn.configure(disabledforeground="#a3a3a3")
jsonCreatedBtn.configure(foreground="#000000")
jsonCreatedBtn.configure(highlightbackground="#d9d9d9")
jsonCreatedBtn.configure(highlightcolor="black")
jsonCreatedBtn.configure(pady="0")
jsonCreatedBtn.configure(text='''更新''')
jsonCreatedBtn.configure(command=updateTime)

jsonNotesLbl = tk.Label(innerFrm)
jsonNotesLbl.grid(row=13, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="w")
jsonNotesLbl.configure(activebackground="#f9f9f9")
jsonNotesLbl.configure(activeforeground="black")
jsonNotesLbl.configure(anchor='w')
jsonNotesLbl.configure(background="#ffffff")
jsonNotesLbl.configure(disabledforeground="#a3a3a3")
jsonNotesLbl.configure(foreground="#000000")
jsonNotesLbl.configure(highlightbackground="#d9d9d9")
jsonNotesLbl.configure(highlightcolor="black")
jsonNotesLbl.configure(justify='left')
jsonNotesLbl.configure(text='''设置文件备注：''')

jsonNotesTxt = Text(innerFrm)
jsonNotesTxt.configure(width="25")
jsonNotesTxt.configure(height="2")
jsonNotesTxt.configure(background="white")
jsonNotesTxt.configure(borderwidth="1")
jsonNotesTxt.configure(font="TkTextFont")
jsonNotesTxt.configure(foreground="black")
jsonNotesTxt.configure(highlightbackground="#d9d9d9")
jsonNotesTxt.configure(highlightcolor="black")
jsonNotesTxt.configure(highlightthickness="0")
jsonNotesTxt.configure(insertbackground="black")
jsonNotesTxt.configure(selectbackground="#c4c4c4")
jsonNotesTxt.configure(selectforeground="black")
jsonNotesTxt.configure(wrap="word")
jsonNotesTxt.configure(spacing1="1")
jsonNotesTxt.configure(spacing2="1")
jsonNotesTxt.configure(spacing3="1")

# 开始采集按钮
startBtn = tk.Button(window)
startBtn.place(relx=0.413, rely=0.887, height=38, width=139)
startBtn.configure(activebackground="#ececec")
startBtn.configure(activeforeground="#000000")
startBtn.configure(background="#d9d9d9")
startBtn.configure(disabledforeground="#a3a3a3")
startBtn.configure(font="-family {Microsoft YaHei} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
startBtn.configure(foreground="#000000")
startBtn.configure(highlightbackground="#d9d9d9")
startBtn.configure(highlightcolor="black")
startBtn.configure(pady="0")
startBtn.configure(text='''▶  开始采集''')
startBtn.configure(command=start)
startBtn.configure(state="disabled")

window.mainloop()
# video-capturer
 从视频中捕捉包含运动的画面

## 系统支持

* Microsoft Windows 10 版本 1809 或更新
* Python 3 以上
* OpenCV 3 或以上

## 开始使用之前

1. 安装 Python 环境

   打开 Microsoft Store 应用，搜索“Python”并下载 Python 3.7 / 3.8。

2. 安装 OpenCV

   打开命令提示符，输入 pip install opencv-python 并回车，等待安装完成。

3. 安装 imutils 图像操作简便函数集

   打开命令提示符，输入 pip install imutils 并回车，等待安装完成。

4. X安装 ffmpeg 并设置

   在浏览器中访问 https://ffmpeg.zeranoe.com/builds/，下载最新稳定版本并解压缩。

   可选：在 C:\Program Files 建立 ffmpeg 文件夹，将解压的所有文件何文件夹（如 bin）移动到 ffmpeg 文件夹下。

   在系统搜索中搜索“环境变量”，单击第一个结果。单击“环境变量”，在“系统变量”下找到 Path，单击“编辑”，“新建”并输入 C:\Program Files\ffmpeg\bin\，然后确定。

   打开命令提示符，输入 ffmpeg.exe -loglevel panic 并回车。
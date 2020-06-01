# video-capturer
 从视频中捕捉包含运动的画面

## 最新版本

ver 200601.1350

新增功能：

* 在视频窗口上显示当前视频的估计剩余时间。

修复问题：

* 修复了在静默采集且隐藏窗口的设置下，不能正常采集的问题。

已知问题：

* 在 Windows 上，部分 H264 编码的视频在采集过程中遇到终端报错，不影响采集，但可能影响性能。

  错误信息：

  ```
  [NULL @ 00000230ac4d4a00] non-existing PPS 0 referenced
  ```

  变通办法：

  * 转换视频格式

  * 使用静默采集模式：

    ```
    pythonw start.py
    ```

## 系统支持

* Windows, macOS, Linux
* Python 3 以上
* OpenCV 3 或以上

## 软件结构

video-capturer 的默认结构如下：

| 目录 / 文件       | 描述                   | 可设定 | 可删除 |
| ----------------- | ---------------------- | ------ | ------ |
| [video-capturer]  | 根目录                 |        |        |
| - [input]         | “输入”目录             | v      | v      |
| - [log]           | 日志目录               |        | v      |
| - [output]        | “输出”目录             | v      | v      |
| - [pyimagesearch] | 图像采集过程中用到的包 |        |        |
| - flow_chart.jpg  | 软件流程图             |        | v      |
| - conf.json       | 图像采集的设置文件示例 | v      |        |
| - conf_2.json     | 图像采集的设置文件示例 | v      | v      |
| - README.md       | 软件说明文档           |        |        |
| - install.py      | 软件安装程序           |        |        |
| - start.py        | 软件主程序             |        |        |

与软件功能无关的文件虽不在上述列表中，不可删除。

## 准备工作

以 Windows 10 为例：

1. 安装 Python

   打开 Microsoft Store 应用，搜索“Python”并下载 Python 3.7 / 3.8。

2. 安装依赖包

   在 video-capturer 目录下，以管理员身份打开命令提示符或 PowerShell，输入 

   ```
   python install.py
   ```

    开始安装。安装完成后，即可开始使用 video-capturer。

## 采集图像

### 准备视频文件

将待采集的视频文件放到“输入”目录下，路径可以在 .json 文件中修改。video-capturer 只会查找在该文件夹（不包括子文件夹）中的所有视频文件，批量进行图像采集。

支持的视频文件格式：.mp4, .avi, .mov, .mpeg, .flv, .wmv。

### 设置采集选项

video-capturer 使用 .json 文件规定采集图像过程中的设置，默认使用根目录下的 conf.json 文件。包括以下参数：

| 参数              | 描述                                                         | 值   | 描述         |
| ----------------- | --------------------------------------------- | ---- | --------------------------- |
| show_video        | 在采集图像时显示视频、阈值、帧增量三个窗口，禁用可以加快捕捉速度。    | true | 显示窗口 |
|  |  | false | 隐藏窗口 |
| show_detail       | 在采集图像时显示采集记录，禁用可以使终端输出看起来简洁。 | true | 显示采集记录 |
|  |  | false | 隐藏采集记录 |
| input_folder | “输入”目录，即视频文件所在目录。例如，如果为 input/，则只在该文件夹（不包括子文件夹）中查找视频文件。 | 路径，以 / 结尾 |  |
| output_folder     | “输出”目录，即采集图像的保存位置。例如，如果为 output/，则保存在“output/视频名称__设置名称”目录下。 | 路径，以 / 结尾 |              |
| read_frames       | 视频文件的读法，即每几帧取一帧读。 | 1 | 按帧读取视频 |
|  |  | n | 每 n 帧取一帧读 |
| capture_type      | 图像的采集算法，包括多帧加权平均法、二帧差分法、三帧差分法。 | avg | 多帧加权平均法 |
|  |  | two | 二帧差分法 |
|  |  | three | 三帧差分法 |
| capture_images    | 图像的采集方式，包括应采尽采、采集多帧、采集多秒。该选项是一个数组，第一个参数规定侦测到运动时采集图像的方式，第二、三个参数规定相应数值（第三个值不存在时要填 0）。 | ["all", n, 0] | 应采尽采，每 n 帧取一帧保存 |
|  |  | ["frame", n, 0] | 采集 n 帧 |
|  |  | ["second", n, m] | 采集 n 秒，每 n 帧取一帧保存 |
| save_annotations  | 保存带标记的图像，包括轮廓、视频播放时间、帧编号等信息。 | true | 保存带有标记的、宽度为 500 的图像 |
|  |  | false | 保存不带标记的、原始大小的图像 |
| save_log          | 保存本次采集的日志。日志将保存到 log/ 目录下、以本次采集开始时间命名的 .log 文件中。部分错误信息不会出现在日志中。 | true | 保存日志 |
|  |  | false | 不保存日志 |
| min_motion_frames | 运动帧最小值，即在图像保存到磁盘之前包含运动的连续帧的最小数量。值越小，保存的图像越多，但偶发运动的结果也会更多。 | n | 连续侦测到运动超过 n 帧，才保存这一批连续运动的图像 |
| min_delta_thresh  | 阈值增量最小值，即令给定像素被判定为“运动”的、当前帧和平均帧 / 前帧之间的最小绝对值差。值越小，检测到的运动更多，但 false positive 的结果也会更多。 | n | 侦测到当前帧和平均帧 / 前帧之间的阈值增量达到 n 时，判定当前帧为“运动” |
| min_area          | 轮廓区域最小值，即令给定像素被判定为“运动”的、图像的最小区域面积（以像素为单位）。值越小，标注到更多运动区域的轮廓，具体大小可根据需要判定的物体调整。 | n | 侦测到运动的像素面积达到 n 时，判定该区域包含运动的物体 |

类似（例如从同一个摄像头获取）的视频可以使用相同的 .json 文件进行批处理。如果视频间差异太大，可能需要分别采用不同的 .json 文件以调整采集精度。

### 开始采集

在 video-capturer 目录下，打开命令提示符或 PowerShell。

* 正常采集：使用同目录下 conf.json 文件中的设置采集图像，采集过程中在终端显示所有输出。

  ```
  python start.py
  ```

* 静默采集：使用同目录下 conf.json 文件中的设置采集图像，采集过程中不在终端显示任何输出。

  ```
  pythow start.py
  ```

* 带参数采集：在命令行加入 --conf 或 -c 参数可以指定用其他 .json 文件中的设置采集图像。

  ```
  python start.py --c conf_2.json
  ```

  ```
  pythonw start.py --c conf_2.json
  ```

为防止因权限不足，无法创建文件或文件夹而中断采集过程，建议以管理员身份运行命令提示符或 PowerShell。

采集时，对弹出的三个窗口进行拖拽会使采集暂停，直至鼠标松开。

如果同时启用了静默采集和隐藏窗口选项，可以通过日志文件和 Windows 任务管理器中的 Python 进程确定采集进程。

### 中止采集

采集过程中，可以使用键盘快捷键中止过程：

* 按下 Q 键：中止全部采集
* 按下 S 键：跳过对当前视频的采集

## 查看结果

* 采集的图像：位于“output/视频名称__设置名称”目录下
* 视频信息：展示源视频的运动帧分（包括帧编号、时间码、全部轮廓和 min_area 轮廓），便于分析运动的分布和强度。包括 vinfo.csv 和 vinfo.png，位于“output/视频名称__设置名称”目录下
* 采集日志：如果设置了保存日志，位于 log/ 目录下

## 参考

本软件使用了以下开源代码：

* 多帧加权平均法基于 Adrian Rosebrock 在 PyImageSearch 的成果。
* 帧间差分法基于斩铁剑圣在知乎 Teamwork 专栏的成果。
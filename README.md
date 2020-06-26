# video-capturer
 从视频中捕捉包含运动的画面

## 最新版本

ver 200626.2326

新增功能：

* 在 GUI 版本中增加了清空待采集文件列表的按钮

已知问题：

* 在 GUI 版本中，启用日志记录会显著拖慢采集速度，强烈建议将 save_log 参数设置为 false

* 新的计算视频帧数的方法较原先缓慢，因此在采集每个视频之前，会有短暂的停顿

* 在 Windows 上使用 CMD 版本时，部分 H264 编码的视频在采集过程中会在终端频繁报错，不影响采集，但可能影响性能。

  错误信息：

  ```
  [NULL @ 00000230ac4d4a00] non-existing PPS 0 referenced
  ```

  变通办法：

  * 转换视频格式

  * 使用 GUI 版本的静默采集模式：

    ```
    pythonw vcgui.py
    ```
  
  * 使用 CMD 版本的静默采集模式：
  
    ```
    pythonw vccmd.py
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
| - [xiangzhenlu]   | 图像采集过程中用到的包 |        |        |
| - conf.json       | 图像采集的设置文件示例 | v      |        |
| - conf_2.json     | 图像采集的设置文件示例 | v      | v      |
| - README.md       | 软件说明文档           |        |        |
| - install.py      | 软件安装程序           |        |        |
| - vccmd.py        | 软件主程序（CMD 版本） |        |        |
| - vcgui.py        | 软件主程序（GUI 版本） |        |        |

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
   
   如果上述命令报错，请把 python 替换为 python3。

## 采集图像

可以使用命令行（CMD）版本或图形用户界面（GUI）版本之一的 video-capturer 进行采集。

### 使用命令行（CMD）版本

#### 1. 准备视频文件

支持的视频文件格式：.mp4, .avi, .mov, .mpeg, .flv, .wmv。

#### 2. 设置采集选项

video-capturer 使用 .json 文件规定采集图像过程中的设置，默认使用根目录下的 conf.json 文件。包括以下参数：

| 参数              | 描述                                                         | 值   | 描述         |
| ----------------- | --------------------------------------------- | ---- | --------------------------- |
| show_video        | 在采集图像时显示视频、阈值、帧增量三个窗口，禁用可以加快捕捉速度。    | true | 显示窗口 |
|  |  | false | 隐藏窗口 |
| save_annotations  | 保存带标记的图像，包括轮廓、视频播放时间、帧编号等信息。 | true | 保存带有标记的、宽度为 500 像素的图像 |
|  |  | false | 保存不带标记的、原始大小的图像 |
| save_log          | 保存本次采集的日志。日志将保存到 log/ 目录下、以本次采集开始时间命名的 .log 文件中。部分错误信息不会出现在日志中。 | true | 保存日志 |
|  |  | false | 不保存日志 |
| output_folder     | “输出”目录，即采集图像的保存位置，可以在本地、可移动介质或网络上，可以是相对路径（如 output/）或绝对路径（如 D:/）。 | "路径"，以 / 结尾 | 全部采集结果保存到路径下的“视频名称__设置名称”子文件夹中 |
| read_frames       | 视频文件的读法，即每几帧取一帧读。 | 1 | 按帧读取视频 |
|  |  | n | 每 n 帧取一帧读 |
| capture_type      | 图像的采集算法，包括多帧加权平均法、二帧差分法、三帧差分法。 | "avg" | 多帧加权平均法 |
|  |  | "two" | 二帧差分法 |
|  |  | "three" | 三帧差分法 |
| capture_images    | 图像的采集方式，包括应采尽采、采集多帧、采集多秒。该选项是一个数组，第一个参数规定侦测到运动时采集图像的方式，第二、三个参数规定相应数值（第三个值不存在时须填 0）。 | ["all", n, 0] | 应采尽采，每 n 帧取一帧保存 |
|  |  | ["frame", n, 0] | 采集 n 帧 |
|  |  | ["second", m, n] | 采集 m 秒，每 n 帧取一帧保存 |
| min_motion_frames | 运动帧最小值，即在图像保存到磁盘之前包含运动的连续帧的最小数量。值越小，保存的图像越多，但偶发运动的结果也会更多。 | n | 连续侦测到运动超过 n 帧，才保存这一批连续运动的图像 |
| min_delta_thresh  | 阈值增量最小值，即令给定像素被判定为“运动”的、当前帧和平均帧 / 前帧之间的最小绝对值差。值越小，检测到的运动更多，但 false positive （假相关）的结果也会更多。 | n | 侦测到当前帧和平均帧 / 前帧之间的阈值增量达到 n 时，判定当前帧为“运动” |
| min_area          | 轮廓区域最小值，即令给定像素被判定为“运动”的、图像的最小区域面积（以像素为单位）。值越小，标注到更多运动区域的轮廓，具体大小可根据需要判定的物体调整。 | n | 侦测到运动的像素面积达到 n 时，判定该区域包含运动的物体 |
| json_created | 此 .json 文件的创建时间。若要在其他地方使用此参数，请按照 YYYY-MM-DD HH:MM 的格式填写。 | "YYYY-MM-DD HH:MM" | 在此时间创建 |
| json_notes | 此 .json 文件的注释。 | "注释" |  |

彼此相似（例如从同一个摄像头获取、拍摄类似的物体）的视频可以使用相同的 .json 文件进行批处理。如果视频间差异太大，可能需要分别采用不同的 .json 文件以调整采集精度。

如果视频文件的输入位置位于可移动介质或网络上，采集速度将受到影响。

#### 3. 开始采集

在 video-capturer 目录下，打开命令提示符或 PowerShell。

在开始之前，需要了解采集命令的结构：

```
python vccmd.py -c <用户设置文件路径> -i <采集来源类型> -p <采集来源路径>
```

其中，有两个必需参数：

* -i 或 --input：可用值包括 files（单个文件）或 folder（单个文件夹）
* -p 或 --path：到单个文件或文件夹的路径

根据这些参数的排列组合，有如下几种采集模式：

* 正常采集：

  加载 conf.json 配置文件，采集单个文件

  ```
  python vccmd.py -i file -p example_01.mp4
  ```

  加载 conf.json 配置文件，采集整个目录

  ```
  python vccmd.py -i folder -p input/
  ```
  加载用户自定义的配置文件，采集单个文件
  
  ```
  python vccmd.py -c conf_2.json -i file -p example_01.mp4
  ```


* 静默采集：加载 conf.json 配置文件，采集单个文件

  ```
  pythonw vccmd.py -i file -p example_01.mp4
  ```

为防止因权限不足，无法创建文件或文件夹而中断采集过程，建议以管理员身份运行命令提示符或 PowerShell。

如果上述命令报错，请把 python 替换为 python3。

在某些情况下，采集时的以下操作将会使采集暂停：

* 对弹出的三个窗口进行拖拽。松开鼠标即可恢复采集。
* 在命令提示符或 PowerShell 窗口中单击。按 ESC 即可恢复采集。

如果同时启用了静默采集和隐藏窗口选项，可以通过日志文件和 Windows 任务管理器中的 Python 进程确定采集进程。

#### 4. 中止采集

采集过程中，可以使用键盘快捷键中止过程：

* 按下 Q 键：中止全部采集
* 按下 S 键：跳过对当前视频的采集

请注意：在 Windows 下，程序将监听全局的键盘按键。即，如果在其他程序中输入了以上两个按键，将触发相应操作。

### 使用图形用户界面（GUI）版本

#### 1. 准备视频文件

支持的视频文件格式：.mp4, .avi, .mov, .mpeg, .flv, .wmv。

#### 2. 打开程序

在 video-capturer 目录下，打开命令提示符或 PowerShell，输入

```
pythonw vcgui.py
```

待图形用户界面显示后，可以关闭打开的命令提示符或 PowerShell。

#### 3. 设置并开始采集

在窗口左侧，指定一种采集来源，并单击“选择”按钮添加相应的文件夹或文件。

在窗口右侧，指定要使用的 .json 设置文件，也可以新建设置文件。如果弹出了“错误”对话框，请按提示进行操作。单击“修改”链接可以调整每项采集设置，单击“保存修改”应用到 .json 设置文件和即将进行的采集。

当采集来源、.json 设置文件均设置好后，即可单击“开始采集”按钮进行采集。

采集过程中，将弹出进度指示窗口。采集完毕后，将弹出“采集完成”对话框。

#### 4. 中止采集

采集过程中，单击“停止采集”按钮停止全部采集，单击“跳过”链接跳过对当前视频的采集。

## 查看结果

* 采集的图像：位于“output/视频名称__设置名称”目录下
* 视频信息：展示源视频的运动帧分布信息（包括帧编号、时间码、全部轮廓和 min_area 轮廓），便于分析运动的分布和强度。包括 vinfo.csv 和 vinfo.png，位于“output/视频名称__设置名称”目录下
* 采集日志：如果设置了保存日志，位于 log/ 目录下

## 常见问题

问：采集的图像数量太多怎么办？

答：采集的图像数量多，常常与采集结果中 false positive 太多有关，具体请参见下一个问题。但是，如果仅仅希望降低采集图像的数量，可采用以下方法之一：

* 提高 read_frames 的 n 值
* 如果将 capture_images 设置为“all”，则提高 n 值
* 如果将 capture_images 设置为“frame”，则降低 n 值
* 如果将 capture_images 设置为“seconds”，则降低 m 值、提高 n 值
* 采用下一个问题中的方法（推荐）

问：采集的图像中，false positive 太多怎么办？

答：采集的图像 false positive 多，意味着采集的标准过于宽松。要增加结果的相关性，可采用以下方法之一：

* 提高 min_motion_frames 的 n 值
* 提高 min_delta_thresh 的 n 值（推荐）
* 提高 min_area 的 n 值

问：可以采集移动存储设备、局域网或网络上的视频文件吗？

答：可以，前提是这些位置须挂载到某一盘符（如 Z:/）下。如果视频文件的输入位置位于可移动介质或网络上，采集速度将受到影响。

## 参考

本软件使用了以下开源代码：

* 多帧加权平均法基于 Adrian Rosebrock 在 PyImageSearch 的成果。
* 帧间差分法基于斩铁剑圣在知乎 Teamwork 专栏的成果。
* 图形用户界面基于 tkinter 和 PAGE 构建。

## 更新历史

ver 200601.1350

新增功能：

* 在视频窗口上显示当前视频的估计剩余时间。

修复问题：

* 修复了在静默采集且隐藏窗口的设置下，不能正常采集的问题。

ver 200617.1311

新增功能：

* 现在可以在 .json 文件中使用 input_files 参数，指定待采集的某个或几个视频文件
* 现在可以在 .json 文件中加入创建时间和注释，便于更好管理不同的采集设置

修复问题：

* 优化了对不同平台上安装依赖包的支持

ver 200622.1157

新增功能：

* 增加了采集前的确认信息

ver 200625.2340

新增功能：

* 增加了图形用户界面（GUI）版本
* 调整了命令行（CMD）版本输入的参数

移除功能：

* 移除了 .json 文件中的 input_type, input_folder 和 input_files 参数，将在每次采集前指定

修复问题：

* 优化了对不同平台上安装依赖包的支持
* 修复了在“输入”文件夹中存在非图像文件时影响采集的问题
* 修改了计算视频帧数的方法，避免特定视频被错误计算，导致采集失败的问题
# RK3588 MediaPipe 手势识别

基于 MediaPipe 和 OpenCV 实现的实时手势识别项目，专为 **鲁班猫4（RK3588）** 开发板适配，通过 MIPI 摄像头进行实时手势检测与识别。

## 功能特性

- 实时手势识别，支持 MediaPipe 内置手势类别（如 Open_Palm、Closed_Fist、Pointing_Up、Thumb_Up 等）
- 支持同时识别最多 **2 只手**
- 实时绘制手部 21 个关键点及骨骼连接线
- 显示手势名称及置信度分数
- 适配鲁班猫4 MIPI 摄像头（`/dev/video11`），支持 1920×1080 分辨率输入

## 硬件要求

| 组件 | 规格 |
|------|------|
| 开发板 | 鲁班猫4（RK3588） |
| 摄像头 | MIPI 摄像头（挂载于 `/dev/video11`） |
| 系统 | Linux（推荐 Ubuntu / Debian） |

## 软件依赖

```bash
pip install mediapipe opencv-python numpy
```

> 建议使用 Python 3.8 及以上版本。

## 模型文件

项目使用两个 MediaPipe 模型文件：

| 文件名 | 用途 |
|--------|------|
| `gesture_recognizer.task` | 手势识别模型（float16） |
| `hand_landmarker.task` | 手部关键点检测模型 |

若模型文件不存在，程序会自动从 Google 服务器下载 `gesture_recognizer.task`。

## 快速开始

1. 克隆仓库：

```bash
git clone https://github.com/lixuboyc/rk3588-mediapipe.git
cd rk3588-mediapipe
```

2. 安装依赖：

```bash
pip install mediapipe opencv-python numpy
```

3. 运行程序：

```bash
python main.py
```

4. 按 `ESC` 键退出程序。

## 参数说明

可在 `main.py` 中修改以下配置：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `VIDEO_SOURCE` | `/dev/video11` | 摄像头设备节点 |
| 分辨率 | 1920×1080 | 输入帧分辨率 |
| `num_hands` | 2 | 最多识别的手数量 |
| `min_hand_detection_confidence` | 0.5 | 手部检测最低置信度 |
| `min_hand_presence_confidence` | 0.5 | 手部存在最低置信度 |
| `min_tracking_confidence` | 0.5 | 手部追踪最低置信度 |

## 效果说明

程序运行后将打开一个窗口，实时显示：

- 绿色圆点：手部 21 个关键点
- 绿色连线：手部骨骼连接
- 左上角文字：识别到的手势名称及置信度（格式：`手势名 (置信度)`）

## 目录结构

```
.
├── main.py                    # 主程序
├── gesture_recognizer.task    # 手势识别模型
├── hand_landmarker.task       # 手部关键点模型
└── README.md
```

## 参考资料

- [MediaPipe Gesture Recognizer](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
- [MediaPipe Hand Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
- [鲁班猫4 官方文档](https://wiki.lckfb.com/)

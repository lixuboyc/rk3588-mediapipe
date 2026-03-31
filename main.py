import sys
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
import numpy as np

# 下载模型文件（如果不存在）
import urllib.request
import os

# 手势识别模型
gesture_model_path = "gesture_recognizer.task"
if not os.path.exists(gesture_model_path):
    print("Downloading gesture recognizer model...")
    url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
    urllib.request.urlretrieve(url, gesture_model_path)
    print("Model downloaded!")

# 创建 GestureRecognizer
base_options = BaseOptions(model_asset_path=gesture_model_path)
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.GestureRecognizer.create_from_options(options)

# 视频输入配置：鲁班猫4 MIPI摄像头 (video11)
VIDEO_SOURCE = "/dev/video11"
print("Loading MIPI camera from:", VIDEO_SOURCE)
cap = cv2.VideoCapture(VIDEO_SOURCE, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Cannot open video file!")
    print("Please check if the file path is correct.")
    sys.exit(1)

# 获取视频信息
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Video loaded successfully!")
print("FPS: {}, Total frames: {}, Resolution: {}x{}".format(fps, frame_count, width, height))

frame_timestamp_ms = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    
    # Detect gestures
    results = detector.recognize_for_video(mp_image, frame_timestamp_ms)
    frame_timestamp_ms += 33  # 假设约30fps

    # Draw the hand annotations and gesture labels on the image
    if results.gestures:
        for i, (gesture_list, landmarks) in enumerate(zip(results.gestures, results.hand_landmarks)):
            # 获取最可能的手势
            if gesture_list:
                top_gesture = gesture_list[0]
                gesture_name = top_gesture.category_name
                gesture_score = top_gesture.score
                
                # 在图像上显示手势名称
                cv2.putText(image, "{} ({:.2f})".format(gesture_name, gesture_score), 
                           (10, 30 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制关键点
            for landmark in landmarks:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            
            # 绘制连接线
            connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
            for connection in connections:
                start_idx = connection.start
                end_idx = connection.end
                start_point = landmarks[start_idx]
                end_point = landmarks[end_idx]
                x1 = int(start_point.x * image.shape[1])
                y1 = int(start_point.y * image.shape[0])
                x2 = int(end_point.x * image.shape[1])
                y2 = int(end_point.y * image.shape[0])
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import os

def extract_frame(video_path, result_path):
    times=0
    #提取视频的频率，每25帧提取一个
    frameFrequency=100
    #输出图片到当前目录vedio文件夹下
    if not os.path.exists(result_path):
        os.makedirs(result_path) 
    camera = cv2.VideoCapture(video_path)
    while True:
        times+=1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times%frameFrequency==0:
            imgName = os.path.join(result_path, str(times))
            cv2.imwrite(imgName+'.jpg', image)
            print(result_path + str(times)+'.jpg')
    print('图片提取结束')
    camera.release()
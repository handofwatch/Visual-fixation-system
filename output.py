# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:40:03 2019

@author: lc
"""
import interface as i
import ReturnData as r

video_path='C:/Users/lc/Desktop/Cirtus/input/test.mp4'

i.analysis_for_video(video_path)


eye_path1='C:/Users/lc/Desktop/Cirtus/eyeData/left.txt'
eye_path2='C:/Users/lc/Desktop/Cirtus/eyeData/right.txt'

r.init(video_path,eye_path1,eye_path2)


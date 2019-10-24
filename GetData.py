# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:25:12 2019

@author: lc
"""
import os
import cv2
#根据左右眼导出眼动数据，以左眼为基础，右眼为补充
def getEyeData(eye_path1,eye_path2):
    fLeft=open(eye_path1)
    fRight=open(eye_path2)   
    line1 = fLeft.readline()   # 以行的形式进行读取文件
    list1 = []
    list2 = []
    while line1:           # 获取一组眼动数据中对应列的数据
        a = line1.split()
        x_l = a[2]   
        y_l = a[3]
        list1.append(x_l)  
        list2.append(y_l)
        line1 = fLeft.readline()

    list1.pop(0)         # 将列表第一个元素（即标签）删除
    list2.pop(0)

    
    line2 = fRight.readline()
    list3 = []
    list4 = []
    while line2: #获取另一组眼动数据中对应的注视点数据
        b = line2.split()
        x_r = b[2]
        y_r = b[3]
        list3.append(x_r)
        list4.append(y_r)
        line2 = fRight.readline()
        
    list3.pop(0) #删除标签
    list4.pop(0)

    list_x = []
    list_y = []
    i=0
    while i < len(list1):
        x = float(list1[i])
        y = float(list2[i])
        if i > 2:
            if x == 0:
                if y == 0: #补充缺少的数据
                    x = float(list3[i]) #延迟问题的处理==========================
                    y = float(list4[i])
        list_x.append(x) 
        list_y.append(y)
        i+=1
    return list_x , list_y , len(list_x)

"""
#单独导出屏幕眼动数据
def getEyeData(directory_name):
    fScreen = open(r"./"+directory_name)
    line = fScreen.readline()                 #按行读入数据
    list1=[]
    list2=[]
    while line:
        a=line.split()
        if len(a)>4:
            x=a[2]
            y=a[3]
            list1.append(x)
            list2.append(y)
        line = fScreen.readline()
    
    fScreen.close()
    list1.pop(0)#删除数据中的标识符元素
    list2.pop(0)
    
    list_x=[]
    list_y=[]
    i=0
    while i < len(list1):
        f_x = float(list1[i])               #类型转换
        i_x = int(f_x)                      #舍去小数点？？？待处理
        f_y = float(list2[i])
        i_y = int(f_y)
        list_x.append(i_x)
        list_y.append(i_y)
        i+=1
    #print (list_x)
    return list_x,list_y,len(list_x)                    #返回x，y坐标组成的list
"""

array_of_img = []
def getImgData(img_path):
    for filename in os.listdir(img_path):         #将图片的矩阵信息存储在list中
        img = cv2.imread(img_path + "/" + filename)
        height=img.shape[0]
        width=img.shape[1]
        array_of_img.append(img)
    #print(array_of_img)
    return array_of_img,len(array_of_img),height,width


def getTagData(directory_name):
    f = open(r"./"+directory_name)
    line = f.readline()
    codeList=[]
    tagList=[]
    while line:
        a=line.split()
        code=a[0]
        tag=a[1]
        codeList.append(code)
        tagList.append(tag)
        line=f.readline()

    f.close()
    codeList.pop(0)
    tagList.pop(0)
    
    colorList=[]
    for i in codeList:
        i=i.strip('#')
        colorList.append(i)
        
    #print(colorList)
    return colorList , tagList
    


























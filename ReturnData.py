# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 21:42:59 2019

@author: lc
"""
import GetData as g
import ModifyData as m

#全局变量
list_x = [] #眼动数据x坐标
list_y = [] #眼动数据y坐标
list_color = [] #ade20k数据集语义颜色
list_tag = [] #ade20k数据集语义颜色对应的标签名称
list_img = [] #图片矩阵组成的数组
current_dict = {} #当前一张图片的眼动数据统计
sum_dict = {} #整个视频的眼动数据统计
point_num = 0 #视频总注视点个数
img_num = 0 #视频分割的总图片数
img_height = 0 #图片的高度
img_width = 0 #图片的宽度
avg_point = 0 #每张图片对应的注视点个数
path1='C:/Users/lc/Desktop/Task1,2/input/test.mp4'
path2='C:/Users/lc/Desktop/Task1,2/eyeData/left.txt'
path3='C:/Users/lc/Desktop/Task1,2/eyeData/right.txt'
def init(video_path,eye_path1,eye_path2):
    global list_x,list_y,point_num,list_img,img_num,img_height,img_width,list_color,list_tag,avg_point
    #全局变量的声明
    a=video_path.split('/') #语义分割结果图片路径的处理
    img_path=a[0]
    count=1
    while count<len(a)-1:
        img_path=img_path+'/'+a[count]
        count+=1
    img_path=img_path+'/images/results'

    list_x,list_y,point_num = g.getEyeData(eye_path1,eye_path2)
    list_img,img_num,img_height,img_width = g.getImgData(img_path)
    list_color,list_tag = g.getTagData('tagData/tag.txt')
    
    list_x,list_y = m.modifyEyeData(list_x,list_y,point_num,img_height,img_width)
    avg_point = point_num/img_num
    i=0 #图片计数
    j=0 #眼动数据计数
    while i < img_num:
        frames=0
        while frames < avg_point:
            if j == point_num: break
            color = m.locate(list_x[j],list_y[j],list_img[i])
            tag = m.colorComp(color,list_color,list_tag)
            
            if tag == 'E':
                current_img=list_img[i]
                print(i,list_x[j],list_y[j],current_img[list_y[j],list_x[j]],color)                        # 有待处理错误数据？
                print( 'Error: the color is not in the dataset!')
            else:
                if list_x[j]!=img_width/2 and list_y[j]!=0:
                    m.count(tag,sum_dict)
                
            frames+=1
            j+=1
        i+=1
        
        
def findTag(x): #必须在调用函数init后才可使用  tag取值为[1,150] 建议用数字与ade20k中的name集合对应 
    #print(list_tag)
    tag = list_tag[x-1]
    if tag in sum_dict:
        return sum_dict[tag]
    else:
        return 0


def returnSum(): #必须在调用函数init后才可使用
    return sum_dict

def returnTag():
    return list_tag

def returnImgNum():
    return img_num

def findImg(x): #必须在调用函数init后才可使用  x取值为[1, len(list_img)]
    current_dict.clear()
    if len(list_img)==0:
        return 'Error: There is no Image to find'
    x-=1
    i=x*int(avg_point)
    while i < int(avg_point) * (x + 1):
        if i == len(list_x): break
        color = m.locate(list_x[i],list_y[i],list_img[x])
        tag = m.colorComp(color,list_color,list_tag)
        if tag == 'E':
            print(list_x[i],list_y[i],(list_img[x])[list_y[i],list_x[i]],color)
            print( 'Error: the color is not in the dataset!') #改成return终止操作，但是不知道如何改进这个问题。。。
        else:
            m.count(tag,current_dict)
        i+=1
    
    return current_dict
def clear(): #在下一批数据使用时调用，将数据清零，并删除之前的数据
    global list_x,list_y,point_num,list_img,img_num,list_color,list_tag,avg_point,current_dict
    list_x.clear()
    list_y.clear()
    point_num=0
    list_img.clear()
    img_num=0
    list_color.clear()
    list_tag.clear()
    avg_point=0
    sum_dict.clear()
    current_dict.clear()
    #清除图片数据和眼动数据
    #m.deleteData('imgData')
    #m.deleteData('eyeData')
    

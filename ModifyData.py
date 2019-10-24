# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 20:53:32 2019

@author: lc
"""
import os
def modifyEyeData(list1,list2,point_num,height,width):
    list_x=[]
    list_y=[]
    #num = 0
    i=0
    while i < point_num:
        x=int(list1[i]*width/768+width/2)
        y=int(list2[i]*height/288)
        list_x.append(x)
        list_y.append(y)
        """
        if x!=(width/2) and y!=0:
            list_x.append(x)
            list_y.append(y)
            num+=1
        """
        i+=1
    
    return list_x,list_y

def count(tag, consequence):
    if consequence.__contains__(tag):
        a=consequence.get(tag)
        a+=1
    else:
        a=1
    #print (tag)
    consequence[tag] = a
    return consequence

def locate(y, x, img):
    b=img[x,y,0]
    g=img[x,y,1]
    r=img[x,y,2]
    
    sb=str(hex(b))
    sg=str(hex(g))
    sr=str(hex(r))
    
    sb=sb.replace('0x','')
    sg=sg.replace('0x','')
    sr=sr.replace('0x','')
    
    if len(sb)==1:
        sb='0'+sb
    elif len(sg)==1:
        sg='0'+sg
    elif len(sr)==1:
        sr='0'+sr
        
    if len(sr)==0:
        color = '00'
    else: 
        color = sr
    
    if len(sg)==0:
        color = color + '00'
    else: 
        color = color + sg
    
    if len(sb)==0:
        color = color + '00'
    else: 
        color =color+sb
        
    color=color.upper()
    return color

def colorComp(color,colorList,tagList):
    i = 0
    tag = 'E'
    while i < len(colorList):
        if colorList[i] == color:
            tag=tagList[i]
            break
        i+=1
    #print (color)    
    return tag

def deleteData(directory_name):
    for filename in os.listdir(r"./"+directory_name):
        os.remove(directory_name+"/"+filename)
    
    
    
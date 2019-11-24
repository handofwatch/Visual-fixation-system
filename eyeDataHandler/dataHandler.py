import os
import cv2
from eyeDataHandler import getEyeData as g


# 当前模块的路径
base_dir = os.path.dirname(os.path.abspath(__file__))
# 截取的图片时间序列（从前面传进来）
img_time_list = [1.0, 7.7, 13.4]
# 生成语义分割好的图片的文件夹位置
result_pic_path = os.path.normpath(os.path.join(base_dir, "../output/images"))
# 左右眼数据位置
# left_eye_data_path = os.path.normpath(os.path.join(base_dir, "../eyeData/left.txt"))
# right_eye_data_path = os.path.normpath(os.path.join(base_dir, "../eyeData/right.txt"))
# 标签txt文件位置
tag_path = os.path.normpath(os.path.join(base_dir, "../tagData/tag.txt"))
# 允许的注视点一个时间间隔内的像素差，用于去除误差点
allow_delta = 20


# 提取分割后的图片
def read_result_imgs(result_path):
    img_list = []
    result_img_list = []
    for filename in os.listdir(result_path):
        if str(filename)[-2] == 'n':
            img = cv2.imread(result_path + "/" + filename)
            result_img_list.append(img)
        if str(filename)[-2] == 'p':
            img = cv2.imread(result_path + "/" + filename)
            img_list.append(img)
    return img_list, result_img_list


# 核心函数，输入时间序列，输出注释点的详细信息序列和注视点统计字典
def handle_result_img(img_time_list, left_eye_data_path, right_eye_data_path):
    point_time_list, points = g.align_two_eyes(left_eye_data_path, right_eye_data_path)
    points = g.wash_data(points, allow_delta)
    img_list, result_img_list = read_result_imgs(result_pic_path)
    print(img_list)
    tag_dict = get_color_dict(tag_path)
    points_detail = []
    result_dict = {}
    for i in range(len(img_time_list)):
        point_id = find_nearest_time(img_time_list[i], point_time_list)
        # 如果数据为空只能往下找，找到有效的为止
        while points[point_id] == [-1, -1]:
            point_id += 1
        point = points[point_id]
        height = result_img_list[i].shape[0]
        width = result_img_list[i].shape[1]
        result_img_list[i] = paint_point(result_img_list[i], [point[0], point[1]], 30, (0, 0, 255), 0.9)
        color = result_img_list[i][int(point[1]*height/288)][int(point[0]*width/768 + width/2)]
        hex_color = rgb2hex([color[2], color[1], color[0]])
        # 裁剪结果图片，取左半边
        result_img_list[i] = result_img_list[i][:, 0:int(width/2)]
        print(hex_color)
        if hex_color in tag_dict:
            tag = tag_dict[hex_color]
        else:
            tag = 0
        if tag in result_dict:
            result_dict[tag] += 1
        else:
            result_dict[tag] = 1
        # 每个注视点的详细信息，分别是重新排的序号、所处视频的时间、所处图片中的位置、颜色、标签名称
        point_detail = [i, img_time_list[i], int(point[0]*width/768), int(point[1]*height/288), hex_color, tag]
        points_detail.append(point_detail)
    return points_detail, result_dict, img_list, result_img_list


# 传入特定时间t和眼动数据时间轴序列，返回t对应的眼动数据位置（int）
def find_nearest_time(t, array):
    i = 0
    if array[len(array)-1] < t:
        print("image time is out of range")
    while array[i] < t:
        i += 1
    return i


# 在图片上画点
def paint_point(img, position, radius, color, alpha):
    img_copy = img[:]
    cv2.circle(img_copy, (int(position[0]), int(position[1])), radius, color, -1)
    img_new = cv2.addWeighted(img, alpha, img_copy, 1-alpha, 0)
    return img_new


# rgb转化为16进制码
def rgb2hex(rgb):
    hex = []
    for i in rgb:
        if i == 0:
            h = str(0) + str(0)
        else:
            h_left = int(i / 16)
            h_right = i % 16
            h = convert(h_left) + convert(h_right)

        hex.append(h)
    hex_combine = "#" + ''.join(hex)
    return hex_combine


# 十六进制
def convert(value):
    if value == 10:
        return "A"
    elif value == 11:
        return "B"
    elif value == 12:
        return "C"
    elif value == 13:
        return "D"
    elif value == 14:
        return "E"
    elif value == 15:
        return "F"
    return str(value)


# 通过tag_path，输出颜色-物品对应字典
def get_color_dict(tag_path):
    f = open(tag_path)
    line = f.readline()
    tag_dict = {}
    while line:
        a = line.split()
        color_code = a[0]
        tag = a[1]
        tag_dict[color_code] = tag
        line = f.readline()
    f.close()
    # 删掉非颜色的，比如第一行
    tag_dict = {k: v for k, v in tag_dict.items() if k[0] == '#'}
    return tag_dict


# 注视点点的详细信息，结果字典，原图片集，加了注视点的图片集
# points_detail, result_dict, img_list, result_img_list = handle_result_img(img_time_list, '/Users/engine/Desktop/Visual-fixation-system/eyeData/left.txt', '/Users/engine/Desktop/Visual-fixation-system/eyeData/right.txt')

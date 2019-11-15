# 从txt文件里提取数据，空数据标记为[-1, -1]，输入路径返回眼动时间轴和注视点位置数组
def read_eye_data(eye_data_path, eye):
    points_position = []
    time_array = []
    ff = open(eye_data_path)
    line = ff.readline()
    count = 0
    while line:
        row = line.split()
        if count == 0:
            print('Start Reading ' + eye + ' Eye Data...')
        else:
            point_position = [float(row[2]), float(row[3])]
            points_position.append(point_position)
            time_point = time2float(row[0])
            time_array.append(time_point)
        count += 1
        line = ff.readline()
    return time_array, points_position


# 对齐左右眼的数据（因为开始时间可能不一样，每一行的时间也有细微差别，以左眼的时间轴为准），返回标准眼动时间轴和左右平均化的注视点位置数组
def align_two_eyes(left_data_path, right_data_path):
    points = []
    left_time_array, left_points_array = read_eye_data(left_data_path, 'Left')
    right_time_array, right_points_array = read_eye_data(right_data_path, 'Right')
    i = 0
    # 对齐最前面的数据，有一只眼睛可能会缺数据，拿空数据补齐（误差时间在0.002之内，视为对齐）
    while abs(left_time_array[i] - right_time_array[i]) > 0.002:
        # 也就是说右边缺数据了
        if left_time_array[i] < right_time_array[i]:
            right_time_array.insert(i, left_time_array[i])
            right_points_array.insert(i, [0.0, 0.0])
        # 也就是说左边缺数据了
        else:
            left_time_array.insert(i, right_time_array[i])
            left_points_array.insert(i, [0.0, 0.0])
        i += 1
    # 以左眼时间轴和左眼数据为第一参考，左眼没有数据则参考右眼（不做平均是因为后面还有清洗）
    for j in range(len(left_time_array)):
        if left_points_array[j] == [0, 0] and right_points_array[j] == [0, 0]:
            point = [-1, -1]
        elif left_points_array[j] == [0, 0]:
            point = right_points_array[j]
        else:
            point = left_points_array[j]
        points.append(point)
    return left_time_array, points


# 把时间格式xx:xx:xx.xxx转化为以秒为单位的float
def time2float(time):
    store_time = time.split(':')
    if len(store_time) != 3:
        print("Wrong Time format")
        return 0
    else:
        return int(store_time[0])*3600 + int(store_time[1])*60 + float(store_time[2])


# 计算两个点的误差是否合理（衡量标准为定义的常量allow_delta）
def delta_between(point1, point2, allow_delta):
    if abs(point1[0]-point2[0]) < allow_delta and abs(point1[1]-point2[1]) < allow_delta:
        return True
    else:
        return False


# 辅助函数，获取x位置的下一个有效点的位置，如果超界就返回x本身
def get_next_avail_data(x, points):
    i = x
    while i < len(points):
        i += 1
        if points[i] != [-1, -1]:
            return i
    return x


# 辅助函数，获取x位置的上一个有效点的位置，如果超界就返回x本身
def get_former_avail_data(x, points):
    i = x
    while i > 0:
        i -= 1
        if points[i] != [-1, -1]:
            return i
    return x


# 清洗明显错误的数据
def wash_data(points, allow_delta):
    for i in range(1, len(points)-1):
        # 单个数据异常
        if delta_between(points[get_former_avail_data(i, points)], points[i], allow_delta) is False and delta_between(points[get_next_avail_data(i, points)], points[i], allow_delta) is False:
            points[i] = [-1, -1]
        # 连续错误数据清洗（待完成）
    return points

import cv2
import os


class ExtractPictures:

    def __init__(self):
        super(ExtractPictures, self).__init__()

    @staticmethod
    def video_frames(
                     path_in='',
                     path_out='',
                     only_output_video_info=False,
                     extract_time_points=None,
                     initial_extract_time=0,
                     end_extract_time=None,
                     extract_time_interval=-1,
                     output_prefix='extract',
                     jpg_quality=100,
                     ):
        cap = cv2.VideoCapture(path_in)
        frame_number = cap.get(7)  # 帧数
        rate = cap.get(5)  # 帧速率
        duration = frame_number/rate  # 单位s

        # 仅仅输出视频信息
        if only_output_video_info:
            _duration = str(duration)
            return _duration

        # 依据自定义时间点提取图片
        elif extract_time_points is not None:
            time_list = []
            if float(max(extract_time_points)) > duration:
                raise NameError('the max time point is larger than the video duration')
            try:
                os.mkdir(path_out)
            except OSError:
                pass
            success = True
            count = 0
            while success and count < len(extract_time_points):
                print("start extract the " + str(count + 1) + " image")
                time_list.append(extract_time_points)
                cap.set(cv2.CAP_PROP_POS_MSEC, (1000*extract_time_points[count]))
                success, image = cap.read()
                if success:
                    cv2.imwrite(os.path.join(path_out, "{}_{:06d}.jpg".format(output_prefix, count+1)), image,
                                [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                    count += 1
            return time_list

        # 自定义视频的起始位置提取图片
        else:
            if initial_extract_time > duration:
                raise NameError('initial extract time is larger than the video duration')
            if end_extract_time is not None:
                if end_extract_time > duration:
                    raise NameError('end extract time is larger than the video time')
                if initial_extract_time > end_extract_time:
                    raise NameError('initial time is larger than end time')

            # 以连续帧提取图片
            if extract_time_interval == -1:
                if initial_extract_time > 0:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time))
                try:
                    os.mkdir(path_out)
                except OSError:
                    pass
                if end_extract_time is not None:
                    time_list = []
                    number = (end_extract_time - initial_extract_time)*rate + 1
                    success = True
                    count = 0
                    while success and count < number:
                        print("start extract the " + str(count+1) + " image")
                        time = cap.get(0)

                        time_list.append(round(time/1000, 2))
                        success, image = cap.read()
                        if success:
                            cv2.imwrite(os.path.join(path_out, "{}_{:06d}.jpg".format(output_prefix, count + 1)), image,
                                        [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                            count += 1
                    return time_list

                # 如果开始或者结束时间为空就连续帧全部输出
                else:
                    time_list = []
                    success = True
                    count = 0
                    while success:
                        success, image = cap.read()
                        if success:
                            print("start extract the " + str(count + 1) + " image")
                            time = cap.get(0)
                            time_list.append(round(time/1000, 2))
                            cv2.imwrite(os.path.join(path_out, "{}_{:06d}.jpg".format(output_prefix, count + 1)), image,
                                        [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                            count += 1
                    return time_list

            # 在自定义起始范围内依照时间间隔提取图片
            elif 0 < extract_time_interval < 1/rate:
                raise NameError('extract_time_interval is less than the frame time interval')
            elif extract_time_interval > (frame_number/rate):
                raise NameError("extract_time_interval is larger than the duration of the video")

            else:
                try:
                    os.mkdir(path_out)
                except OSError:
                    pass
                if end_extract_time is not None:
                    time_list = []
                    number_ = (end_extract_time - initial_extract_time)/extract_time_interval + 1
                    success = True
                    count = 0
                    while success and count < number_:
                        print("start extract the " + str(count + 1) + " image")
                        cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time + count*1000*extract_time_interval))
                        success, image = cap.read()
                        time = cap.get(0)
                        if success:
                            cv2.imwrite(os.path.join(path_out, "{}_{:06d}.jpg".format(output_prefix, count + 1)), image,
                                        [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                            count += 1
                            # 浮点数四舍五入两位
                            time_list.append(round(time / 1000, 2))
                    return time_list
                # 如果开始或者结束时间为空就连续帧全部输出
                else:
                    print("间隔范围内全部输出")
                    time_list = []
                    success = True
                    count = 0
                    while success:
                        time = cap.get(0)
                        time_list.append(round(time/1000, 2))
                        success, image = cap.read()
                        if success:
                            print("start extract the " + str(count + 1) + " image")
                            cv2.imwrite(os.path.join(path_out, "{}_{:06d}.jpg".format(output_prefix, count + 1)), image,
                                        [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                            count += 1
                    return time_list

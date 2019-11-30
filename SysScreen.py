import os
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
from templates.UiBar import UiBar
from templates.UiPie import UiPie
from eyeDataHandler.dataHandler import handle_result_img
import extract.interface

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'secret string'


@app.route('/', methods=['GET', 'POST'])
def sys_screen():
    return render_template('MainScreen.html')


def ui_bar(name, data):

    _picture = UiBar()
    _picture.bar(name, data)


def ui_pie(name, data):

    _picture = UiPie()
    _picture.pie(name, data)


@app.route('/Result', methods=['POST'])
def picture():

    _id = request.form.get('formid')

    if request.method == 'POST':
        if _id == 'bar':
            return render_template('bar.html')

        if _id == 'pie':
            return render_template('pie.html')


#前端传入数据表单交由后端处理
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    result_sum = []
    if request.method == 'POST':
        #获得用户上传文件，并把他们放进服务器特定位置，并改为特定名字
        video_file = request.files['video']
        video_ext = video_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        r_data_file = request.files['rData']
        r_data_ext = r_data_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        l_data_file = request.files['lData']
        l_data_ext = l_data_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        video_path = os.path.join(file_dir, 'videoFile' + '.' + video_ext)
        video_file.save(video_path)#文件路径
        r_data_path = os.path.join(file_dir, 'rDataFile') + '.' + r_data_ext
        r_data_file.save(r_data_path)
        l_data_path = os.path.join(file_dir, 'lDataFile') + '.' + l_data_ext
        l_data_file.save(l_data_path)

        start_time = request.form.get("startTime")
        start_time = float(start_time)
        end_time = request.form.get("finishTime")
        end_time = float(end_time)
        interval = request.form.get("interval")
        interval = int(interval)

        name = []
        data = []
        point_dict = {}
        result_path = os.path.join(file_dir, "images")

        #将用户输入数字作为参数调用interface函数接口,得出time_list值，然后带入dataHandler中

        #拿到视频信息，一会儿后放在Result页面
        #video_infor = extract.interface.switch_case(1, file_dir, result_path)
        #print(video_infor)

        #得出time_list
        time_list = extract.interface.pass_input(start_time, end_time, interval, video_path, result_path)

        #分析图片
        #extract.interface.analysis(result_path)

        #调用第二组函数处理图片
        #result = handle_result_img(time_list, l_data_path, r_data_path)

        #test
        point_list = [[0, 0.0, 1219, 503, '#FF0652', 'table'], [1, 0.03, 1219, 503, '#FF0652', 'table']]

        result_sum = {'table': 2} #result[1]
        # resultSum = {'chair': 55, 'wall': 395, 'table': 441, 'box': 2,
        #              'person;individual;someone;somebody;mortal;soul': 6,
        #              'bag': 1, 'desk': 4, 'food;solid;food': 4, 'painting;picture': 4, 'book': 27}
        for i in result_sum:
            name.append(i)
            data.append(result_sum[i])
        ui_bar(name, data)
        ui_pie(name, data)

        return render_template('Result.html', point_infor=json.dumps(point_list))

    return render_template('MainScreen.html')


if __name__ == '__main__':
    app.run()



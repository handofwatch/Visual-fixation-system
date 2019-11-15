import os
from flask import Flask
from flask import render_template
from flask import request
from templates.UiBar import UiBar
from templates.UiPie import UiPie
from eyeDataHandler.dataHandler import handle_result_img
import extract.extract as e


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


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    result_sum = []
    if request.method == 'POST':
        video_file = request.files['video']
        video_ext = video_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        r_data_file = request.files['rData']
        r_data_ext = r_data_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        l_data_file = request.files['lData']
        l_data_ext = l_data_file.filename.rsplit('.', 1)[1]  # 获取文件后缀
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        video_path = os.path.join(file_dir, 'videoFile' + '.' + video_ext)
        video_file.save(video_path)
        r_data_file.save(os.path.join(file_dir, 'rDataFile') + '.' + r_data_ext)
        l_data_file.save(os.path.join(file_dir, 'lDataFile') + '.' + l_data_ext)
        name = []
        data = []
        confirm = request.get_json()
        result_path = os.path.join(os.path.dirname(video_file), "images")
        if confirm == '':
            time_list = e.ExtractPictures.video_frames(
                path_in=video_file,
                path_out=result_path,
                only_output_video_info=True,
                extract_time_points=None,
                initial_extract_time=0,
                end_extract_time=None,
                extract_time_interval=-1,
                output_prefix='extract',
                jpg_quality=100,
            )
            result_sum = handle_result_img(time_list, l_data_file, r_data_file)
        # resultSum = {'chair': 55, 'wall': 395, 'table': 441, 'box': 2,
        #              'person;individual;someone;somebody;mortal;soul': 6,
        #              'bag': 1, 'desk': 4, 'food;solid;food': 4, 'painting;picture': 4, 'book': 27}
        for i in result_sum:
            name.append(i)
            data.append(result_sum[i])
        ui_bar(name, data)
        ui_pie(name, data)
        return render_template('Result.html')

    return render_template('MainScreen.html')


if __name__ == '__main__':
    app.debug = True
    app.run()



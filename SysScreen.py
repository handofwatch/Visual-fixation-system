from flask import Flask
from flask import render_template
from flask import request
from templates.UiBar import UiBar
from templates.UiPie import UiPie
import os
from extract.interface import *

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'secret string'

@app.route('/', methods =['GET', 'POST'])
def sysScreen():
    return render_template('MainScreen.html')

def uibar(name, data):

    picture = UiBar()
    picture.bar(name, data)


def uipie(name, data):

    picture = UiPie()
    picture.pie(name, data)



@app.route('/Result', methods =['POST'])
def picture():

    id = request.form.get('formid')

    if request.method == 'POST':
        if id == 'bar':
            return render_template('bar.html')

        if id == 'pie':
            return render_template('pie.html')

@app.route('/uploadFile', methods =['POST'])
def uploadFile():
    if request.method == 'POST':
        videoFile = request.files['video']
        videoExt = videoFile.filename.rsplit('.', 1)[1]  # 获取文件后缀
        rDataFile = request.files['rData']
        rDataExt = rDataFile.filename.rsplit('.', 1)[1]
        lDataFile = request.files['lData']
        lDataExt = lDataFile.filename.rsplit('.', 1)[1]

        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        videoPath = os.path.join(file_dir, 'videoFile' + '.' + videoExt)
        videoFile.save(videoPath)
        rDataFile.save(os.path.join(file_dir, 'rDataFile' + '.' + rDataExt))
        lDataFile.save(os.path.join(file_dir, 'lDataFile' + '.' + lDataExt))
        name = []
        data = []


#请修改这里
        print(videoPath)
        analysis_for_video(videoPath)

        resultSum = {'chair': 55, 'wall': 395, 'table': 441, 'box': 2,
                     'person;individual;someone;somebody;mortal;soul': 6,
                     'bag': 1, 'desk': 4, 'food;solid;food': 4, 'painting;picture': 4, 'book': 27}
    #返回一个字典resultSum，当中注视点种类为键，注视点数量为值
        for i in resultSum:
            name.append(i)
            data.append(resultSum[i])
        uibar(name, data)
        uipie(name, data)

        return render_template('Result.html')

    return render_template('MainScreen.html')




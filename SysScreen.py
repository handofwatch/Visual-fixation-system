from flask import Flask
from flask import render_template
from flask import request
from templates.UiBar import UiBar
from templates.UiPie import UiPie
import interface as i
import ReturnData as r

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret string'

@app.route('/', methods =['GET', 'POST'])
def sysScreen():
    #form = request.form
    if request.method == 'POST' :
        # 调用后台接口实现数据传输
        # videoPath = '/Users/handofwatch/PycharmProjects/Visual_fixation_system/input/test.mp4'
        # rDataPath = '/Users/handofwatch/PycharmProjects/Visual_fixation_system/eyeData/right.txt'
        # lDataPath =
        # i.analysis_for_video(form.videoPath)
        # r.clear()
        # r.init(videoPath, lDataPath, rDataPath)
        # sum = r.returnSum()
        resultSum = {'chair': 55, 'wall': 395, 'table': 441, 'box': 2,  'person;individual;someone;somebody;mortal;soul': 6,
               'bag': 1, 'desk': 4, 'food;solid;food': 4, 'painting;picture': 4, 'book': 27}
        name = []
        data = []

        for i in resultSum:
            name.append(i)
            data.append(resultSum[i])
        uibar(name, data)
        uipie(name, data)
        return  render_template('Result.html')

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

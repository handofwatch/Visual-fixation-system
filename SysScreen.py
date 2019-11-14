from flask import Flask
from flask import render_template
from flask import request
from templates.UiBar import UiBar
from templates.UiPie import UiPie
import extract.interface as i
import csv


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret string'


@app.route('/', methods=['GET', 'POST'])
def sys_screen():
    name = []
    data = []
    if request.method == 'POST':
        with open('../output/rate.csv') as f:
            reader = csv.reader(f)
            print("====reader++++")
            print(reader)
            next(reader)
            for row in reader:
                name.append(row['name'])
            print(name)
            print(data)
        ui_bar(name, data)
        ui_pie(name, data)
        return render_template('Result.html')

    return render_template('MainScreen.html')


def ui_bar(name, data):

    _picture = UiBar()
    picture.bar(name, data)


def ui_pie(name, data):

    _picture = UiPie()
    picture.pie(name, data)


@app.route('/Result', methods =['POST'])
def picture():

    id = request.form.get('formid')

    if request.method == 'POST':
        if id == 'bar':
            return render_template('bar.html')

        if id == 'pie':
            return render_template('pie.html')


if __name__ == '__main__':
    app.debug = True
    app.run()

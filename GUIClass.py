from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from functools import partial
import extract.interface as i
import ReturnData as r
import os

def drawPieChart(data):
    pieSeries = QPieSeries()  # 定义PieSeries
    sum = 0
    for key in data:
        sum += data[key]

    for key in data:
        pieSeries.append(key, data[key])

    for slice in pieSeries.slices():
        labelStr = slice.label() + ":" + str(int(slice.value())) + "/" + str(int(100 * slice.value() / sum)) + "%"
        slice.setLabel(labelStr)

    pieSeries.setLabelsVisible()
    # slice = pieseries.slices()[0]  # 得到饼图的某一个元素切片，在这取得为第一个
    # slice.setExploded()  # 设置为exploded
    # slice.setLabelVisible()  # 设置Lable
    # slice.setPen(QPen(Qt.darkGreen, 1))  # 设置画笔类型
    # slice.setBrush(Qt.green)  # 设置笔刷

    pieChart = QChart()  # 定义QChart
    pieChart.addSeries(pieSeries)  # 将 pieseries添加到chart里
    pieChart.setTitle("视频分析结果——饼图")  # 设置char的标题
    pieChart.legend().hide()  # 将char的legend设置为隐藏
    pieChart.setAutoFillBackground(True)

    pieChartView = QChartView(pieChart)  # 定义charView窗口，添加chart元素，设置主窗口为父窗体，将chartView嵌入到父窗体
    pieChartView.setRenderHint(QPainter.Antialiasing)  # 设置抗锯齿

    return pieChartView


def drawBarChart(data):
    barSet = QBarSet("注视数值")
    barSeries = QBarSeries()
    axis = QBarCategoryAxis()  # 坐标轴
    for key in data:
        barSet.append(data[key])
        axis.append(key)

    barSeries.append(barSet)
    barSeries.setLabelsPosition(QAbstractBarSeries.LabelsInsideEnd)

    barSeries.setLabelsVisible()

    barChart = QChart()  # 定义QChart
    barChart.addSeries(barSeries)
    barChart.setTitle("统计结果——柱状图")
    barChart.createDefaultAxes()
    barChart.setAxisX(axis, barSeries)
    barChart.legend().hide()

    barChartView = QChartView(barChart)
    barChartView.setRenderHint(QPainter.Antialiasing)  # 设置抗锯齿
    return barChartView


class ChildWindow(QDialog):
    def __init__(self, dataPath):
        super(ChildWindow, self).__init__()
        self.resize(1600, 900)

        self.result = {"wall": 2, "building": 3, "edifice": 4, "sky": 5, "floor": 6, "flooring1": 7, "flooring2": 7,
                       "flooring3": 7, "flooring4": 7, "flooring5": 7, "flooring6": 7, "flooring7": 7, "flooring8": 7,
                       "flooring9": 7, "flooring0": 7, "flooring99": 7, "flooring999": 7, "flooring9999": 7, }


        self.frameNum = r. returnImgNum()  # 改成接口
        self.frameIndex = 0
        self.dataPath = dataPath

        # 展示统计图的窗口
        self.subWindow = QDialog()

        self.layout = QGridLayout()

        # 展示视频路径
        self.showPath = QLabel()
        self.showPath.setText("当前视频路径：")
        self.layout.addWidget(self.showPath, 0, 0, 1, 1)
        self.videoPathLabel = QLabel()
        self.videoPathLabel.setText(self.dataPath)
        self.layout.addWidget(self.videoPathLabel, 0, 1, 1, 4)

        '''
        从这里开始到函数最后是两段差不多功能的代码
        '''

        # 创建scrollarea，创建一个Widget
        self.scrollArea = QScrollArea()
        self.scrollGroupBox = QGroupBox()
        self.scrollGroupBox.setMinimumHeight(2000)

        # 为Widget设置layout，并生成展示的图片，并加入到layout里
        self.scrollLayout = QGridLayout()
        self.screenWidth = QApplication.desktop().screenGeometry().width()
        self.imgDirPath = os.path.join(os.path.dirname(self.dataPath), "images","results")
        self.imgList = os.listdir(self.imgDirPath)
        for i in range(0, len(self.imgList)):
            print(self.imgList[i])
            label = QLabel()
            label.setText(str(i))
            self.scrollLayout.addWidget(label, 2 * i, 0, 2, 1)
            # self.scrollLayout.addWidget(label)

            pix = QPixmap(self.imgDirPath + "/" + self.imgList[i])
            label = QLabel()
            label.setPixmap(pix)
            self.scrollLayout.addWidget(label, 2 * i, 1, 2, 5)


            button = QPushButton()
            button.setText("查看统计饼图")
            button.clicked.connect(partial(self.showFramePie, i))
            self.scrollLayout.addWidget(button, 2 * i, 6, 1, 2)
            # self.scrollLayout.addWidget(button)

            button = QPushButton()
            button.setText("查看统计柱状图")
            button.clicked.connect(partial(self.showFrameBar, i))
            self.scrollLayout.addWidget(button, 2 * i + 1, 6, 1, 2)
            # self.scrollLayout.addWidget(button)


        # 设置Widget的layout，并将Widget添加到滚动区，再将滚动区添加到layout
        self.scrollGroupBox.setMinimumHeight(self.frameNum * 400)
        self.scrollGroupBox.setMaximumWidth(int(self.screenWidth * 0.96))
        self.scrollGroupBox.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(self.scrollGroupBox)
        self.scrollArea.setWidgetResizable(True)
        self.layout.addWidget(self.scrollArea, 1, 0, 10, 9)

        # 设置整个子窗口的layout
        self.setLayout(self.layout)

        #
        # # 创建scrollarea，创建一个Widget
        # self.scrollArea = QScrollArea()
        # self.scrollWidget = QWidget()
        # self.scrollArea.setWidget(self.scrollWidget)
        # self.layout.addWidget(self.scrollArea, 1, 0, 10, 5)
        #
        # self.screenWidth = QApplication.desktop().screenGeometry().width()
        # for i in range(0, self.frameNum):
        #     label = QLabel(self.scrollWidget)
        #     label.setText(str(i))
        #     label.move(400 * i, 100)
        #     # self.scrollLayout.addWidget(label)
        #
        #     pix = QPixmap("f:/" + "1.jpg").scaled(800, 600)
        #     label = QLabel(self.scrollWidget)
        #     label.setPixmap(pix)
        #     label.move(400 * i, 300)
        #
        #     button = QPushButton(self.scrollWidget)
        #     button.setText("查看统计饼图")
        #     button.clicked.connect(partial(self.showFramePie, i))
        #     button.move(400 * i, 800)
        #     # self.scrollLayout.addWidget(button)
        #
        #     button = QPushButton(self.scrollWidget)
        #     button.setText("查看统计柱状图")
        #     button.clicked.connect(partial(self.showFrameBar, i))
        #     button.move(400 * i, 1000)
        #     # self.scrollLayout.addWidget(button)
        #
        # # 设置整个子窗口的layout
        # self.setLayout(self.layout)

    def showFramePie(self, i):
        self.result = r.findImg(i + 1)
        self.subWindow = chartWindow(drawPieChart(self.result))
        self.subWindow.showMaximized()
        print("饼图", i)

    def showFrameBar(self, i):
        self.result = r.findImg(i + 1)
        self.subWindow = chartWindow(drawBarChart(self.result))
        self.subWindow.showMaximized()
        print("柱状图", i)

class chartWindow(QDialog):
    def __init__(self, chartView):
        super(chartWindow, self).__init__()

        self.layout = QVBoxLayout()
        self.chartView = chartView
        self.layout.addWidget(self.chartView)
        self.setLayout(self.layout)



class MyMainWindow(QWidget):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.resize(1600, 900)
        # self.move(0, 0)

        # 子窗口
        self.childWindow = QDialog()
        self.pieChartWindow = QDialog()
        self.barChartWindow = QDialog()

        # 测试数据
        self.frames = ["f:/1.jpg", "f:/2.jpg", "f:/1.jpg", "f:/1.jpg", "f:/1.jpg"]
        self.result = {"wall": 2, "building": 3, "edifice": 4, "sky": 5, "floor": 6, "flooring1": 7, "flooring2": 7, "flooring3": 7, "flooring4": 7, "flooring5": 7, "flooring6": 7, "flooring7": 7, "flooring8": 7, "flooring9": 7, "flooring0": 7, "flooring99": 7, "flooring999": 7, "flooring9999": 7, }
        self.videoPath = ""
        self.leftEyeDataPath = ""
        self.rightEyeDataPath = ""

        self.layout = QGridLayout()

        # 用于展示视频统计结果的图和按钮
        self.pieChart = QChartView()
        self.barChart = QChartView()

        # 显示“请选择视频和眼动数据路径”的标签
        self.showNotification = QLabel()
        self.showNotification.setText("请选择视频和眼动数据路径")
        ft = QFont()
        ft.setPointSize(40)
        self.showNotification.setFont(ft)
        self.layout.addWidget(self.showNotification, 0, 0, 5, 12, Qt.AlignCenter)

        # 显示“视频路径”四个字
        self.showPath = QLabel()
        self.showPath.setText("当前视频路径：")
        self.layout.addWidget(self.showPath, 5, 1, 1, 1)

        # 展示选取的视频路径
        self.videoPathLabel = QLabel()
        self.videoPathLabel.setText("空")
        self.layout.addWidget(self.videoPathLabel, 5, 2, 1, 4)

        # 选取视频按钮
        self.selectButton = QPushButton()
        self.selectButton.setText("选取视频")
        self.selectButton.clicked.connect(self.selectVideo)
        self.layout.addWidget(self.selectButton, 5, 6, 1, 2)

        # 显示“左眼眼动数据”四个字
        self.showLeftEyeDataPath = QLabel()
        self.showLeftEyeDataPath.setText("左眼数据路径：")
        self.layout.addWidget(self.showLeftEyeDataPath, 6, 1, 1, 1)

        # 展示选取的左眼眼动数据路径
        self.leftEyeDataPathLabel = QLabel()
        self.leftEyeDataPathLabel.setText("空")
        self.layout.addWidget(self.leftEyeDataPathLabel, 6, 2, 1, 4)

        # 选取左眼眼动数据按钮
        self.selectLeftEyeDataButton = QPushButton()
        self.selectLeftEyeDataButton.setText("选取左眼数据")
        self.selectLeftEyeDataButton.clicked.connect(self.selectLeftEyeData)
        self.layout.addWidget(self.selectLeftEyeDataButton, 6, 6, 1, 2)

        # 显示“右眼眼动数据”四个字
        self.showRightEyeDataPath = QLabel()
        self.showRightEyeDataPath.setText("右眼数据路径：")
        self.layout.addWidget(self.showRightEyeDataPath, 7, 1, 1, 1)

        # 展示选取的右眼眼动数据路径
        self.rightEyeDataPathLabel = QLabel()
        self.rightEyeDataPathLabel.setText("空")
        self.layout.addWidget(self.rightEyeDataPathLabel, 7, 2, 1, 4)

        # 选取右眼眼动数据按钮
        self.selectRightEyeDataButton = QPushButton()
        self.selectRightEyeDataButton.setText("选取右眼数据")
        self.selectRightEyeDataButton.clicked.connect(self.selectRightEyeData)
        self.layout.addWidget(self.selectRightEyeDataButton, 7, 6, 1, 2)

        # 分析视频按钮
        self.analyseVideoButton = QPushButton()
        self.analyseVideoButton.setText("分析视频")
        self.analyseVideoButton.clicked.connect(self.analyseData)
        self.layout.addWidget(self.analyseVideoButton, 5, 8, 3, 2)
        self.analyseVideoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 展示每一帧按钮
        self.showDetailButton = QPushButton()
        self.showDetailButton.setText("展示每一帧")
        self.showDetailButton.clicked.connect(self.initSubWindow)
        self.layout.addWidget(self.showDetailButton, 5, 10, 1, 2)
        self.showDetailButton.hide()

        self.savePieImageButton = QPushButton()
        self.savePieImageButton.setText("查看饼图")
        self.savePieImageButton.clicked.connect(self.openPieChartWindow)
        self.layout.addWidget(self.savePieImageButton, 6, 10, 1, 2)
        self.savePieImageButton.hide()

        self.saveBarImageButton = QPushButton()
        self.saveBarImageButton.setText("查看柱状图")
        self.saveBarImageButton.clicked.connect(self.openBarChartWindow)
        self.layout.addWidget(self.saveBarImageButton, 7, 10, 1, 2)
        self.saveBarImageButton.hide()

        self.setLayout(self.layout)

    # 分析数据
    def analyseData(self):
        if self.leftEyeDataPath != "" and self.rightEyeDataPath != "" and self.videoPath != "":
            self.showNotification.setText("分析视频将花费较长时间，请稍等片刻")
            #调用后台接口实现数据传输
            i.analysis_for_video(self.videoPath)
            r.clear()
            r.init(self.videoPath,self.leftEyeDataPath,self.rightEyeDataPath)
            self.result=r.returnSum()
            # 在取得视频后显示截取的帧，展示统计图，展示切换统计图的按钮
            self.pieChart = drawPieChart(self.result)
            self.layout.addWidget(self.pieChart, 0, 0, 5, 6)
            self.barChart = drawBarChart(self.result)
            self.layout.addWidget(self.barChart, 0, 6, 5, 6)
            self.showDetailButton.show()
            self.savePieImageButton.show()
            self.saveBarImageButton.show()
            self.showNotification.hide()
            self.analyseVideoButton.setText("重新分析")
        else:
            pa = QPalette()
            pa.setColor(QPalette.WindowText, Qt.red)
            self.showNotification.setPalette(pa)
            self.showNotification.setText("请选择视频路径和眼动数据！")

    def initSubWindow(self):
        self.childWindow = ChildWindow(self.videoPath)
        self.childWindow.showMaximized()

    # 选择视频
    def selectVideo(self):
        # 选择文件
        fileName, filetype = QFileDialog.getOpenFileName(self, "选择视频", "/", "video files (*.mp4 *.avi)")
        # 不为空则设置文件路径
        if fileName != "":
            self.videoPath = fileName
            self.videoPathLabel.setText(fileName)


        '''
        print(fileName)  # 打印文件全部路径（包括文件名和后缀名）
        fileinfo = QFileInfo(fileName)
        print(fileinfo)  # 打印与系统相关的文件信息，包括文件的名字和在文件系统中位置，文件的访问权限，是否是目录或符合链接，等等。
        file_name = fileinfo.fileName()
        print(file_name)  # 打印文件名和后缀名
        file_suffix = fileinfo.suffix()
        print(file_suffix)  # 打印文件后缀名
        file_path = fileinfo.absolutePath()
        print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）

        选择多文件
        files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "/", "所有文件 (*);;文本文件 (*.txt)")
        print(files, ok1)  # 打印所选文件全部路径（包括文件名和后缀名）和文件类型

        保存文件
        fileName2, ok2 = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        print(fileName2)  # 打印保存文件的全部路径（包括文件名和后缀名）

        #选择文件夹
        # directory1 = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        # if directory1!=[]:
        #     print(directory1)  # 打印文件夹路径

        '''

    def selectLeftEyeData(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选择左眼数据", "/", "text files (*.txt)")
        # 不为空则设置文件路径
        if fileName != "":
            self.leftEyeDataPath = fileName
            self.leftEyeDataPathLabel.setText(fileName)

    def selectRightEyeData(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选择右眼数据", "/", "text files (*.txt)")
        # 不为空则设置文件路径
        if fileName != "":
            self.rightEyeDataPath = fileName
            self.rightEyeDataPathLabel.setText(fileName)

    def openPieChartWindow(self):
        self.pieChartWindow = chartWindow(drawPieChart(self.result))
        self.pieChartWindow.showMaximized()

    def openBarChartWindow(self):
        self.barChartWindow = chartWindow(drawBarChart(self.result))
        self.barChartWindow.showMaximized()

    def savePieImage(self):
        screen = QGuiApplication.primaryScreen()
        p = screen.grabWindow(self.pieChart.winId())
        image = p.toImage()
        savePath, fileType = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        print(savePath)  # 打印保存文件的全部路径（包括文件名和后缀名）
        image.save(savePath)


    def saveBarImage(self):
        screen = QGuiApplication.primaryScreen()
        p = screen.grabWindow(self.barChart.winId())
        image = p.toImage()
        savePath, fileType = QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        print(savePath)  # 打印保存文件的全部路径（包括文件名和后缀名）
        image.save(savePath)
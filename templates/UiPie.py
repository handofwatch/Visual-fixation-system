from pyecharts.charts import Pie

class UiPie:
    def pie(self, name, data):
        pie = Pie()
        pie.add("注视点数量饼状图", [(a,b) for a,b in zip(name, data)])
        pie.render(path="templates/pie.html")


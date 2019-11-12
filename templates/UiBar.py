from pyecharts.charts import Bar
from pyecharts import options as opts

class UiBar():

    def bar(self, name, data):

        bar = Bar()
        bar.add_xaxis(name)
        bar.add_yaxis("注视点数量", data)

        bar.set_global_opts(title_opts=opts.TitleOpts(title="注视点数量柱状图"))
        bar.render(path="templates/bar.html")

# -*- coding: utf-8 -*-
import os
import sys
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

def test():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    # output_file("lines.html", title="line plot example")

    # create a new plot with a title and axis labels
    p = figure(title=u"测试simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    # show(p)
    scr, div = components(p)
    print(scr)
    print(div)

if __name__=="__main__":
    test()

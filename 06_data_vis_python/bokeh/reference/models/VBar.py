import numpy as np

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, VBar

N = 9
x = np.linspace(-2, 2, N)
y = x**2

source = ColumnDataSource(dict(x=x,top=y))

plot = Plot(
    title=None, width=300, height=300,
    min_border=0, toolbar_location=None)

glyph = VBar(x="x", top="top", bottom=0, width=0.5, fill_color="#b3de69")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

curdoc().add_root(plot)

show(plot)

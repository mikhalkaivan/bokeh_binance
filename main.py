from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, NumeralTickFormatter
from bokeh.models.tools import RedoTool,RangeTool,UndoTool,EditTool,HelpTool,ResetTool,SaveTool,FreehandDrawTool,ZoomInTool,ZoomOutTool,WheelZoomTool,WheelPanTool
from bokeh.models.widgets import Dropdown, MultiSelect
from datetime import datetime
import math
import bn
import pandas as pd


SYMBOL_ONE = 'BTC'
SYMBOL_TWO = 'USDT'
PERIOD = '1 day ago UTC'
TIMEDELTA = '15m'

def get_data(symbol_1,symbol_2,interval,start):
    frame = bn.get_data(symbol_1,symbol_2,interval,start)
    times = []
    stringtimes = []
    raw_times = frame[0]
    open = frame[1]
    high = frame[2]
    low = frame[3]
    close = frame[4]
    for time in raw_times.unique():
        readable = datetime.fromtimestamp(int(time / 1000))
        times.append(readable)
        stringtimes.append(readable.strftime("%Y-%m-%d %H:%M:%S"))
    volumes = frame[5]
    data = dict(
        time = times,
        volume = volumes,
        stringtime = stringtimes,
        open = open,
        high = high,
        low = low,
        close = close
    )
    source = ColumnDataSource(data)
    return source


def get_plot_volume(source):
    hover = HoverTool(
        tooltips=[
            ('time', '@time{%Y-%m-%d %H:%M:%S}'),
            ('volume', '@volume{0.00 a}')
        ],
        formatters={'time':'datetime'},
        mode='vline'
    )
    p = figure(title="Cryptocurrencies volume trading", x_axis_label="Время", y_axis_label="Volume from",x_axis_type="datetime", plot_width=1000, plot_height=550)
    p.tools.append(hover)
    p.tools.append(RedoTool())
    p.tools.append(UndoTool())
    p.tools.append(ZoomOutTool())
    p.tools.append(ZoomInTool())
    p.tools.append(WheelPanTool())
    p.tools.append(WheelZoomTool())
    p.title.align = "center"
    p.title.text_font_size = "25px"
    p.yaxis.formatter = NumeralTickFormatter(format="0.00 a")
    p.xaxis.major_label_orientation = math.pi / 4
    p.line(x="time", y="volume", source=source, line_width=2, color="red", legend="volume trading")
    p.segment("time","high","time","low",color="black", source=source)
    return p


def update(attr,old,new):
    symbol_1 = dropdown_symbol_one.value
    symbol_2 = dropdown_symbol_two.value
    start = dropdown_histdata.value
    interval = dropdown_timedelta.value
    datasource = get_data(symbol_1,symbol_2,interval,start)
    source.data = datasource.data


dropdown_symbol_1 = [('Bitcoin','BTC'),('Etherium','ETH'),('Ripple','XRP')]
dropdown_symbol_one = Dropdown(label='Символ 1',button_type='success',menu=dropdown_symbol_1,value='BTC')
dropdown_symbol_2 = [('Dollar','USDT'),('Bitcoin','BTC')]
dropdown_symbol_two = Dropdown(label='Символ 2',button_type='success',menu=dropdown_symbol_2,value='USDT')
dropdown_hist = [('Месяц','1 month ago UTC'),('Неделя','7 day ago UTC'),('24 часа','24 hour ago UTC'),('12 часов','12 hour ago UTC'),('6 часов','6 hour ago UTC'),('1 час','1 hour ago UTC')]
dropdown_histdata = Dropdown(label='Временной масштаб', button_type='success',menu=dropdown_hist,value='24 hour ago UTC')
dropdown_delta = [('24 часа','24h'),('1 час','1h'),('15 минут','15m'),('5 минут','5min')]
dropdown_timedelta = Dropdown(label='Временной масштаб', button_type='success',menu=dropdown_delta,value='1h')

dropdowns = [dropdown_symbol_one, dropdown_symbol_two,dropdown_histdata,dropdown_timedelta]
for i in dropdowns:
    i.on_change('value', update)

source = get_data(SYMBOL_ONE,SYMBOL_TWO,TIMEDELTA,PERIOD)
plot_volumefrom = get_plot_volume(source)

widgets = column(dropdown_symbol_one,dropdown_symbol_two,dropdown_histdata,dropdown_timedelta)
image = column(plot_volumefrom)

curdoc().add_root(row(widgets,image))
curdoc().title = "Plot"

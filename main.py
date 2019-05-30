from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, NumeralTickFormatter
from bokeh.models.tools import RedoTool,RangeTool,UndoTool,EditTool,HelpTool,ResetTool,SaveTool,FreehandDrawTool,ZoomInTool,ZoomOutTool,WheelZoomTool,WheelPanTool
from bokeh.models.widgets import Dropdown, MultiSelect, TextInput
from datetime import datetime
import math
import bn
import pandas as pd


SYMBOL_ONE = 'BTC'
SYMBOL_TWO = 'USDT'
PERIOD = '1 day ago UTC'
TIMEDELTA = '1h'


def get_data_volume(symbol_1,symbol_2,interval,start):
    frame = bn.get_data(symbol_1,symbol_2,interval,start)
    times = []
    raw_times = frame[0]
    open = frame[1]
    high = frame[2]
    low = frame[3]
    close = frame[4]
    width = (raw_times[1] - raw_times[0])*0.8
    widths = []
    for time in raw_times.unique():
        readable = datetime.fromtimestamp(int(time / 1000))
        times.append(readable)
        widths.append(width)
    volumes = frame[5]
    data = dict(
        time = times,
        volume = volumes,
        open = open,
        high = high,
        low = low,
        close = close,
        raw_times = raw_times,
        widths = widths,
    )
    source = ColumnDataSource(data)
    return source


def get_data_price(symbol_1,symbol_2,interval,start):
    frame = bn.get_data(symbol_1, symbol_2, interval, start)
    raw_times = frame[0]
    open = frame[1]
    high = frame[2]
    low = frame[3]
    close = frame[4]
    width = (raw_times[1] - raw_times[0]) * 0.8
    times = []
    widths_desc = []
    widths_inc = []
    high_desc = []
    high_inc = []
    low_desc = []
    low_inc = []
    open_desc = []
    open_inc = []
    close_desc = []
    close_inc = []
    time_desc = []
    time_inc = []
    for time in raw_times.unique():
        readable = datetime.fromtimestamp(int(time / 1000))
        times.append(readable)
    for i in range(0,len(raw_times)):
        if open[i] > high[i]:
            widths_desc.append(width)
            high_desc.append(high[i])
            low_desc.append(low[i])
            open_desc.append(open[i])
            close_desc.append(close[i])
            time_desc.append(times[i])
        elif open[i] <= high[i]:
            widths_inc.append(width)
            high_inc.append(high[i])
            low_inc.append(low[i])
            open_inc.append(open[i])
            close_inc.append(close[i])
            time_inc.append(times[i])
    data = dict(
        widths_desc = widths_desc,
        widths_inc = widths_inc,
        high_desc = high_desc,
        high_inc = high_inc,
        low_desc = low_desc,
        low_inc = low_inc,
        open_desc = open_desc,
        open_inc = open_inc,
        close_desc = close_desc,
        close_inc = close_inc,
        time_desc = time_desc,
        time_inc = time_inc
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
    p = figure(title="График объемов продаж", x_axis_label="Время", y_axis_label="Объемы продаж",x_axis_type="datetime", plot_width=1000, plot_height=550)
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
    p.vbar("time", "widths", "volume", 0 , fill_color="navy", line_color="black", source=source, legend="Объемы продаж")
    return p


def get_plot_price(source):
    hover = HoverTool(
        tooltips=[
            ('time', '@time{%Y-%m-%d %H:%M:%S}'),
            ('open', '@open{0.00 a}'),
            ('close', '@close{0.00 a}'),
            ('high', '@high{0.00 a}'),
            ('low', '@low{0.00 a}'),
        ],
        formatters={'time': 'datetime'},
        mode='vline'
    )
    p = figure(title="График цены", x_axis_label="Время", y_axis_label="Цена",
               x_axis_type="datetime", plot_width=1000, plot_height=550)
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
    p.segment("time", "high", "time", "low", color="black", source=source)
    p.vbar('time', 'widths', 'open', 'close', fill_color="wheat", line_color="black", source=source,legend='Цена')
    return p


def update(attr,old,new):
    symbol_1 = dropdown_symbol_one.value
    symbol_2 = dropdown_symbol_two.value
    start = dropdown_histdata.value
    interval = dropdown_timedelta.value
    datasource = get_data_volume(symbol_1,symbol_2,interval,start)
    source.data = datasource.data
    text_symbol1.value = symbol_1
    text_symbol2.value = symbol_2
    text_period.value = start
    text_interval.value = interval


dropdown_symbol_1 = [('Bitcoin','BTC'),('Etherium','ETH'),('Ripple','XRP'),('Litecoin','LTC')]
dropdown_symbol_one = Dropdown(label='Символ 1',button_type='success',menu=dropdown_symbol_1,value='BTC')
dropdown_symbol_2 = [('Dollar, USDT','USDT'),('Dollar,USDC','USDC') ,('Bitcoin','BTC')]
dropdown_symbol_two = Dropdown(label='Символ 2',button_type='success',menu=dropdown_symbol_2,value='USDT')
dropdown_hist = [('Месяц','1 month ago UTC'),('Неделя','1 week ago UTC'),('24 часа','1 day ago UTC'),('12 часов','12 hours ago UTC'),('6 часов','6 hours ago UTC'),('1 час','1 hour ago UTC')]
dropdown_histdata = Dropdown(label='Временной отрезок', button_type='success',menu=dropdown_hist,value='1 day ago UTC')
dropdown_delta = [('24 часа','1d'),('1 час','1h'),('15 минут','15m'),('5 минут','5m'),('3 минуты','3m')]
dropdown_timedelta = Dropdown(label='Интервал', button_type='success',menu=dropdown_delta,value='1h')
text_symbol1 = TextInput(title='Символ 1:', value=SYMBOL_ONE)
text_symbol2 = TextInput(title='Символ 2:', value=SYMBOL_TWO)
text_period = TextInput(title='Временной интервал:', value=PERIOD)
text_interval = TextInput(title='Временной интервал:', value=TIMEDELTA)

dropdowns = [dropdown_symbol_one, dropdown_symbol_two,dropdown_histdata,dropdown_timedelta]
for i in dropdowns:
    i.on_change('value', update)

source = get_data_volume(SYMBOL_ONE,SYMBOL_TWO,TIMEDELTA,PERIOD)
plot_volumefrom = get_plot_volume(source)
plot_price = get_plot_price(source)

widgets = column(dropdown_symbol_one,dropdown_symbol_two,dropdown_histdata,dropdown_timedelta, text_symbol1,
                 text_symbol2,text_period,text_interval)
image = column(plot_volumefrom,plot_price)

curdoc().add_root(row(widgets,image))
curdoc().title = "Binance API plot"

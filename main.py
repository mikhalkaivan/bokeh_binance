from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, NumeralTickFormatter
from bokeh.models.tools import RedoTool,RangeTool,UndoTool,EditTool,HelpTool,ResetTool,SaveTool,FreehandDrawTool,PointDrawTool,ZoomInTool,ZoomOutTool,WheelZoomTool,WheelPanTool
from bokeh.models.widgets import Dropdown, MultiSelect
from datetime import datetime
import math
import bn


SYMBOL_ONE = 'BTC'
SYMBOL_TWO = 'USDT'
PERIOD = '1 day ago UTC'
TIMEDELTA = '1h'

def get_data(symbol_1,symbol_2,interval,start):
    frame = bn.get_data(symbol_1,symbol_2,interval,start)
    times = []
    raw_times = frame[0]
    for time in raw_times.unique():
        readable = datetime.fromtimestamp(int(time / 1000))
        times.append(readable)
    volumes = frame[7]
    data = dict(
        time = times,
        volume = volumes
    )
    source = ColumnDataSource(data)
    return source


def get_plot_volume(source):
    hover = HoverTool(
        tooltips=[
            ('time', '@date{"%Y-%m-%d %H:%M:%S"}'),
            ('volume', '@volume{0.00 a}')
        ],
        formatters={'time':'datetime'},
        mode='vline'
    )
    p = figure(title="Cryptocurrencies volume trading", x_axis_label="Время", y_axis_label="Volume from",x_axis_type="datetime", plot_width=600, plot_height=550)
    p.tools.append(hover)
    p.tools.append(RedoTool())
    p.tools.append(UndoTool())
    p.tools.append(PointDrawTool())
    p.tools.append(ZoomOutTool())
    p.tools.append(ZoomInTool())
    p.tools.append(WheelPanTool())
    p.tools.append(WheelZoomTool())
    p.title.align = "center"
    p.title.text_font_size = "25px"
    p.yaxis.formatter = NumeralTickFormatter(format="0.00 a")
    p.xaxis.formatter = DatetimeTickFormatter(
        minutes=['%Mm'],
        hours=['%Hh'],
        days=['%m/%d'],
        months=['%m/%Y'],
        years=['%Y']
    )
    p.xaxis.major_label_orientation = math.pi / 4
    line = p.line(x="time", y="volume", source=source, line_width=2, color="red", legend="volume trading")
    p.tools.append(FreehandDrawTool(renderers=[line]))
    return p


def update(attr,old,new):
    symbol_1 = dropdown_symbol_one.value
    symbol_2 = dropdown_symbol_two.value
    interval = dropdown_histdata.value
    start = dropdown_timedelta.value
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
image = column(row(plot_volumefrom))

curdoc().add_root(row(widgets,image))
curdoc().title = "Plot"

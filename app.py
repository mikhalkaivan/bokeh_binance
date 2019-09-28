from flask import Flask,render_template,request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE
import data


SYMBOL_ONE = 'BTC'
SYMBOL_TWO = 'USDT'
PERIOD = '1 day ago UTC'



app = Flask(__name__)


deltas = ['1h','15m','5m']
periodes = ['1 day ago UTC','1 hour ago UTC','30 min ago UTC']

def get_plot(x,y):
    p = figure(plot_width=500,plot_height=500)
    p.line(x=x,y=y)
    return p


@app.route('/')
def index():
    timedelta = request.args.get('t')
    period = request.args.get('p')
    if timedelta == None:
        timedelta = '1h'
    if period == None:
        period = '1 day ago UTC'
    d = data.get_data(SYMBOL_ONE,SYMBOL_TWO,timedelta,period)
    plot = get_plot(d[0],d[1])
    script,div = components(plot)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    html =  render_template('index.html',div=div,script=script,deltas=deltas,timedelta=timedelta,
                            js_resources=js_resources,css_resources=css_resources)
    return encode_utf8(html)


if __name__ == '__main__':
    app.run(debug=True)
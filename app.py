# getting libraries

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime,timedelta
import requests
import json
import pandas
from pandas import DataFrame, to_datetime
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import numpy as np
import time
import cgi
import os

## Function to do the actual thing
def output():
	# getting user set options from the index2.html page
        options = request.form.getlist('feature')
	stock = request.form['stock']
        stock = stock.upper()
        
        # requesting data from Quandl
        nw = datetime.now()
	start_date = (nw - timedelta(days=30)).strftime('%Y-%m-%d')
	end_date = nw.strftime('%Y-%m-%d')
	req_url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stock+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=3bkydVzcH_PPsy5zzAPn'
	r = requests.get(req_url)
        
        # pandas in action
	request_df = DataFrame(r.json()) 
	df = DataFrame(request_df.ix['data','dataset'], columns = request_df.ix['column_names','dataset'])
	df.columns = [x.lower() for x in df.columns]
	df = df.set_index(['date'])
	df.index = to_datetime(df.index)
	
	  
       
        # create plot - PLAY AROUND WITH THIS TO MAKE IT GENUINE
	#output_file("output.html", title="Stock prices changes for last month")
	p = figure(x_axis_type = "datetime")
	if 'open' in options:
	    p.line(df.index, df['open'], color='black', legend='Opening price')
	if 'high' in options:
	    p.line(df.index, df['high'], color='red', legend='Highest price')
	if 'close' in options:
	    p.line(df.index, df['close'], color='blue', legend='Closing price')
	return p

###############################################################################

app = Flask(__name__)


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index2.html')
      
     
  
@app.route('/output',methods=['GET','POST'])
def chart():
	plot = output()
	script, div = embed.components(plot)
	return render_template('output.html', script=script, div=div)
	
if __name__ == '__main__':
    #app.run(debug = True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


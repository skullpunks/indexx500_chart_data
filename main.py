from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

import pandas as pd 
import yfinance as yf 
from yahoo_fin.stock_info import get_data,get_live_price
from datetime import datetime

#origins = ["https://main--radiant-sawine-92fe28.netlify.app/"]
origins = ["https://in500.chart.indexx.ai/"]
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"], 
)


@app.get("/")
def index(period:str):
    print(period) 
    stock = yf.Ticker("^GSPC")
    data_frame = stock.history(period=period,interval="1h")
    columns = ["Open","High","Low","Close"]
    data_frame = pd.DataFrame(data_frame,columns=columns, index=data_frame.index)
    data_frame.reset_index(inplace=True) 
    
    if(period == '1d'):
        data_frame['period'] = data_frame['index'].dt.strftime("%I:%M %p")
    elif(period == '5d' or period == '1mo'):
        data_frame['period'] = data_frame['index'].dt.strftime("%b %d")
    elif(period == '6mo' or period == '1y'):
        data_frame['period'] = data_frame['index'].dt.strftime("%b %Y")
    
    data_close = data_frame['Close'].to_numpy()
    data_dates = data_frame['period'].to_numpy()   
    return {'date':list(data_dates), 'close':list(data_close)}


@app.get("/price")
def price_details():
    price =get_live_price("^GSPC")
    stock = yf.Ticker("^GSPC")
    data_frame = stock.history(period='1d',interval="1h")
    columns = ["Open","High","Low","Close"]
    data_frame = pd.DataFrame(data_frame,columns=columns, index=data_frame.index)
    data_frame.reset_index(inplace=True) 
    data_close = data_frame['Close'].to_numpy()
    data_high = data_frame['High'].to_numpy() 
    data_low = data_frame['Low'].to_numpy()
    data_open = data_frame['Open'].to_numpy() 

    now = datetime.now() 
    dt_string = now.strftime("%b %d, %H:%M: %p") 
    
    return  {'date':dt_string,'high':list(data_high)[0], 'close':list(data_close)[0], 'low':list(data_low)[0],'open':list(data_open)[0], 'price':price}

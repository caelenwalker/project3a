'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')

def call(symbol, chart_type, time_series, start_date, end_date):
    dateKeyList = []
    openValues = []
    highValues = []
    lowValues = []
    closeValues = []

    if chart_type == "1":
        chart = pygal.Bar()
    else:
        chart = pygal.Line()
    chart.title = 'Stock Data for ' + symbol + ': ' + str(start_date) + ' to ' + str(end_date)
    if time_series == "1":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval=60min&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    elif time_series == "2":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    elif time_series == "3":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+symbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+symbol+'&outputsize=full&apikey=TF2MH4AQ3EMH4GZL'
    r = requests.get(url)
    data = r.json()
    data.pop('Meta Data')
    dateList = data.values()
    for dictionary in dateList:
        for dateKey in dictionary:
            dateKey_dt = convert_date(dateKey)
            if dateKey_dt.day in range(start_date.day, end_date.day+1) and dateKey_dt.month in range(start_date.month, end_date.month+1) and dateKey_dt.year in range(start_date.year, end_date.year+1):
                dateKeyList.append(dateKey)
                openValues.append(float(dictionary[dateKey]['1. open']))
                highValues.append(float(dictionary[dateKey]['2. high']))
                lowValues.append(float(dictionary[dateKey]['3. low']))
                closeValues.append(float(dictionary[dateKey]['4. close']))
    dateKeyList.reverse()
    openValues.reverse()
    highValues.reverse()
    lowValues.reverse()
    closeValues.reverse()
    chart.x_labels = map(str, dateKeyList)
    chart.add('Open', openValues)
    chart.add('High', highValues)
    chart.add('Low', lowValues)
    chart.add('Close', closeValues)
    return 

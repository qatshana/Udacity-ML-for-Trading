'''
Generates dataframe for multiple tickers

input -- ticker.csv 

output -- dataframe with each output column representing one ticker 

'''

import pandas as pd
import matplotlib.pyplot as plt


def test_run():
	''' Scan through the symbols'''
	start_date='2010-01-22'
	end_date='2015-02-10'
	# generate date range
	dates=pd.date_range(start_date,end_date)	
	df=pd.DataFrame(index=dates)
	
	# gget spy data and organize it
	symbol='SPY'
	dfSPY=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])

	dfSPY=dfSPY.rename(columns={'Adj Close':'SPY'})	
	# joine the two sets
	df=df.join(dfSPY,how='inner') # with inner added, it allows you to remove nan

	symbols=['GOOG','AAPL','GLD','A']

	for symbol in symbols:
		dfTemp=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])

		dfTemp=dfTemp.rename(columns={'Adj Close':symbol})	
		# joine the two sets
		df=df.join(dfTemp,how='inner') # with inner added, it allows you to remove nan
	
	#print(df1)
	return df

def plot_stocks(df,title='Stock Prices'):
	''' plot stocks '''
	ax=df.plot(title=title,fontsize=2)
	ax.set_xlabel('Dates')
	ax.set_ylabel('Prices')
	plt.show()

def normalize_data(df):
	''' scale all prices to so we can have relative values '''	
	df=df/df.ix[0,:]
	return df

if __name__=="__main__":
	df=test_run()
	df=normalize_data(df)
	plot_stocks(df)
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

def get_stats(df):
	''' calculate the mean, median and std of stocks'''
	mean=df.mean()
	median=df.median()
	stdDev=df.std()
	return (mean,median,stdDev) 

def get_rolling_mean(df,symbol='SPY'):
	''' get rolling mean of a ticker '''
	rm=pd.rolling_mean(df[symbol],window=20)
	return rm

def get_rolling_std(df,symbol='SPY'):
	''' get rolling std a ticker '''
	std=pd.rolling_std(df[symbol],window=20)
	return std

def plot_rm(df,symbol,rm):
	''' plot rolling mean and stock price '''
	ax=df[symbol].plot(title='Rolling Mean',label='SPY')
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	rm.plot(label='SPY Rolling Mean',ax=ax)
	ax.legend(loc='upper left')
	plt.show()

def plot_Bolling(df,symbol,band1,band2):
	''' plot Bolling and stock price '''
	ax=df[symbol].plot(title='Bolling Bands',label='SPY')
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	band1.plot(label='SPY Band1',ax=ax)
	band2.plot(label='SPY Band2',ax=ax)
	ax.legend(loc='upper left')
	plt.show()
	


if __name__=="__main__":
	df=test_run()
	df=normalize_data(df)
	#plot_stocks(df)
	(dfmean,dfmedian,dfstd)=get_stats(df)
	print(dfmean)
	print(dfstd)
	rm=get_rolling_mean(df,'SPY')
	std=get_rolling_std(df,'SPY')
	#plot_rm(df,'SPY',rm)
	band1=rm-2*std
	band2=rm+2*std
	plot_Bolling(df,'SPY',band1,band2)
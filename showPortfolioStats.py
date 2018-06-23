'''
Get Perforamance of Portfolion based on allocation and tickers

input -- ticker.csv, allocation % and tickers 

output -- portfolio stats and plots

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_dataFrame(start_date,end_date,symbols):
	''' Scan through the symbols'''
	# generate date range
	dates=pd.date_range(start_date,end_date)	
	df=pd.DataFrame(index=dates)

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
	ax=df.plot(title=title)
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
	ax=df[symbol].plot(title='Bolling Bands',label=symbol)
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	band1.plot(label='SPY Band1',ax=ax)
	band2.plot(label='SPY Band2',ax=ax)
	ax.legend(loc='upper left')
	plt.show()
	

def compute_daily_return(df):
	'''' computes the daily returns for each column/ticker in dataframe '''
	df_returns=df/df.shift(1)-1
	return df_returns

def plot_daily_returns(df_returns,symbol):
	''' plot daily returns '''
	ax=df_returns[symbol].plot(label=symbol)
	ax.set_xlabel('Date')
	ax.set_ylabel('Returns')
	ax.legend(loc='upper left')
	plt.show()

def plot_hist(df_returns,symbol,bins=20):
	''' plot hist of returns '''
	mean=df_returns[symbol].mean()
	std=df_returns[symbol].std()
	kurtosis=df_returns[symbol].kurtosis()
	ax=df_returns[symbol].hist(bins=bins)
	plt.axvline(mean,color='r',linestyle='dashed',linewidth=2)
	plt.axvline(mean+std,color='g',linestyle='dashed',linewidth=2)
	plt.axvline(mean-std,color='g',linestyle='dashed',linewidth=2)
	plt.axhline(20,color='g',linestyle='dashed',linewidth=2)
	ax.set_xlabel('Returns')
	ax.set_ylabel('Frequency')
	ax.legend(loc='upper left')
	plt.show()

def plot_two_hist(df_returns,symbol1,symbol2,bins=20):
	''' plot hist of returns '''
	ax=df_returns[symbol1].hist(bins=bins,label=symbol1)
	df_returns[symbol2].hist(bins=bins,label=symbol2)
	ax.set_xlabel('Returns')
	ax.set_ylabel('Frequency')
	ax.legend(loc='upper left')
	plt.show()

def plot_scatter(df_returns,symbol1,symbol2):
	''' plot hist of returns '''
	ax=df_returns.plot(kind='scatter',x=symbol1,y=symbol2)
	beta,alpha=np.polyfit(df_returns[symbol1],df_returns[symbol2],1)
	print(alpha,beta)
	plt.plot(df_returns[symbol1],alpha+beta*df_returns[symbol1],'r-')
	ax.set_xlabel(symbol1)
	ax.set_ylabel(symbol2)
	ax.legend(loc='upper left')
	plt.show()

def get_corr(df_returns):
	''' Get correlation between returns'''
	return df_returns.corr(method='pearson')

if __name__=="__main__":
	# Set Portfolio Parameters
	start_date='2009-01-01'
	end_date='2011-12-31'	
	symbols=['SPY','XOM','GOOG','GLD']
	allocs=[0,0,1,0]
	start_val=1000000 # start with 1 m
	''' load stock prices'''
	df=load_dataFrame(start_date,end_date,symbols)
	''' normalize performance'''
	dfnormed=normalize_data(df)
	''' appy allocation to individual stocks'''
	dfalloced=allocs*dfnormed
	dfposs_val=dfalloced*start_val
	''' get total perfomance by day'''
	dfport_val=dfposs_val.sum(axis=1)
	''' compute daily returns on portfolio'''
	df_returns=compute_daily_return(dfport_val)
	df_daily_rets=df_returns[1:]
	''' Compute Portfolio Stats'''
	cum_ret=(dfport_val[-1]/dfport_val[0])-1
	avg_daily_ret=df_daily_rets.mean()
	std_daily_ret=df_daily_rets.std()
	rf_rate_ann=2.0/100
	rf_rate_daily=rf_rate_ann/365 # need to fix this formula
	sharpe_ratio=np.sqrt(252)*(avg_daily_ret-rf_rate_daily)/std_daily_ret
	#print(df_returns)
	print ('Cummulative returns %5.3f' %cum_ret)	
	print ('Shape ratio %5.3f' %sharpe_ratio)

	''' Show Results'''
	fig = plt.figure()

	# Divide the figure into a 2x1 grid, and give me the first section
	ax1 = fig.add_subplot(121)

	# Divide the figure into a 2x1 grid, and give me the second section
	ax2 = fig.add_subplot(122)
	dfport_val.plot(title='Portfolio Perf',ax=ax1,legend=True)
	ax1.set_ylabel('Value')
	ax1.set_xlabel('Date')
	

	dfnormed.plot(title='Stock Perf',ax=ax2,legend=True)
	
	#plt.legend(loc='uppder left')
	ax2.set_ylabel('Price')
	ax2.set_xlabel('Date')
	ax2.legend(loc='upper left')

	plt.show()

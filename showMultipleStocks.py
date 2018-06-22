import pandas as pd


def test_run():
	''' Scan through the symbols'''
	start_date='2010-01-22'
	end_date='2010-01-26'
	# generate date range
	dates=pd.date_range(start_date,end_date)	
	df1=pd.DataFrame(index=dates)
	
	# gget spy data and organize it
	symbol='SPY'
	dfSPY=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])
		
	# joine the two sets
	df1=df1.join(dfSPY)
	df1=df1.dropna()
	print(df1)

if __name__=="__main__":
	test_run()
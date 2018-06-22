import pandas as pd



def show_stock_max(symbol):
	'''
	read csv file and get max of close price
	'''
	df=pd.read_csv("data/{}.csv".format(symbol))
	return df['Close'].max()



def show_volume_mean(symbol):
	'''
	read csv file and get max of close price
	'''
	df=pd.read_csv("data/{}.csv".format(symbol))
	return df['Volume'].mean()


def test_run():
	''' Scan through the symbols'''
	symbols=['AAPL','IBM','A']
	print (symbols)
	for symbol in symbols:
		print('Stock with ticker %s has a max value of %3.1f' % (symbol,show_stock_max(symbol)))
		print('Stock with ticker %s has a volume mean of %3.1f' % (symbol,show_volume_mean(symbol)))

if __name__=="__main__":
	test_run()
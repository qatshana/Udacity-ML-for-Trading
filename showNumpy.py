'''
Generates numpy array


'''

import numpy as np


def test_run():
	''' Scan through the symbols'''
	print (np.array([(3,4,5),(6,7,8)]))

	''' create a normally distributed array with mean = 4 and std dev at 2 with 3X4'''
	a=np.random.normal(4,2,size=(3,4))
	print (a)
	''' Replace entire column 3 with below numbers'''
	a[:,3]=[10,20,40]
	print (a)
	''' fix the seed'''
	np.random.seed(1040)
	''' generate a 20 random integers between 1,10 '''
	b=np.random.randint(1,10,8)
	'''  use indices to access different elements in the array'''
	indices=np.array([1,3,5])
	print (b)
	print(b[indices])

	''' return value of array below mean'''

	data=np.random.random((3,5))
	print (data)

	print(data[data<np.mean(data)])



if __name__=="__main__":
	df=test_run()

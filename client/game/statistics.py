#copyright (c) 2011 savagerebirth.com
#this file provides VERY basic stats functions
#to be execmodded as statistics.py

def mean(X): #any iterable with numeric values
	#sample mean of course
	return sum(X)/len(X);

def sd(X): #any iterable with numeric values
	#this is the sample sd
	xbar = stats.mean(X);
	residualsquared = [(x - xbar)^2 for x in X];
	if len(X) != 0:
		s = sqrt(sum(residualsquared)/(len(X)-1));
	else:
		s = 0; #Well it's probably not defined in truth, but WHO CARES
	return s;

###########################################################################################
This project will query the Twitter API for a given number of handles, get the tweets
written by these handles within a given timeframe, and then perform a series of functions 
on the results to gain an understanding of how discourse has evolved in German politics in 
the last decade

The project is broken up into a number of different scripts:

1. twitter.py
	This script takes as input a given number of twitter handles and time-range and queries 
	Twitter API for the relevant tweets. These tweets are then parsed and stored as csv 
	files. This is done to minimize the number of queries made as the Twitter API has 
	strict monthly limits in the event the processing of the data needs to be fine-tuned 
	or run multiple times

	Each run is stored as 2 files, a csv and a cooresponding metadata file and 
	each file is timestamped. The files are named query_results-<timestamp>.csv and
	query_results-<timestamp>.md and are stored within a directory called Output. Each 
	is formatted as follows:

		CSV:
		handle,date,text
		<handle_1>,<date_1>,<text_1>

		MD:
		Time run: <time>
		Handles queried: [<handles>]
		Start time: <start_time>
		End time: <end_time>

	Currently, these values need to be updated by updating constant values at the top of 
	the file and once updated can be run with: 

		py twitter.py

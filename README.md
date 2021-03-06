## Description

This project will query the Twitter API for a given number of handles, get the tweets
written by these handles within a given timeframe, and then perform a series of functions 
on the results to gain an understanding of how discourse has evolved in German politics in 
the last decade

## Scripts

The project is broken up into a number of different scripts:

1. twitter.py

	This script takes as input a given number of twitter handles and time-range and queries 
	Twitter API for the relevant tweets. These tweets are then parsed and stored as csv 
	files. This is done to minimize the number of queries made as the Twitter API has 
	strict monthly limits in the event the processing of the data needs to be fine-tuned 
	or run multiple times

	Each run is stored as 2 files, a csv and a cooresponding metadata file and 
	each file is timestamped. The files are named query_results-{timestamp}.csv and
	query_results-{timestamp}.md and are stored within a directory called Output. Each 
	is formatted as follows:

		CSV:
		handle,date,text
		{handle_1},{date_1},{text_1}

		MD:
		Time run: {time}
		Handles queried: [{handles}]
		Start time: {start_time}
		End time: {end_time}

	Currently, these values need to be updated by updating constant values at the top of 
	the file and once updated can be run with: 

		py twitter.py

2. filter.py

	This script parses the file of full tweets and filters them out leaving only those 
	containing a word of interest. Both the file to filter and list of words of interest
	are stored as variables at the top of the script. This script outputs the results to 
	two files, query_results-{timestamp}-filtered.csv and query_results-{timestamp}-filtered.md.
	The files are formatted as follows:

		CSV:
		handle,date,tweet
		{handle_1},{date_1},{tweet_1}

		MD:
		File filtered: {file}
		Filter list: [{word_1}, {word_2}, ..., {word_n}]

	This script can be run with:

		py filter.py

3. tweet_count.py

	This script takes the tweets filtered by filter.py, and groups them by handle and
	month tweeted yielding a table that gives a count for how many tweets were tweeted
	by each account in each month. The results are saved as a file, tweet_count_results-{timestamp}.csv
	which is formatted as follows:

		CSV:
		handle,{MM/YYYY},tweet_count
		{handle_1},{date_1},{count_1}

	The script takes a file to count as a parameter as given by a variable at the top of the script and
	can be run via:

		py tweet_count.py

4. sentiment.py
	
	This script takes the filtered tweets as input and send requests for each to the Google
	Cloud Language API. This returns a magnitude and sentiment for each tweet a decription of 
	which can be found at: https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values

	This will output 2 files, a csv and a cooresponding metadata file each of which are timestamped.
	The files are named sentiment_results-{timestamp}.csv and sentiment_results-{timestamp}.md and 
	both are stored within a directory called Output. They are formatted as follows:

		CSV:
		handle,date,text,sentiment,magnitude
		{handle_1},{date_1},{text_1}

		MD:
		File: {file}

	The file to be processed is stored as a constant value at the top of the script and needs
	to be updated on each run. 

	Additionally, an environment variable needs to be set up before running the script which points to 
	the key needed to access the api. This key can be found at {path_to_project}/conf/{json_credential_file}.
	The variable can be set via:

		export GOOGLE_APPLICATION_CREDENTIALS="{path_to_project}/conf/{json_credential_file}"

	The script can then be run via:

		py sentiment.py

5. sentiment_average.py
	
	This script takes the output from the sentiment.py script and averages the results of 
	the each tweet score and magnitude value per month for each handle. The results from this
	are stored in an output file, sentiment_monthly_average-{timestamp}.csv. It is formatted as follows:

		CSV:
		handle,{MM/YYYY},tweet_count,average_sentiment,average_magnitude
		{handle_1},{date_1},{count_1},{avg_sentiment_1},{avg_magnitude_1}

	The file to be processed is stored as a constant value at the top of the script and needs
	to be updated on each run. 

	The script can then be run via:

		py sentiment_average.py

6. monthly_sentiemnt.py

	This script takes all of the tweets for each given handle, consolidates the text 
	of all of their tweets for each month, and then queries the sentiment analysis 
	for the combined text data. The goal of this is to give the sentiment analysis
	tooling more context for the tweets in generating a score and magnitude. The results
	from this script are stored in an output file, sentiment_monthly-{timestamp}.csv. 
	It is formatted as follows: 

		CSV:
		handle,{MM/YYYY},tweet_count,score,magnitude
		{handle_1},{date_1},{count_1},{score},{magnitude}

	The file to be processed is stored as a constant value at the top of the script and needs
	to be updated on each run. 

	Additionally, an environment variable needs to be set up before running the script which points to 
	the key needed to access the api. This key can be found at {path_to_project}/conf/{json_credential_file}.
	The variable can be set via:

		export GOOGLE_APPLICATION_CREDENTIALS="{path_to_project}/conf/{json_credential_file}"

	The script can then be run via:

		py monthly_sentiment.py

7. generate_sample.py

	This script filters through the full list of tweets, pulling out those that do not 
	contain a word of interest. It then goes through these filtered tweets and simply pulls
	out every 5th word to obtain a simple sample that is not representitive of the monthly
	distribution of the tweets. The list of tweets is stored in an output file, 
	random_sample-{timestamp}.csv and random_sample-{timestamp}.md which are formatted as follows:

		CSV:
		handle,date,tweet
		{handle_1},{date_1},{tweet_1}

		MD:
		File filtered: {file}
		Filter list: [{word_1}, {word_2}, ..., {word_n}]
		Percentage sampled: {sample_percent}%

## Setup

#### Environment

To run this you will first need to set up an environment to do so. You will need to install a number of pieces of software:
* Sublime Text Editor
	1. Download installer: https://www.sublimetext.com/3
		* download to C:\Program Files\Sublime Text 3\
	2. Add binary to system path
		1. Press the windows key
		2. Type "environment variables"
		3. Select "Edit the System Environment Variables"
		4. Click the "Environment Variables" button
		5. Under "System variables", double-click Path
		6. Add C:\Program Files\Sublime Text 3\ to the variable
* Git Bash
	1. Download installer: https://git-scm.com/download/win
	2. Run installer using recommended settings
* Python 3 
	1. Download installer: https://www.python.org/downloads/
	2. Run installer with recommended settings
		* Note: Make sure to check the option to add python to your path variable
	3. Open Git Bash and run "py --version" to ensure it is set up correctly 
* Code repo:
	1. Open Git Bash
	2. Type "cd ~" to go to your home area
	3. Type "mkdir IdeaProjects" to create a place to store the code
	4. Type "cd IdeaProjects" to move to this location
	5. Type "git clone https://github.com/ledigiacomo/AfD_research.git" to pull down the code
	6. Type "cd AfD_research" to go into its directory 
		* Typing "ls" should show you the scripts
		* You can open any of the scripts with: subl {script_name}.py

#### Update & Run
* If you followed the setup directions as above you can go to the code with the command: cd ~/IdeaProjects/AfD_research
* From here you can run "git pull" to pull down the latest version of the code
* Once this has completed you can run any python script with: py {script_name}.py
	* You can see the scripts in the repo by running: ls
	* You can open any of the scripts with: subl {script_name}.py


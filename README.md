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

## Setup

#### Environment

To run this you will first need to set up an environment to do so. You will need to install a number of pieces of software:
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
	7. Typing "ls" should show you the scripts

#### Update & Run
* If you followed the setup directions as above you can go to the code with the command: cd ~/IdeaProjects/AfD_research
* From here you can run "git pull" to pull down the latest version of the code
* Once this has completed you can run any python script with: py {script_name}.py
	* You can see the scripts in the repo by running: ls


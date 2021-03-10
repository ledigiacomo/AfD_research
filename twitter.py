import requests
import os
import json
import sys
import time
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
os.environ["BEARER_TOKEN"] = "AAAAAAAAAAAAAAAAAAAAALwMNAEAAAAAmr6bGyd7snmMMv9P4emshCjSsnc%3DAhCJiRgxZGYtEpCSfOyLnBvF9HZ5K0BY3XtgHmYpBDSsqnCw8Q"
bearer_token = os.environ.get("BEARER_TOKEN")

# Constants:
OUTPUT_DIR = "./Output/"
START_TIME = "2015-01-01T00:00:00Z"
END_TIME = "2017-12-31T23:59:59Z"
search_url = "https://api.twitter.com/2/tweets/search/all"
handles = [
    "Tino_Chrupalla",
    "JoanaCotar",
    "GottfriedCurio",
    "DrMEspendiller",
    "PeterFelser",
    "Martin_Hess_AfD",
    "Marc_Jongen",
    "MdB_Lucassen",
    "Schneider_AfD",
    "Rene_Springer",
    "Alice_Weidel"
]

# Function to print unrecognized Unicode characters
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# Sends the request to the Twitter API
def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        # Too many requests, wait 1 minute and try again
        if response.status_code == 429:
            time.sleep(60)
            connect_to_endpoint(url, headers, params)
        else:
            raise Exception(response.status_code, response.text)
    return response.status_code, response.json()

# Creates the request for the Twitter API
def query_search_endpoint(handle, next_token):
    headers = create_headers(bearer_token)
    query_params = {'query': '(from:' + handle + ')', 'start_time': START_TIME, 'end_time': END_TIME, 'tweet.fields': 'created_at', 'max_results': 100}
    if next_token:
        query_params["next_token"] = next_token
       
    status, json_response = connect_to_endpoint(search_url, headers, query_params)
    return status, json_response

# Parses the API response and formats the results into a csv format
#
# The information parsed from the response are the handle, date the tweet was posted, and text of the tweet
def parseResponse(handle, response):
    lines = []

    data = response.get("data")
    if not data:
        print("No data found for %s" % handle)
        return ""

    for tweet in data:
        line = "%s,%s,%s" % (handle, tweet["created_at"], tweet["text"].replace('\n', "").replace(",", ""))
        lines.append(line)

    return "\n".join(lines)

def writeCsvResults(timestamp, results):
    with open("%squery_results-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
        file.write(results)

def writeMdResults(timestamp):
    with open("%squery_results-%s.md" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
        file.write("Handles queried: [%s]\n" % ",".join(handles))
        file.write("Start time: %s\n" % START_TIME)
        file.write("End time: %s\n" % END_TIME)

# Creates the csv and MD files with the results of a run
# 
# The files are named query_results-<timestamp>.csv and query_results-<timestamp>.md
def writeResults(results):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

    writeCsvResults(timestamp, results)
    writeMdResults(timestamp)

#################################################################################################
# This is the main body of the script. The basic flow is as follows:
# 1. Get a handle from the supplied list
# 2. Ask twitter for the tweets from the handle within the date range
# 3. If the results were paginated repeat the request asking for the next page
#
# Pagination: In order to keep the requests from getting too big and breaking their system,
# Twitter will return the tweets in groups of up to 100 with a next_token value. Once you have 
# finished processing this group, you need to resend the request with next_token as a parameter 
# to get the results. 
def main():
    csvString = "handle,date,text\n"

    for handle in handles: # Go through each handle in thelist
        status, response = query_search_endpoint(handle, None) # Query Twitter API for handle's tweets

        if status == 200:
            csvString += parseResponse(handle, response) + "\n" # Parse and store the results

        while "meta" in response and "next_token" in response["meta"]: #If there are more results ask for them
            time.sleep(1) # Rate limit on API of 1 request/sec
    
            status, response = query_search_endpoint(handle, response["meta"]["next_token"])
            if status == 200:
                csvString += parseResponse(handle, response) + "\n" # Parse and store the results
            
    writeResults(csvString) # Create the csv and md files with the results

if __name__ == "__main__":
    main()
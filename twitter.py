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

def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.status_code, response.json()

def query_search_endpoint(handle, next_token):
    headers = create_headers(bearer_token)
    query_params = {'query': '(from:' + handle + ')', 'start_time': START_TIME, 'end_time': END_TIME, 'tweet.fields': 'created_at'}
    if next_token:
        query_params["next_token"] = next_token
       
    status, json_response = connect_to_endpoint(search_url, headers, query_params)
    return status, json_response

def parseResponse(handle, response):
    lines = []

    data = response.get("data")
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

def writeResults(results):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%SZ')

    writeCsvResults(timestamp, results)
    writeMdResults(timestamp)

def main():
    csvString = "handle,date,text\n"

    # for handle in handles:
    status, response = query_search_endpoint(handles[0], None)

    if status == 200:
        csvString += parseResponse(handles[0], response) + "\n"

    while "next_token" in response["meta"]:
        # Rate limit on API of 1 request/sec
        time.sleep(1)

        status, response = query_search_endpoint(handles[0], response["meta"]["next_token"])
        if status == 200:
            csvString += parseResponse(handles[0], response) + "\n"
        
    uprint(csvString)
    writeResults(csvString)

if __name__ == "__main__":
    main()
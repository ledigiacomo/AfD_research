from google.cloud import language_v1
from google.cloud import storage
import sys
import time
import datetime

OUTPUT_DIR = "./Output/"

SAMPLE = True

if SAMPLE:
    TWEET_FILE = "./Output/random_sample-2021-05-09T15-10-40Z.csv"
else:
	TWEET_FILE = "./Output/query_results-2021-05-07T18-56-57Z-filtered.csv"

# Function to print unrecognized Unicode characters
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def combineTweets(tweets):
	tweetsByMonth = {}
	for tweetData in tweets:
		if len(tweetData.split(",")) is 3:
			handle = tweetData.split(",")[0]
			date = tweetData.split(",")[1]
			tweet = tweetData.split(",")[2]
	
			month = str(date.split("T")[0].split("-")[1])
			year = str(date.split("T")[0].split("-")[0])

			monthYear = month + "/" + year
	
			if handle not in tweetsByMonth:
				tweetsByMonth[handle] = {}
	
			if monthYear not in tweetsByMonth[handle]:
				tweetsByMonth[handle][monthYear] = {}
				tweetsByMonth[handle][monthYear]["count"] = 0
				tweetsByMonth[handle][monthYear]["text"] = []
	
			tweetsByMonth[handle][monthYear]["count"] = tweetsByMonth[handle][monthYear]["count"] + 1
			tweetsByMonth[handle][monthYear]["text"].append(tweet)

	return tweetsByMonth

"""
    Analyzing Sentiment in a String
    
    Args:
      text_content The text content to analyze
"""
def analyze_sentiment(text_content):
    client = language_v1.LanguageServiceClient()

    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "de"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    return response.document_sentiment.score, response.document_sentiment.magnitude

def analyze(tweetsByMonth):
    analysis = ["handle,month,tweet_count,score,magnitude"]
    for handle in tweetsByMonth:
    	for monthYear in tweetsByMonth[handle]:
            text = "\n\n".join(tweetsByMonth[handle][monthYear]["text"])
            score, magnitude = analyze_sentiment(text)

            analysis.append(",".join([handle, monthYear, str(tweetsByMonth[handle][monthYear]["count"]), str(score), str(magnitude)]))

    return analysis

def writeResults(results):
	timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

	if SAMPLE:
		with open("%ssentiment_monthly-SAMPLE-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
			file.write("\n".join(results))
	else:
		with open("%ssentiment_monthly-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
			file.write("\n".join(results))

def main():
	with open(TWEET_FILE, encoding="utf-8") as f:
		results = f.read().splitlines()
		print("Found %d tweets to analyze" % len(results))

		tweetsByMonth = combineTweets(results[1:])

		analysis = analyze(tweetsByMonth)

		writeResults(analysis)

if __name__ == "__main__":
	main()
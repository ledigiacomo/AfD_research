from google.cloud import language_v1
from google.cloud import storage
import sys
import time
import datetime

OUTPUT_DIR = "./Output/"
SAMPLE = True

if SAMPLE:
    TWEET_FILE = "./Output/random_sample-2021-05-10T15-08-09Z.csv"
else:
    TWEET_FILE = "./Output/query_results-2021-05-10T14-15-58Z-filtered.csv"

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

def analyzeIndividual(results):
    analysis = ["handle,date,tweet,score,magnitude"]
    for result in results:
        if len(result.split(",")) is 3:
            handle = result.split(",")[0]
            date = result.split(",")[1]
            tweet = result.split(",")[2]

            score, magnitude = analyze_sentiment(tweet)

            analysis.append(",".join([handle, date, tweet, str(score), str(magnitude)]))

    return analysis

def writeCsvResults(timestamp, analysis):
    if SAMPLE:
        with open("%ssentiment_results-SAMPLE-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
            file.write("\n".join(analysis))
    else:
        with open("%ssentiment_results-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
            file.write("\n".join(analysis))

def writeMdResults(timestamp):
    if SAMPLE:
        with open("%ssentiment_results-SAMPLE-%s.md" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
            file.write("File: %s\n" % TWEET_FILE)
    else:
        with open("%ssentiment_results-%s.md" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
            file.write("File: %s\n" % TWEET_FILE)

def writeResults(analysis):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

    writeCsvResults(timestamp, analysis)
    writeMdResults(timestamp)

def main():
    with open(TWEET_FILE, encoding="utf-8") as f:
        results = f.read().splitlines()
        print("Found %d tweets to analyze" % len(results))

        analysis = analyzeIndividual(results[1:])

        writeResults(analysis)

if __name__ == "__main__":
    main()
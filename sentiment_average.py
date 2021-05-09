import sys
import time
import datetime

OUTPUT_DIR = "./Output/"

SAMPLE = True

if SAMPLE:
    SENTIMENT_FILE = "./Output/sentiment_results-SAMPLE-2021-05-09T16-43-11Z.csv"
else:
	SENTIMENT_FILE = "./Output/sentiment_results-2021-05-08T00-12-36Z.csv"

# Function to print unrecognized Unicode characters
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def analyzeResults(results):
	analysis = {}
	for result in results:
		if len(result.split(",")) is 5:
			handle = result.split(",")[0]
			date = result.split(",")[1]
			tweet = result.split(",")[2]
			score = float(result.split(",")[3])
			magnitude = float(result.split(",")[4])
	
			month = str(date.split("T")[0].split("-")[1])
			year = str(date.split("T")[0].split("-")[0])

			monthYear = month + "/" + year
	
			if handle not in analysis:
				analysis[handle] = {}
	
			if monthYear not in analysis[handle]:
				analysis[handle][monthYear] = {}
				analysis[handle][monthYear]["count"] = 0
				analysis[handle][monthYear]["score"] = 0
				analysis[handle][monthYear]["magnitude"] = 0

	
			analysis[handle][monthYear]["count"] = analysis[handle][monthYear]["count"] + 1
			analysis[handle][monthYear]["score"] = analysis[handle][monthYear]["score"] + score
			analysis[handle][monthYear]["magnitude"] = analysis[handle][monthYear]["magnitude"] + magnitude

	return analysis

def writeResults(results):
	lines = []
	lines.append("handle,month,tweet_count,average_score,average_magnitude")

	for handle in results:
		for monthYear in results[handle]:
			count = results[handle][monthYear]["count"]
			average_score = results[handle][monthYear]["score"] / results[handle][monthYear]["count"]
			average_magnitude = results[handle][monthYear]["magnitude"] / results[handle][monthYear]["count"]

			lines.append("%s,%s,%s,%s,%s" % (handle, monthYear, count, average_score, average_magnitude))

	timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

	if SAMPLE:
		with open("%ssentiment_monthly_averages-SAMPLE-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
			file.write("\n".join(lines))
	else:
		with open("%ssentiment_monthly_averages-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
			file.write("\n".join(lines))

def main():
	with open(SENTIMENT_FILE, encoding="utf-8") as f:
		results = f.read().splitlines()
		print("Found %d tweets with sentiments to analyze" % len(results))

		analysis = analyzeResults(results[1:])

		writeResults(analysis)

if __name__ == "__main__":
	main()
import sys
import time
import datetime

OUTPUT_DIR = "./Output/"
TWEET_FILE = "./Output/query_results-2021-03-17T20-06-40Z-filtered.csv"

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
		if len(result.split(",")) is 3:
			handle = result.split(",")[0]
			date = result.split(",")[1]
			tweet = result.split(",")[2]
	
			month = str(date.split("T")[0].split("-")[1])
			year = str(date.split("T")[0].split("-")[0])

			monthYear = month + "/" + year
	
			if handle not in analysis:
				analysis[handle] = {}
	
			if monthYear not in analysis[handle]:
				analysis[handle][monthYear] = 0
	
			analysis[handle][monthYear] = analysis[handle][monthYear] + 1

	return analysis

def writeResults(results):
	lines = []
	lines.append("handle,month,tweet_count")

	for handle in results:
		for monthYear in results[handle]:
			lines.append("%s,%s,%s" % (handle, monthYear, results[handle][monthYear]))

	timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')
	with open("%stweet_count_results-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
		file.write("\n".join(lines))

def main():
	with open(TWEET_FILE, encoding="utf-8") as f:
		results = f.read().splitlines()
		print("Found %d tweets to analyze" % len(results))

		analysis = analyzeResults(results[1:])

		writeResults(analysis)

if __name__ == "__main__":
	main()
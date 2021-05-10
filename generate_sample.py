import sys
import time
import datetime

OUTPUT_DIR = "./Output/"
FILE_TO_FILTER = "./Output/query_results-2021-05-10T13-54-07Z.csv"
SAMPLE_SIZE = 5

words = [
	"Einwanderer",
	"Einwandererin",
	"Einwanderung",
	"Grenzkontrolle",
	"Grenze",
	"Grenzen",
	"Einwanderungsland",
	"Einwanderungsgesetze",
	"Einwanderungsantrag",
	"Einwanderungsstop",
	"Einwandererfamilie",
	"Immigrant",
	"Immigrantin",
	"Immigrantenfamilie",
	"Zuwanderer",
	"Zuwandererin",
	"Gastarbeiter",
	"Gastarbeiterin",
	"Wanderarbeiter",
	"Wanderarbeiterin",
	"Wirtschaftsflüchtling",
	"Arbeitsmigrant",
	"Wanderarbeitskraft",
	"Asylsuchende",
	"Asylsuchender",
	"Asylbewerber",
	"Asylbewerberin",
	"Asylwerber",
	"Asylwerberin",
	"Flüchtling",
	"Flüchtlinge",
	"Rechsstellung",
	"Flüchtlingslager",
	"Armutsflüchtling",
	"Flüchlingsstatus",
	"Asyl",
	"Zuflucht",
	"Wanderung",
	"Migration",
	"Abwanderung",
	"Umzug",
	"Auswanderung",
	"Wanderungsstrom",
	"Massenwanderbewegung",
	"Flüchtlingsbewegung",
	"Aüslander",
	"Aüslanderin",
	"Aüslandisch",
	"Vertriebene",
	"Vertriebener",
	"Sicherheit",
	"Bedrohung",
	"Asylant",
	"Umvolkung",
	"Bevölkerungsaustausch",
	"Asylindustrie",
	"Flüchtlingswelle"
]

def filterResults(results):
	filteredResults = []
	for result in results:
		found = False
		for word in words:
			if word.lower() in result.lower():
				found = True
				break

		if not found:
			filteredResults.append(result)

	return filteredResults

def getSample(filteredResults):
	sample = filteredResults[1::SAMPLE_SIZE]

	return sample

# Creates the csv and MD files with the results of a run
# 
# The files are named query_results-<timestamp>.csv and query_results-<timestamp>.md
def writeResults(results):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

    writeCsvResults(timestamp, results)
    writeMdResults(timestamp)

def writeCsvResults(timestamp, results):
	with open("%srandom_sample-%s.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
		file.write(results)

def writeMdResults(timestamp):
    with open("%srandom_sample-%s.md" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
        file.write("File filtered: %s\n" % FILE_TO_FILTER)
        file.write("Filter list: [%s]\n" % ", ".join(words))
        file.write("Percentage sampled: %f%%" % (100/SAMPLE_SIZE))

def main():
	with open(FILE_TO_FILTER, encoding="utf-8") as f:
		results = f.read().splitlines()
		print("Found %d tweets to filter" % len(results))

		csvString = "handle,date,text\n"
		filteredResults = filterResults(results)
		print("Found %d tweets that contained no words of interest" % len(filteredResults))

		sample = getSample(filteredResults)

		print("Sampled %d tweets" % len(sample))

		writeResults(csvString + "\n".join(sample))

if __name__ == "__main__":
	main()
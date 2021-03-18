import sys
import time
import datetime

OUTPUT_DIR = "./Output/"
FILE_TO_FILTER = "./Output/query_results-2021-03-18T16-12-09Z.csv"

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
	"Moslem",
	"Moslemin",
	"Muslim",
	"Muslimin",
	"Moslemisch",
	"Moslemisches ",
	"Moslemischer",
	"Islam",
	"Terrorist",
	"Terroristin",
	"Terroristisch",
	"Terroranschlag",
	"Terrorgruppe",
	"Terrororganisation",
	"Terroristische",
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
	"Islamisch",
	"Islamischer Staat",
	"Vertriebene",
	"Vertriebener",
	"Sicherheit",
	"Bedrohung"
]

def filterResults(results):
	filteredResults = []
	for result in results:
		for word in words:
			if word in result:
				filteredResults.append(result)
				break

	return filteredResults

# Creates the csv and MD files with the results of a run
# 
# The files are named query_results-<timestamp>.csv and query_results-<timestamp>.md
def writeResults(results):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H-%M-%SZ')

    writeCsvResults(timestamp, results)
    writeMdResults(timestamp)

def writeCsvResults(timestamp, results):
	with open("%squery_results-%s-filtered.csv" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
		file.write(results)

def writeMdResults(timestamp):
    with open("%squery_results-%s-filtered.md" % (OUTPUT_DIR, timestamp), "w", encoding="utf-8") as file:
        file.write("File filtered: %s\n" % FILE_TO_FILTER)
        file.write("Filter list: [%s]\n" % ",".join(words))

def main():
	with open(FILE_TO_FILTER, encoding="utf-8") as f:
		results = f.read().splitlines()
		print("Found %d tweets to filter" % len(results))

		csvString = "handle,date,text\n"
		filteredResults = filterResults(results)
		print("Found %d tweets that contained atleast 1 word of interest" % len(filteredResults))

		writeResults(csvString + "\n".join(filteredResults))

if __name__ == "__main__":
	main()
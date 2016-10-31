# -*- coding: utf-8 -*-
import os, sys, csv, math

csv.field_size_limit(sys.maxsize)

def create_folder_if_needed(folder_name):
	# creates a folder that will receive the builds, if it doesn't exists
	try:
		os.makedirs(folder_name)
	except OSError:
		if not os.path.isdir(folder_name):
			raise

def proportion_test(p1, n1, p2, n2):

	n1_f = float(n1)
	n2_f = float(n2)

	# Z value for 0.95 confidence
	z_test = 1.96

	# https://onlinecourses.science.psu.edu/stat414/node/268
	p = ((n1_f * p1) + (n2_f * p2)) / (n1_f + n2_f)

	# H0:p1−p2=0 : means are equals
	dividend =  (math.sqrt(p * (1-p) * (1/n1_f + 1/n2_f)))

	z = 0

	if dividend !=  0:
		z = (p1 - p2 - 0) / dividend


	if z < -z_test:
		print("rejected small " + str(z))
		return -1
	elif z > z_test:
		print("rejected big " + str(z))
		return 1
	else:
		print("not rejected " + str(z))
		return 0

def main():

	
	input_summary_file_path = '../data/group-summary_groupedByBuildId_v2.csv'		

	mininum_builds = 100

	'''
	"Projeto","Qtd builds casuais","Qtd builds não casuais","Perc. sucesso casual","Perc. sucesso não casual","Quem ganha?"
	'''

	casual_wins = 0
	non_casual_wins = 0
	draw = 0
	ignored_rows = 0

	casual_projects = []
	non_casual_projects = []
	
	# get project names
	with open(input_summary_file_path, 'rb') as csvfile:
		# read the file as csv
		filereader = csv.DictReader(csvfile, skipinitialspace=True)

		for row in filereader:
		
			project = row['Projeto']
			casual_builds = float(row['Qtd builds casuais'])
			non_casual_builds = float(row['Qtd builds não casuais'])
			casual_success = float(row['Perc. sucesso casual'])
			non_casual_success = float(row['Perc. sucesso não casual'])
			
			if casual_builds != 0 and non_casual_builds != 0 and casual_builds+non_casual_builds > mininum_builds:

				print(str(casual_builds) + '  ' + str(non_casual_builds) + '  ' + str(casual_success) + '  ' + str(non_casual_success))
				result = proportion_test(casual_success, casual_builds, non_casual_success, non_casual_builds)

				if result == 0:
					draw += 1
					print(project + ": draw")
				elif result == -1:
					non_casual_wins += 1
					print(project + ": non_casual_wins")
					non_casual_projects += [project + " " + str(casual_builds) + " " + str(non_casual_builds) + " " + str(casual_success) + " " + str(non_casual_success)]
				else:
					casual_wins += 1
					print(project + ": casual_wins")
					casual_projects += [project + " " + str(casual_builds) + " " + str(non_casual_builds) + " " + str(casual_success) + " " + str(non_casual_success)]
			else:
				ignored_rows += 1

	

	print("Casual Victories: ")
	for project in casual_projects:
		print(project)
	print("")
	print("Non-Casual Victories: ")
	for project in non_casual_projects:
		print(project)
				
	print("Casual Wins: " + str(casual_wins))
	print("Non-Casual Wins: " + str(non_casual_wins))
	print("Draw: " + str(draw))
	print("Ignored: " + str(ignored_rows))

if __name__ == '__main__':
    main()

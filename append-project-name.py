import os, sys, csv

csv.field_size_limit(sys.maxsize)

def create_folder_if_needed(folder_name):
	# creates a folder that will receive the builds, if it doesn't exists
	try:
		os.makedirs(folder_name)
	except OSError:
		if not os.path.isdir(folder_name):
			raise
def main():

	input_travis_file_path = '/Users/Marcel/Downloads/travistorrent-5-3-2016.csv'	
	input_contact_file_path = '../data/build-commiter-info-sorted2.csv'
	output_contact_file_path = '../data/build-commiter-info-sorted3.csv'		

	project_name_dict = {}

	# get project names
	with open(input_travis_file_path, 'rb') as csvfile:
		# read the file as csv
		filereader = csv.DictReader(csvfile, skipinitialspace=True)

		for row in filereader:
			
			build = row['tr_build_id']
			project = row['gh_project_name']

			project_name_dict[build] = project
			#print(build + ' ' + project)


	
	with open(input_contact_file_path, 'r+') as infile, open(output_contact_file_path, 'wb') as outfile:
					
		# read the file as csv
		inputreader = csv.DictReader(infile, skipinitialspace=True)

		fieldnames = inputreader.fieldnames + ['project_name']
		csvwriter = csv.DictWriter(outfile, fieldnames)
		csvwriter.writeheader()

		for row in inputreader:
			
			if row['build_id'] in project_name_dict:

				build = row['build_id']
				project_name = project_name_dict[build]
			
				csvwriter.writerow(dict(row, project_name=project_name))
			else:
				csvwriter.writerow(dict(row, project_name='error'))

if __name__ == '__main__':
    main()

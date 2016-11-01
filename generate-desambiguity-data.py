import os, sys, csv
import desambiguity as des

csv.field_size_limit(sys.maxsize)

def create_folder_if_needed(folder_name):
	# creates a folder that will receive the builds, if it doesn't exists
	try:
		os.makedirs(folder_name)
	except OSError:
		if not os.path.isdir(folder_name):
			raise
def main():

	input_file_path = '../data/build-commiter-info-sorted3.csv'	
	output_file_path = '../data/build-commiter-info-desamb.csv'
	ambiguous_file_path = '../data/ambiguous-users.csv'		

	current_project = ''
	current_project_users = []
	current_project_ambiguities = {}

	# open the csv containing travis data
	with open(input_file_path, 'rb') as csvfile, open(output_file_path, 'wb') as outfile, open(ambiguous_file_path, 'wb') as amb_file:

		# read the file as csv
		filereader = csv.DictReader(csvfile, skipinitialspace=True)

		csvwriter = csv.DictWriter(outfile, fieldnames=["row","build_id","author_name","author_email","project_name"])
		csvwriter.writeheader()

		amb_file.write("old_name, old_email, substituted_name, substituted_email, project_name\n")

		users = 0
		amb_users = 0

		for row in filereader:
			
			name = row['author_name'].replace(",", "")
			email = row['author_email']
			project = row['project_name']

			if project != current_project:
				current_project = project
				current_project_users = []
				current_project_ambiguities = {}
				print('Starting project '+project)

			found_user = False

			key = name+email
			if key in current_project_ambiguities:
				user = current_project_ambiguities[key]
				row['author_name'] = user[0]
				row['author_email'] = user[1]
				print('pegou do cache: ' + user[0])

			elif (name, email) not in current_project_users:
				for user in current_project_users:
					if des.is_same_person(name, email, user[0], user[1]):
						row['author_name'] = user[0]
						row['author_email'] = user[1]
						found_user = True

						current_project_ambiguities[key] = user
						amb_users += 1
						print('Found ambiguous user! Old name: ' + name + ' Old email: ' + email + ' new name: ' + user[0] + ' new email: ' + user[1])
						amb_file.write(name + "," + email + "," + user[0] + "," + user[1] + "," + project + "\n")

				if not found_user:
					current_project_users.append((name, email))
					print('Found new user: '+name)
					users += 1

			csvwriter.writerow(dict(row))
		print('Users: '+str(users))
		print('Amb Users: '+str(amb_users))


if __name__ == '__main__':
    main()

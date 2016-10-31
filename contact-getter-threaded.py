import urllib2, time, ast, json, os, httplib, sys, csv
from urlparse import urlparse
from collections import deque
from threading import Thread
from Queue import Queue

csv.field_size_limit(sys.maxsize)

# Will fix these later. These are the values that are used across the threads.
CONCURRENT = 20 # number of the maximim concurrent calls
BUILDS_PER_RUN = 2000000

# Example: https://api.travis-ci.org/builds/10297653

# constants
API_URL = 'https://api.travis-ci.org/builds/'

def openUrl(url):

	try:
		return urllib2.urlopen(url)
	except urllib2.HTTPError, e:
		if e.code == 429: # HTTP ERROR 429: TOO MANY REQUESTS
			print url + ' - TOO MANY REQUESTS - RETRYING in 5 seconds'
			time.sleep(5);
			return openUrl(url)
		if e.code == 500: # HTTP ERROR 500: INTERNAL SERVER ERROR
			print url + ' - HTTP ERROR 500 - RETRYING in 5 seconds'
			time.sleep(5);
			return 'error'
		if e.code == 503: # HTTP ERROR 503: SERVICE UNAVAILABLE
			print url + ' - SERVICE UNAVAILABLE - RETRYING in 5 seconds'
			time.sleep(5);
			return openUrl(url)
		raise


def get_web_page_data(url):

	# load the build webpage and retrieve the data, then convert to json
	response = openUrl(url)

	if response == 'error': # an error occurred
		return 'error'
	else:
		html = response.read()
		parsed_json = json.loads(html)
		return parsed_json

# this method downloads the data from the a build and returns its json

def get_build_data(build_id):
	return get_web_page_data(API_URL + str(build_id))


def write_to_file(row_number, data, file_path):

	author_name = 'error'
	author_email = 'error'
	build_id = 'error'

	if data != 'error':
		author_name	= data['author_name']
		author_email = data['author_email']
		build_id = str(data['id'])
	else:
		print 'Encountered error. Row number: ' + str(row_number)

	#if the file already exists, don't need to put a header
	if not os.path.exists(file_path): 
		print 'creating file'
		target_file = open(file_path, 'w')
		
		# write header
		target_file.write("\"row\", \"build_id\", \"author_email.rstrip('\0')\", \"author_name.rstrip('\0')\"")
		target_file.write('\n')
		target_file.close()

	with open(file_path, 'a') as csvfile:
		csvfile.write((row_number + ',' + build_id + ', \"' + author_name + '\", \"' + author_email + '\"\n').encode('UTF-8'))

def create_folder_if_needed(folder_name):
	# creates a folder that will receive the builds, if it doesn't exists
	try:
		os.makedirs(folder_name)
	except OSError:
		if not os.path.isdir(folder_name):
			raise

# this method receives a list of ids and downloads all the data from every id asynchronously.
def download_and_write_assynchronous_threads(row_tuple_list, output_file_path):

	print 'Starting to download the complete build information. Number of builds:' + str(len(row_tuple_list))
	global id_queue

	threads = []
	for i in range(CONCURRENT):
		t = Thread(target=download_and_write_assynchronous, args = [output_file_path]);
		t.daemon = True
		t.start()
		print('started thread '+ str(i))

	try:
		for row_tuple in row_tuple_list:
			id_queue.put(row_tuple)
		id_queue.join()
	except KeyboardInterrupt:
		sys.exit(1)

	print 'Finished to download build information.'
	

def download_and_write_assynchronous(output_file_path):
	while True:

		global row_tuple_list
		global id_queue
		global cached_row
		global cached_id

		row_tuple = id_queue.get()
		print('current row_tuple: '+str(row_tuple))
		row_number = row_tuple[0]
		gh_project_name = row_tuple[1]
		tr_build_id = row_tuple[2]

		if cached_id == tr_build_id:
			print 'Writing ' + gh_project_name + ' Build_id: ' + str(tr_build_id)
			write_to_file(row_number, cached_data, output_file_path)

		else: 
			print 'Downloading row ' + row_number + ' Name:' + gh_project_name + ' Build_id: ' + str(tr_build_id)
			build_data = get_build_data(tr_build_id)

			print 'Writing ' + gh_project_name + ' Build_id: ' + str(tr_build_id) + ' Row: ' + row_number
			write_to_file(row_number, build_data, output_file_path)
			cached_id = tr_build_id
			cached_data = build_data
		

		id_queue.task_done()
	

# this method receives a list of ids and downloads all the data from every id asynchronously.
def download_missing_rows(input_file_path, output_file_path):

	global row_tuple_list
	last_row_number = 0
	row_list = []
	missing_row_list = []
	row_tuple_list = []

	# if the file already exists, skip to last build - horrible
	if os.path.exists(output_file_path): 
		with open(output_file_path, 'rb') as csvfile:
			# read the file as csv
			filereader = csv.DictReader(csvfile, skipinitialspace=True)
			for row in filereader:

				row_number = int(row['row'])
				row_list.append(row_number)
				if row_number > last_row_number:
					last_row_number = row_number

	for x in range(1, last_row_number):
		if x not in row_list:
			missing_row_list.append(x)
		else:
			row_list.remove(x)


	print missing_row_list

	# open the csv containing travis data
	with open(input_file_path, 'rb') as csvfile:
						
		# read the file as csv
		filereader = csv.DictReader(csvfile, skipinitialspace=True)

		# horrible, need to find a better way - skips the info we already have
		for row in filereader:
			
			if not missing_row_list: # list is empty
				break

			if int(row['row']) in missing_row_list:
				row_tuple = (row['row'], row['gh_project_name'],row['tr_build_id'])				
				row_tuple_list.append(row_tuple)
				missing_row_list.remove(int(row['row']))
			

	download_and_write_assynchronous_threads(row_tuple_list, output_file_path)
	
	while True:
		time.sleep(100)



def main():

	global id_queue
	global row_tuple_list
	global cached_id
	global cached_data

	id_queue = Queue(CONCURRENT * 2)
	row_tuple_list = []
	cached_id = "-1"

	#input_file_path = 'data-testing-get-email'
	input_file_path = '/Users/Marcel/Downloads/travistorrent-5-3-2016.csv'	
	output_file_path = 'build-commiter-info-threaded.csv'

	last_row_number = 0

	#download_missing_rows(input_file_path, output_file_path)

	# if the file already exists, skip to last build - horrible
	if os.path.exists(output_file_path): 
		with open(output_file_path, 'rb') as csvfile:
			# read the file as csv
			filereader = csv.DictReader(csvfile, skipinitialspace=True)
			for row in filereader:

				row_number = int(row['row'])
				print(row_number)
				if row_number > last_row_number:
					last_row_number = row_number

	print(last_row_number)
	

	# open the csv containing travis data
	with open(input_file_path, 'rb') as csvfile:
						
		# read the file as csv
		filereader = csv.DictReader(csvfile, skipinitialspace=True)

		# horrible, need to find a better way - skips the info we already have
		print('skipping')
		for i in range(last_row_number):
   			filereader.next()

   		print('skipped')
		for row in filereader:
			
			row_tuple = (row['row'], row['gh_project_name'],row['tr_build_id'])				
			row_tuple_list.append(row_tuple)

			if int(row['row']) > BUILDS_PER_RUN + last_row_number:
				break

	download_and_write_assynchronous_threads(row_tuple_list, output_file_path)

	while True:
		time.sleep(100)

	

if __name__ == '__main__':
    main()

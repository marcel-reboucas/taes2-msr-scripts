# -*- coding: utf-8 -*-

# pip install python-Levenshtein
# https://pypi.python.org/pypi/python-Levenshtein
from Levenshtein import *
from warnings import warn
import string
import unicodedata

def substring_after(s, delim):
    return s.partition(delim)[2]

def substring_before(s, delim):
	return s.split(delim)[0]

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.decode('utf-8').strip())
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def remove_punctuation(input_str):
	table = string.maketrans("","")
	return input_str.translate(table, string.punctuation.replace("@",""))

def is_same_person(name1_u, email1_u, name2_u, email2_u, threshold = 0.93):
	
	'''
	Before the identification, they remove accent marks and punctuation in the names and split the name into first and last name. 
	Default threshold: 0.93

	Is the same if:
	simil(completeNameA, completeNameB) ≥ t; or
	simil(firstNameA, firstNameB) ≥ t and simil(lastNameA, lastNameB) ≥ t; or
	prefixB contains firstNameA and lastNameA; or
	prefixB contains firstNameA and the initial of lastNameA; or
	prefixB contains the initial of firstNameA and the lastNameA; or
	simil(prefixA, prefixB) ≥ t.
	'''

	name1 = remove_accents(remove_punctuation(name1_u.lower()))
	name2 = remove_accents(remove_punctuation(name2_u.lower()))
	email1 = email1_u.decode('utf-8').strip()
	email2 = email2_u.decode('utf-8').strip()

	#simil(completeNameA, completeNameB) ≥ t;
	if ratio(name1, name2) > threshold:
		return True

	first_name_a = substring_before(name1, ' ')
	first_name_b = substring_before(name2, ' ')
	last_name_a = substring_after(name1, ' ')
	last_name_b = substring_after(name2, ' ')

	#simil(firstNameA, firstNameB) ≥ t and simil(lastNameA, lastNameB) ≥ t;
	if ratio(first_name_a, first_name_b) > threshold and ratio(last_name_a, last_name_b)  > threshold:
		return True

	prefix_a = substring_before(email1, '@')
	prefix_b = substring_before(email2, '@')

	# prefixB contains firstNameA and lastNameA; or
	if first_name_a in prefix_b and last_name_a in prefix_b and first_name_a:
		return True
	
	first_name_a_plus_initial = first_name_a if not last_name_a else first_name_a + last_name_a[0]

	# prefixB contains firstNameA and the initial of lastNameA; or
	if first_name_a_plus_initial in prefix_b and first_name_a:
		return True

	initial_first_plus_last_name_a = last_name_a if not first_name_a else first_name_a[0] + last_name_a

	#prefixB contains the initial of firstNameA and the lastNameA; or
	if last_name_a and initial_first_plus_last_name_a in prefix_b:
		return True

	# simil(prefixA, prefixB) ≥ t.
	if ratio(prefix_a, prefix_b) > threshold:
		return True

	return False


def test():
	
	table = string.maketrans("","")

	print(ratio("marcos", "marcel"))
	print(distance("marcos", "marcel"))

	print(substring_before("marcos aurelio", ' '))
	print(substring_before("marcos", ' '))
	print(substring_before("marcos silva", ' '))
	print(substring_after("marcos aurelio", ' '))
	print(substring_after("marcos da silva cordeiro", ' '))
	print(substring_after("marcos", ' '))

	first_name_a = "marcos"
	last_name_a = "bas"
	first_name_a_plus_initial = first_name_a if not last_name_a else first_name_a + last_name_a[0]
	print(first_name_a_plus_initial)

	# prefixB contains firstNameA and lastNameA; or
	prefix_a = substring_before("mscr@cin.ufpe,br", '@')
	print(prefix_a)

	name = "João ,da Silvá. Meire . Santos"

	print(remove_punctuation(name))
	print(remove_accents(name))
	print(remove_accents(remove_punctuation(name)))

def main():
	print(is_same_person("pivotal", "pivotal@darwin.boulder.pivotallabs.com", "Mark Rushakoff and Tim Labeeuw", "pair+mrushakoff+tim@pivotallabs.com"))
	print(is_same_person("//de", "code@extremist.digital", "Jens Bissinger", "mail@jens-bissinger.de"))
	print(is_same_person("Михаил", "mixan946@yandex.ru", "Ricardo Trindade", "ricardo.silva.trindade@gmail.com"))
	print(is_same_person("Sarah Chandler", "schandler@pivotallabs.com", "Mark Rushakoff and Sarah Chandler", "pair+mrushakoff+schandler@pivotallabs.com"))
	print(is_same_person("=", "=", "Ebrahim Byagowi", "ebrahim@gnu.org"))
	print(is_same_person("Trung Lê", "joneslee85@gmail.com", "Phil Ostler", "philostler@gmail.com"))

	#test()	

if __name__ == '__main__':
    main()

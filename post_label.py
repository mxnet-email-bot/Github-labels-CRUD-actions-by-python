from __future__ import print_function
import requests
import json
from httplib2 import Http
import random 
import re

GITHUB_USER = "CathyZhang0822"
GITHUB_PASSWORD = "230538474afac8233a43264d620b69bf51054f7e"

REPO = "CathyZhang0822/Email-Bot" #eg "CathyZhang0822/Email-Bot"
#REPO = "apache/incubator-mxnet"
REPO_URL = 'https://api.github.com/repos/%s' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
auth_header = {'Authorization': 'token {oa2}'.format(oa2=GITHUB_PASSWORD)}

def rand_hex_color():
	# generate a hex random color
	_HEX = "0123456789abedef"
	return ''.join(random.choice(_HEX) for _ in range(6))

def cleanstr(str, e):
    # convert all non-alphanumeric charaters into e
    cleanstr = re.sub("[^0-9a-zA-Z]",e,str)
    return cleanstr.lower()

def count_pages():
	response = requests.get(REPO_URL + "/labels", auth = AUTH)
	assert response.headers["Status"] == "200 OK", "Authorization failed"
	if ("link" not in response.headers):
		return 1
	return int(cleanstr(response.headers['link'], " ").split()[-3])

def all_labels():
	pages = count_pages()
	retval = [] #list of labels
	for page in range(1, pages + 1):
		url = REPO_URL + "/labels?page=" + str(page) + "&per_page=30"
		response = requests.get(url, auth = AUTH)
		for item in response.json():
			retval.append({item['name'].lower() : item['url']})
	print(len(retval))
	return retval
def create_label(label_name):
	# label_name:string
	color = rand_hex_color()
	print(color)
	label = {"name": label_name,
			 "description": "", 
			 "color": color }
	response = requests.post(REPO_URL + "/labels", json.dumps(label), auth = AUTH)
	if response.status_code == 201:
		print("Successfully create label")
	else:
		print("Could not create the label")
		print("Response:", response.json())
def update_label(old_label_name, new_label_name, new_description, new_color):
	new_label = {"name":new_label_name,
				 "description":new_description,
				 "color": new_color}
	response = requests.patch(REPO_URL + "/labels/" + old_label_name, json.dumps(new_label), auth = AUTH)
	if response.status_code == 200:
		print("Successfully update label")
	else:
		print("Could not delete the label")
		print("Response:", response.json())
def delete_label(label_name):
	response = requests.delete(REPO_URL + "/labels/" + label_name, auth = AUTH)
	if response.status_code == 204:
		print("Successfully delete {label}".format(label = label_name))
	else:
		print("Could not delete the label")
		print("Response:", response.json())


def add_github_labels(number, labels):
	# number: int(the issue number); labels: list of strings
	issue_labels_url = REPO_URL + "/issues/{id}/labels".format(id = number)
	response = requests.post(issue_labels_url, json.dumps(labels), auth = AUTH)
	if response.status_code == 200:
		print('Successfully add labels')
	else:
		print('Could not add the label')
		print('Response:', response.json())

update_label("wontfix", "wont fix", "", rand_hex_color())




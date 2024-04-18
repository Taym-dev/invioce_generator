import json
from os import listdir, replace
from os.path import isfile, join, dirname, realpath
from invoice import createInvoice
from re import match
 
this_path = dirname(realpath(__file__))
json_in_path = f"{this_path}/JSON_IN"
json_procecsed = f"{this_path}/JSON_PROCESSED"
 
onlyfiles = [f for f in listdir(json_in_path) if isfile(join(json_in_path, f))]
 
for fileName in onlyfiles:    
	file = open(f"{json_in_path}/{fileName}")
	file_data = json.load(file)["order"]

	INVOICE_INFO = {
		"id": file_data["ordernummer"],
		"createdAt": file_data["orderdatum"],
		"expiresAt": "24-04-2024",
		"term": int(match("\d+", file_data["betaaltermijn"]).group())
	}
 
	CLIENT_INFO = {
		"name": file_data["klant"]["naam"],
		"address": file_data["klant"]["adres"],
		"postalCity": f"{file_data['klant']['postcode']} {file_data['klant']['stad']}",
		"kvk": file_data["klant"]["KVK-nummer"]
	}

	createInvoice(INVOICE_INFO, CLIENT_INFO, file_data["producten"], f"INVOICE/{file_data['ordernummer']}.pdf")
 
	replace(f"{json_in_path}/{fileName}", f"{json_procecsed}/{fileName}")
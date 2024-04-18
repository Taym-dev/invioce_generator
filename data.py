import json
from os import listdir, replace
from os.path import isfile, join, dirname, realpath
from invoice import createInvoice
from re import match
from datetime import datetime, timedelta
 
this_path = dirname(realpath(__file__))
json_in_path = f"{this_path}/JSON_IN"
json_procecsed = f"{this_path}/JSON_PROCESSED"
 
onlyfiles = [f for f in listdir(json_in_path) if isfile(join(json_in_path, f))]

for fileName in onlyfiles:    
	file = open(f"{json_in_path}/{fileName}")
	file_data = json.load(file)["order"]

	# PDF
	INVOICE_INFO = {
		"id": file_data["ordernummer"],
		"createdAt": file_data["orderdatum"],
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

	# JSON
	invoice = {
		"createdAt": file_data["orderdatum"],
		"expiresAt": (datetime.strptime(INVOICE_INFO['createdAt'], "%d-%m-%Y") + timedelta(INVOICE_INFO['term'])).strftime("%d-%m-%Y"),
		"products": [],
		"totalWithoutTax": 0,
		"tax": 0,
		"total": 0
	}

	for product in file_data["producten"]:
		invoice["products"].append({
			"amount": product["aantal"],
			"name": product["productnaam"],
			"priceOne": product["prijs_per_stuk_excl_btw"],
			"priceAll": round(product["prijs_per_stuk_excl_btw"] * product["aantal"], 2),
			"taxPercentage": product["btw_percentage"]
		})

		invoice["totalWithoutTax"] += product["prijs_per_stuk_excl_btw"]
		invoice["tax"] += round(product["prijs_per_stuk_excl_btw"] * (product["btw_percentage"] / 100), 2)

	invoice["total"] = invoice["totalWithoutTax"] + invoice["tax"]

	with open(f"{this_path}/INVOICE/{fileName}", "w") as file:
		json.dump(invoice, file)


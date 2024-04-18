import json
from os import listdir,replace
from os.path import isfile, join
from invoice import createInvoice
 
json_in_path = "/Users/a../Documents/school/code/invoice_generator/JSON_IN"
json_procecsed = "/Users/a../Documents/school/code/invoice_generator/JSON_PROCESSED"
 
onlyfiles = [f for f in listdir(json_in_path) if isfile(join(json_in_path, f))]
 
for fileName in onlyfiles:    
    file = open(f'{json_in_path}/{fileName}')
    taytib = json.load(file)['order']
    INVOICE_INFO = {
        "id": taytib['ordernummer'],
        "createdAt": taytib['orderdatum'],
        "expiresAt": "24-04-2024",
        "term":taytib['betaaltermijn']
    }
 
    CLIENT_INFO = {
        "name": taytib['klant']['naam'],
        "address": taytib['klant']['adres'],
        "postalCity": f"{taytib['klant']['postcode']} {taytib['klant']['stad']}"
    }
 
    PRODUCTS = [
        { "productnaam": "Dildo", "aantal": 5, "prijs_per_stuk_excl_btw": 30, "btw_percentage": 21 },
        { "productnaam": "Dildo XXL", "aantal": 2, "prijs_per_stuk_excl_btw": 30, "btw_percentage": 9 }
    ]
    createInvoice(INVOICE_INFO, CLIENT_INFO, taytib['producten'], f"INVOICE/{taytib['ordernummer']}.pdf")
 
    replace(f'{json_in_path}/{fileName}', f'{json_procecsed}/{fileName}')
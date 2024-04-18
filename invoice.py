from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

COMPANY_INFO = {
	"name": "Naam",
	"address": "Adres 1",
	"postalCity": "1234AB Stad",
	"kvk": "12345678",
	"btw": "NL123456789B01",
	"bank": "NL12ABNA1234567890"
}

def formatMoney(value):
	return "€ {:,.2f}".format(round(value, 2)).replace(",", "|").replace(".", ",").replace("|", ".")

def createInvoice(invoiceInfo, clientInfo, products, outputPath):
	c = canvas.Canvas(outputPath, pagesize=A4)

	c.setFont("Helvetica", 12)
	
	offsetLeft = 50
	offsetRight = A4[0] - 225

	c.drawString(offsetRight, A4[1] - (100 + (18 * 0)), COMPANY_INFO["name"])
	c.drawString(offsetRight, A4[1] - (100 + (18 * 1)), COMPANY_INFO["address"])
	c.drawString(offsetRight, A4[1] - (100 + (18 * 2)), COMPANY_INFO["postalCity"])

	c.drawString(offsetRight, A4[1] - (175 + (18 * 0)), f"KVK:  {COMPANY_INFO['kvk']}")
	c.drawString(offsetRight, A4[1] - (175 + (18 * 1)), f"BTW:  {COMPANY_INFO['btw']}")
	c.drawString(offsetRight, A4[1] - (175 + (18 * 2)), f"Bank:  {COMPANY_INFO['bank']}")

	c.drawString(offsetLeft, A4[1] - (258 + (18 * 0)), clientInfo['name'])
	c.drawString(offsetLeft, A4[1] - (258 + (18 * 1)), clientInfo['address'])
	c.drawString(offsetLeft, A4[1] - (258 + (18 * 2)), clientInfo['postalCity'])
	c.drawString(offsetLeft, A4[1] - (258 + (18 * 3)), f"KVK: {clientInfo['kvk']}")

	c.setFont("Helvetica", 24)
	c.drawString(offsetLeft, A4[1] - (375 + (28 * 0)), "FACTUUR")
	
	c.setFont("Helvetica", 12)
	c.drawString(offsetLeft, A4[1] - (395 + (18 * 0)), f"Factuurnummer: {invoiceInfo['id']}")

	expiresAt = (datetime.strptime(invoiceInfo['createdAt'], "%d-%m-%Y") + timedelta(invoiceInfo['term'])).strftime("%d-%m-%Y")

	c.drawString(offsetRight, A4[1] - (375 + (18 * 0)), f"Factuurdatum: {invoiceInfo['createdAt']}")
	c.drawString(offsetRight, A4[1] - (375 + (18 * 1)), f"Vervaldatum:   {expiresAt}")

	c.drawString(100, A4[1] - (435 + (18 * 0)), "Omschrijving")
	c.drawString(325, A4[1] - (435 + (18 * 0)), "Bedrag")
	c.drawString(410, A4[1] - (435 + (18 * 0)), "Totaal")
	c.drawString(500, A4[1] - (435 + (18 * 0)), "BTW")

	c.line(50, 400, 535, 400)

	subTotal = 0
	totalTax = 0

	for i, product in enumerate(products):
		productTotal = product['prijs_per_stuk_excl_btw'] * product['aantal']

		subTotal += productTotal
		totalTax += productTotal * (product['btw_percentage'] / 100)

		c.drawString(55, A4[1] - (456 + (21 * i)), f"{product['aantal']}x")
		c.drawString(100, A4[1] - (456 + (21 * i)), f"{product['productnaam']}")
		c.drawString(325, A4[1] - (456 + (21 * i)), formatMoney(product['prijs_per_stuk_excl_btw']))
		c.drawString(410, A4[1] - (456 + (21 * i)), formatMoney(productTotal))
		c.drawString(500, A4[1] - (456 + (21 * i)), f"{product['btw_percentage']}%")

		c.line(50, (379 - (21 * i)), 535, (379 - (21 * i)))

	c.drawString(325, A4[1] - (458 + (21 * (i + 1))), "Subtotaal")
	c.drawString(410, A4[1] - (458 + (21 * (i + 1))), formatMoney(subTotal))

	c.drawString(325, A4[1] - (457 + (21 * (i + 2))), "BTW")
	c.drawString(410, A4[1] - (457 + (21 * (i + 2))), formatMoney(totalTax))

	c.line(310, (334 - (21 * i)), 490, (334 - (21 * i)))

	c.drawString(325, A4[1] - (461 + (21 * (i + 3))), "Totaal")
	c.drawString(410, A4[1] - (461 + (21 * (i + 3))), formatMoney(subTotal + totalTax))

	c.setFont("Helvetica", 10)
	c.drawString(50, 66, f"Wij verzoek u om de betaling binnen {invoiceInfo['term']}-dagen te voldoen op rekening {COMPANY_INFO['bank']}")
	c.drawString(50, 50, "onder vermelding van het factuurnummer.")

	c.save()

# Test
# INVOICE_INFO = {
# 	"id": "123456789",
# 	"createdAt": "01-01-1970",
# 	"term": 1
# }

# CLIENT_INFO = {
# 	"name": "Naam",
# 	"address": "Adres 2",
# 	"postalCity": "4321BA Stad",
# 	"kvk": "87654321"
# }

# PRODUCTS = [
# 	{ "productnaam": "A", "aantal": 1, "prijs_per_stuk_excl_btw": 7.5, "btw_percentage": 21 },
# 	{ "productnaam": "B", "aantal": 2, "prijs_per_stuk_excl_btw": 7.5, "btw_percentage": 9 }
# ]

# createInvoice(INVOICE_INFO, CLIENT_INFO, PRODUCTS, "invoice.pdf")
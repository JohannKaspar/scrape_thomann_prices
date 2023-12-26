import time
from helpers import *
import csv

instrument_urls = {
    "geigensaiten": "alle-produkte-der-kategorie-saiten-fuer-violinen.html",
    "bratschensaiten": "saiten_fuer_violen_-_bratschen.html",
    "cellosaiten": "alle-produkte-der-kategorie-saiten-fuer-celli.html",
}

req_params = {
    'ls': '100',
    'manufacturer[]': [
        'Daddario', 'Jargar', 'Kaplan', 'Pirastro', 'Prim', 
        'Thomastik', 'W.E. Hill & Sons', 'Warchal', 'Westminster', 'Optima'
    ],
    'filter': 'true',
    'setViewMode': 'list'
}

for instrument, instrument_url in instrument_urls.items():
    # loop thorugh the instrument_subpages and create a list of all product links
    page_number = 1
    product_links = []
    
    # loop through the all pages of the instrument results and collect the product links
    while True:
        req_params['pg'] = page_number
        intrument_products_page = get_page(create_url(instrument_url), params=req_params)
        intrument_products_soup = get_soup(intrument_products_page)
        # get all product links from the page
        page_product_links = get_product_links(intrument_products_soup)
        if len(page_product_links) == 0:
            break
        product_links.extend(page_product_links)
        page_number += 1
        time.sleep(0.5)

    product_list = []
    # loop through the product links and extract the product name and price
    for i, product_link in enumerate(product_links[:20]):
        product_page = get_page(create_url(product_link))
        product_soup = get_soup(product_page)
        product_name = get_product_name(product_soup)
        product_price = get_price(product_soup)
        article_number = get_article_number(product_soup)

        product_list.append([
            "", #Artikelnummer (GEWA)
            "", #GTIN/EAN
            product_name, #Bezeichnung
            "", #Beschreibung
            f"Thomann Artikelnummer {article_number}, {product_link}", #Notiz
            "Stück", #Einheit
            "USt 19%", #Steuerart
            product_price, #Bruttopreis
            article_number #Thomann Artikelnummer
            ])

        time.sleep(0.5)

        if i%10 == 0:
            print(f"Produkt {i} von {len(product_links)} in {instrument} abgerufen")

    # write instrument file
    with open(f"data/thomann_prices_{instrument}.csv", "w", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='\'',
                                quoting=csv.QUOTE_MINIMAL)
        header = ["Artikelnummer",
                  "GTIN/EAN",
                  "Bezeichnung",
                  "Beschreibung",
                  "Notiz",
                  "Einheit",
                  "Steuerart",
                  "Bruttopreis",
                  "Thomann Artikelnummer"]
        filewriter.writerow(header)
        for item_info in product_list:
            filewriter.writerow(item_info)

    # write total file
    with open(f"data/thomann_prices_all.csv", "w", newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='\'',
                                quoting=csv.QUOTE_MINIMAL)
        header = ["Artikelnummer",
                  "GTIN/EAN",
                  "Bezeichnung",
                  "Beschreibung",
                  "Notiz",
                  "Einheit",
                  "Steuerart",
                  "Bruttopreis",
                  "Thomann Artikelnummer"]
        filewriter.writerow(header)
        for item_info in product_list:
            filewriter.writerow(item_info)
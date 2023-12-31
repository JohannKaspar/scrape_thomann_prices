import bs4
import requests
import csv

base_url = "https://www.thomann.de/de"

def get_page(url, params=None):
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.text

def get_soup(page):
    return bs4.BeautifulSoup(page, 'html.parser')

# function that extracts ther article number
def get_article_number(soup):
    # Find the <span> element with the class "keyfeature__label" containing the label "Artikelnummer"
    label_element = soup.find("span", class_="keyfeature__label", text="Artikelnummer")

    # Check if the label element is found
    if label_element:
        # Find the sibling <span> element with the article number
        article_number_element = label_element.find_next_sibling("span", class_="fx-text")

        # Check if the article number element is found
        if article_number_element:
            # Extract the article number
            article_number = article_number_element.text.strip()
            return article_number
        else:
            print("Article number element not found.")
            return None
    else:
        print("Label element 'Artikelnummer' not found.")
        return None

# function that extracts the text of the h1 element with class "fx-product-headline product-title__title"
def get_product_name(soup):
    # Auswahl des h1-Elements mit der spezifischen Klasse
    product_name_element = soup.select_one('h1.fx-product-headline.product-title__title')
    
    # Überprüfung, ob das Element gefunden wurde
    if product_name_element:
        # Rückgabe des Textinhalts des Elements
        return product_name_element.get_text().strip()
    else:
        # Rückgabe eines leeren Strings oder einer Fehlermeldung, falls das Element nicht gefunden wird
        return "Produktname nicht gefunden"

# fucntion that extracts the price from the div of class "price"
def get_price(soup):
    price_element = soup.select('div[class="price"]')
    if price_element:
        return price_element[0].get_text().replace(u'\xa0€', u' ').strip()
    else:
        return "Preis nicht gefunden"
    return 

# function for getting all product links from a page (objects of class "product__content")
def get_product_links(soup):
    product_links = []
    product_elements = soup.select('a[class="product__content"]')
    
    # extrat the href attribute from each element
    for element in product_elements:
        product_links.append(element.get('href'))
    return product_links

def create_url(extension, base_url=base_url):
    return base_url + "/" + extension

def get_dialect(path_to_csv):
    with open(path_to_csv, "r", newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        return dialect

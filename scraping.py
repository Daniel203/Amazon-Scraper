import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import sys


class AmazonScraper:

    def __init__(self, keyword):
        self.keyword = keyword

    def generate_url(self):
        """ Generate the amazon's url for the specitfic keyword """
        keyword_url = self.keyword.replace(" ", "+")  # apple airpods -> apple+airpods
        url = "https://www.amazon.it/s?k=" + keyword_url
        return url

    def scrape(self):
        """ scrape informations """
        has_next = True
        number = 0  # page number

        # clear the file
        with open(os.path.join(sys.path[0], "products.csv"), "w") as csvFile:
            csvFile.write("")

        # write informations on a csv file
        with open(os.path.join(sys.path[0], "products.csv"), "a") as csvFile:
            csv_writer = writer(csvFile)
            csv_writer.writerow(['Name', 'Price', 'By', 'Sold By'])
            # scrape products
            while has_next:
                url = f'{self.generate_url()}&page={number}'
                # request 
                respone = requests.get(url)
                soup = BeautifulSoup(respone.text, 'html.parser')
                # check if is the last page 
                try:
                    if soup.find(class_='a-pagination').find(class_='a-disabled a-last') != None:    
                        has_next = False
                except AttributeError:
                    print("Attribute error")
                # find products
                products = soup.findAll(class_='a-link-normal a-text-normal')
                # print products
                for product in products:
                    info_scraped = []
                    info_scraped.append(product.get('href').split("/")[1])  # get product's name and add it to the list
                    link ='https://www.amazon.it' + product.get('href')  # get produtct's link
                    product_page = requests.get(link)
                    soup_ = BeautifulSoup(product_page.text, 'html.parser')  # open link with BeautifulSoup
                    try:
                        info_scraped.append(soup_.find(id='priceblock_ourprice').getText().replace('\xa0',''))  # get product's price
                    except AttributeError:
                        info_scraped.append('')
                    try:
                        info_scraped.append(soup_.find(id='bylineInfo').getText())  # get product's owner
                    except AttributeError:
                        info_scraped.append('')
                    try:
                        info_scraped.append(soup_.find(id='sellerProfileTriggerId').getText())  # get product's owner
                    except AttributeError:
                        info_scraped.append('')
                    print(info_scraped)
                    csv_writer.writerow(info_scraped)
                # next page
                number += 1


if __name__ == "__main__":
    amazonScraper = AmazonScraper("Iphone7")
    amazonScraper.scrape()

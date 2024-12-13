
import feedparser
from lxml.html import fromstring
import csv
import os
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup



def feed_xml():
    rss="https://us-cert.cisa.gov/ics/advisories/advisories.xml"
    feed = feedparser.parse(rss)
    # Ensure the directory exists
    directory = '../data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('./data/advisories.xml', 'w',encoding='utf-8') as xml_file:
        xml_file.write(feed['feed']['title'])

    

def feed_to_csv():
# Fetch the XML data from the URL
    rss="https://us-cert.cisa.gov/ics/advisories/advisories.xml"
    response = requests.get(rss)
    xml_data = response.content

    # Parse the XML data
    root = ET.fromstring(xml_data)
    with open('./data/advisories.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'description', 'published', 'link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    # Extract and print information from each <item> element
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            pub_date = item.find('pubDate').text
        

            # Convert HTML description to plain text
            soup = BeautifulSoup(description, 'html.parser')
            description_text = soup.get_text()

            writer.writerow({
                'title': title,
                'description': description_text,
                'published': pub_date,
                'link': link
            })
feed_xml()
feed_to_csv()

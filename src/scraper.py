from bs4 import BeautifulSoup
from requests import Session
import csv
import json
import re
import requests

class WikipediaScraper:
    '''A class to scrape Wikipedia for countries leaders.'''

    def __init__(self, base_url: str, session: Session):
        '''Initialize the WikipediaScraper object.'''
        self.base_url = base_url
        self.status_endpoint = '/status'
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.session = session
        self.leaders_data = {}
        
    def check_connection(self):
        '''Check the connection to the API.'''
        print("Checking API status...")
        try:
            r = self.session.get(f'{self.base_url}{self.status_endpoint}')
            if r.status_code == 200:
                print("The server is up and running. Continue...")
            else:
                print(f'Something went wrong: status code is {r.status_code}')
            return r.status_code
        except requests.exceptions.RequestException as e:
            print(f'An error during request: {e}')
    
    def refresh_cookie(self):
        '''Refresh the cookie used to access the API.'''
        try:
            cookie = self.session.get(f'{self.base_url}{self.cookies_endpoint}').cookies
            return cookie
        except requests.exceptions.RequestException as e:
            print(f'An error during request cookies: {e}')

    def get_countries(self):
        '''Get a list of supported countries from the API.'''
        r = self.session.get(f"{self.base_url}{self.country_endpoint}", cookies=self.refresh_cookie())
        return r.json()
    
    def get_leaders(self, country: str):
        '''Get leaders data for a given country.'''
        r = self.session.get(f'{self.base_url}{self.leaders_endpoint}', params={'country' : country}, cookies=self.refresh_cookie())
        self.leaders_data[country] = r.json()

    def get_first_paragraph(self, wikipedia_url: str):
        '''Get the first paragraph of the Wikipedia page for a country leader.'''
        r = self.session.get(wikipedia_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div', attrs={'class':"mw-body-content"})
        paragraphs = div.find_all('p')
        for paragraph in paragraphs:
            if re.search(r'^<p><b>.*</b>', str(paragraph)):
                return paragraph.text

    def to_json_file(self, filepath: str):
        '''Write the leaders_data to a JSON file.'''
        with open(filepath, 'w', encoding='utf-8') as json.file:
            json.dump(self.leaders_data, json.file, ensure_ascii=False, indent=4)

    def to_csv_file(self, filepath: str):
        '''Write the leaders_data to a CSV file.'''
        field_names = ["Country", "ID", "First Name", "Last Name", "Birth Date", "Death Date",
                    "Place of Birth", "URL", "Start Mandate", "End Mandate", "Wiki First Paragraph"]
        with open(filepath, 'w', newline='', encoding='utf-8') as csv.file:
            writer = csv.DictWriter(csv.file, fieldnames=field_names)
            writer.writeheader()
            for country, leaders in self.leaders_data.items():
                for leader in leaders:
                    writer.writerow(country, **leader)

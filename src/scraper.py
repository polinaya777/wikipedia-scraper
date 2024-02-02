import b4 as BeautifulSoup
import json
import requests

class WikipediaScraper:
    def __init__(self, url):
        self.url = url
        base_url = 'https://country-leaders.onrender.com'
        country_endpoint = '/countries'
        leaders_endpoint = '/leaders'
        cookies_endpoint = '/cookie'
        leaders_data = {}
        cookie: object
    
    
    def refresh_cookie(self) -> object:
        self.cookie = requests.get(self.base_url + self.cookies_endpoint).json()

    def get_countries(self):
        response = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
        return response.json()
    
    def get_leaders(self, country: str) -> None:
        response = requests.get(self.base_url + self.leaders_endpoint + '/' + country, cookies=self.cookie)
        self.leaders_data[country] = response.json()

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        html = requests.get(wikipedia_url).text
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        return paragraphs[1].text
    
    def to_json_file(self, filepath: str) -> None:
        with open(filepath, 'w') as file:
            file.write(json.dumps(self.leaders_data))  
from requests import Session
from src.scraper import WikipediaScraper


def create_wikiScraper():
    '''Create the WikipediaScraper object instance'''
    while True:
        user_input = input('Do you want to scrape data about world leaders? (Y/N) ').lower()
        if user_input == 'y':
            base_url = 'https://country-leaders.onrender.com'
            wikiScraper = WikipediaScraper(base_url, Session())
            status_code = wikiScraper.check_connection()
            if status_code == 200:
                return wikiScraper
            else:
                print('The server is not responding. Please try again later.\n')
                break
        elif user_input == 'n':
            exit()
        else:
            print('Please enter Y or N!\n')
    

def grabbing_data(wikiScraper: WikipediaScraper):
    '''Grab data from the API'''
    print('Grabbing data...')
    try:
        countries = wikiScraper.get_countries()
        for country in countries:
            wikiScraper.get_leaders(country)
        for country, leaders in wikiScraper.leaders_data.items():
            for leader in leaders:
                leader['wikipedia_first_paragraph'] = wikiScraper.get_first_paragraph(leader['wikipedia_url'])
        print('Data grabbed successfully!')
    except:
        print('An error occurred while grabbing the data. Please try again later.')


def welcome():
    '''Display the welcome message'''
    print("""
    Welcome to the Wikipedia Scraper!
This script will help you grab information about
political leaders of several countries of the world
from API and Wikipedia and save it in JSON or CSV file.\n""")


def menu():
    '''Display the menu'''
    menu = """You can chose the format of the file to export the data to:
    1 - JSON
    2 - SCV
    3 - Exit without saving
    Your selection: """
    return menu


def main():
    '''Main function'''
    welcome()
    wikiScraper = create_wikiScraper()
    grabbing_data(wikiScraper)
    while True:
        try:
            user_choice = int(input(menu()))
            if user_choice == 1:
                print('Exporting data to JSON...')
                wikiScraper.to_json_file('leaders_data.json')
                print('Data exported successfully to: "leaders_data.json"')
                break
            elif user_choice == 2:
                print('Exporting data to CSV...')
                wikiScraper.to_csv_file('leaders_data.csv')
                print('Data exported successfully to: "leaders_data.csv"')
                break
            elif user_choice == 3:
                print('Exiting without saving...')
                break
            else:
                print('Please select a valid option!')
        except:
            print('Please select a valid option!')


if __name__ == "__main__":
    main()
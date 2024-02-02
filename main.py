from src.scraper import WikipediaScraper


def init_wikiScraper():
    pass


def welcome():
    print("""Welcome to the Wikipedia Scraper!
          """)


def menu():
    '''Display the menu'''
    menu = """Please select one of the following options:
    1 - Scrape a country.
    2 - Scrape all countries.
    3 - Get a leader.
    4 - Get all leaders.
    5 - Export data to JSON file (leaders_data.json).
    6 - Exit.

    Your selection: """
    return menu


def main():
    welcome()
    wikiScraper = init_wikiScraper()

    pass


if __name__ == "__main__":
    main()
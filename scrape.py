import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

def scrape_lesson_text(url):
    '''
    This function scrapes the text from the 'lesson' div from the given url
    :param url: str
    :return: str
    '''
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    lesson_div = soup.find('div', class_='lesson')
    if lesson_div:
        return lesson_div.text
    else:
        return "No 'lesson' div found in the webpage."

def main(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape_lesson_text, urls))

    for result in results:
        print(result)

if __name__ == "__main__":
    urls = ["http://example.com", "http://example.org", "http://example.net"]  # replace with your URLs
    main(urls)
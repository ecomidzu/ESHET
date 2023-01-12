from bs4 import BeautifulSoup
import pandas as pd
from os import listdir

def get_pages() -> list:
    return listdir('pages/')

def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()

def parse_data(html: str) -> tuple:
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('#restab tr+ tr td:nth-child(2)')
    titles= []
    links = []
    authors = []
    journals = []
    print(len(articles))
    for article in articles:
        if len(article.contents) ==7:
            authors.append(article.contents[3].text)
            journals.append(article.contents[6].text)
        else:
            journals.append(article.contents[4].text)
            authors.append('')
        titles.append(article.contents[1].text)
        links.append(article.contents[1]['href'])
    return titles, links, authors, journals

def main():
    pages = get_pages()

    all_titles = []
    all_links = []
    all_authors = []
    all_journals = []

    for page in pages:
        html = get_html('pages/'+page)
        titles, links, authors, journals = parse_data(html)
        all_links = all_links + list(links)
        all_titles = all_titles + titles
        all_authors = all_authors + authors
        all_journals = all_journals + journals

    a = pd.DataFrame([all_titles, all_links, all_authors, all_journals], index = ['titles', 'links', 'authors', 'journals']).T
    a.to_excel('result.xlsx', index=False)


if __name__ == '__main__':
    main()
from elibrary import WorkFlow
from parse_links import parse_data, get_pages, get_html
from articles import get_links
from result import parse_data_total, get_articles
from ANOTHER_PARSER import UseSelenium
import pandas as pd
from tqdm import tqdm

def main():
    parser = WorkFlow(query='Экономика', pages=2)
    parser.make_query()
    pages = get_pages()

    all_titles = []
    all_links = []
    all_authors = []
    all_journals = []

    for page in tqdm(pages):
        html = get_html('pages/'+page)
        titles, links, authors, journals = parse_data(html)
        all_links = all_links + list(links)
        all_titles = all_titles + titles
        all_authors = all_authors + authors
        all_journals = all_journals + journals

    a = pd.DataFrame([all_titles, all_links, all_authors, all_journals], index = ['titles', 'links', 'authors', 'journals']).T
    a.to_excel('result.xlsx', index=False)
    a = get_links()
    article = UseSelenium(['https://www.elibrary.ru' + link for link in a], filename=['article_'+str(i)+'.html' for i in range(len(a))], fol_dir='articles')
    article.save_page()
    pages = get_articles()
    new = pd.DataFrame()
    try:
        for page in tqdm(pages):
            html = get_html('articles/'+page)
            result= parse_data_total(html)
            result['ind'] = int(page[8:-5])
            new1 = pd.DataFrame.from_dict(result)
            new = pd.concat([new, new1])
    except Exception as e:
        print(e)
    new = new.set_index('ind')
    print(new)
    d = pd.read_excel('result.xlsx')
    new = pd.concat([d, new],axis=1)
    new.to_excel('exper.xlsx', index=False)

main()
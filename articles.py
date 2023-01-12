import pandas as pd
from ANOTHER_PARSER import UseSelenium

def get_links():
    a = pd.read_excel('result.xlsx')
    return a['links']

def main():
    a = get_links()
    article = UseSelenium(['https://www.elibrary.ru' + link for link in a], filename=['article_'+str(i)+'.html' for i in range(len(a))], fol_dir='articles')
    article.save_page()


if __name__ == '__main__':
    main()
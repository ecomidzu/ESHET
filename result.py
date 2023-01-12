from bs4 import BeautifulSoup
import pandas as pd
from os import listdir
from tqdm import tqdm

def get_pages() -> list:
    return listdir('articles/')

def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()
#Надо бы дописать сбор ключевых слов, рубрику грнти и описаний на других языках, их тоже можно разложить. Улучшить качество.

def parse_data(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.select('#leftcol+ td > table > tbody > tr:nth-child(4) > td:nth-child(1)')
    a = info[0].select('tr')
    total = {}
    total['annotation'] = ''
    ann = 0
    bibl = 0
    alt = 0
    desc_rus=0
    desc_eng=0
    rub=0
    for row in a:
        new = row.select('td')
        for b in new:

            #print(b.text)
            if 'eLIBRARY ID' in b.text:
                total['eLIBRARY ID'] = b.text.split()[2]
            if 'EDN' in b.text:
                total['EDN'] = b.text.split()[1]
            if 'DOI' in b.text:
                total['DOI'] = b.text.split()[1]
            if 'Тип:' in b.text or 'Язык:' in b.text or 'Год издания:' in b.text\
                    or 'УДК:' in b.text or 'Год:' in b.text \
                    or 'Страницы:' in b.text or 'Номер:' in b.text:
                for k in b.text.split('\n'):
                    if ':' in k:
                        total[k.split(':')[0]] = k.split(':')[1].strip()
            if (bibl==1 or alt==1) and 'АЛЬТ' not in b.text:
                g = b.text.split(':')
                if len(g) == 1:
                    total[g[0].strip()]=''
                else:
                    total[g[0].strip()] = g[1].strip()
            if 'БИБЛИОМЕТРИЧЕСКИЕ ПОКАЗАТЕЛИ' in b.text:
                bibl=1
            if 'АЛЬТМЕТРИКИ' in b.text:
                bibl=0
                alt=1
            if 'ОПИСАНИЕ' in b.text:
                alt=0
    key_info = soup.select('table')
    for table in key_info:
        #print(table)
        if 'АННОТАЦИЯ:' in str(table):
            text=''
            c = table.select('div')
            for bg in c:
                text += '\n'+bg.text
            total['АННОТАЦИЯ'] = text
        if 'КЛЮЧЕВЫЕ СЛОВА:' in str(table):
            text=''
            c = table.select('a')
            for bg in c:
                text += '; '+bg.text
            total['Ключевые слова'] = text[2:]
    total = dict(filter(lambda x:x[1], total.items()))
    for key in total.keys():
        total[key] = [total[key]]
    return total



def main():
    pages = get_pages()
    new = pd.DataFrame()
    try:
        for page in tqdm(pages):
            html = get_html('articles/'+page)
            result= parse_data(html)
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


if __name__ == '__main__':
    main()
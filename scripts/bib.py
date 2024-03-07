import requests
import json
import browser_cookie3
from dotenv import load_dotenv
import os

load_dotenv()

arr_authors = [ os.getenv('AUTH') ]
MY_API_KEY = os.getenv('KEY')

cj = browser_cookie3.firefox()
r = requests.get('https://www.scopus.com/search/form.uri?display=advanced', cookies=cj)

bib = set()

def get_scopus_info(SCOPUS_ID):
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
          + SCOPUS_ID
          + "?field=authors,title,publicationName,volume,issueIdentifier,"
          + "prism:pageRange,coverDate,article-number,doi,citedby-count,prism:aggregationType")
    resp = requests.get(url,
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': MY_API_KEY})

    return json.loads(resp.text.encode('utf-8'))

for author in arr_authors:

    resp = requests.get("https://www.scopus.com/onclick/export.uri?oneClickExport=%7b%22Format%22%3a%22BIB%22%2c%22View%22%3a%22CiteOnly%22%7d&origin=AuthorProfile&zone=resultsListHeader&dataCheckoutTest=false&sort=plf-f&tabSelected=docLi&authorId=" + author,
                        cookies=cj,
                        headers={'authority': 'www.scopus.com',
                                'X-ELS-APIKey': MY_API_KEY,
                                'method': 'GET',
                                'path': '/onclick/export.uri?oneClickExport=%7b%22Format%22%3a%22BIB%22%2c%22View%22%3a%22CiteOnly%22%7d&origin=AuthorProfile&zone=resultsListHeader&dataCheckoutTest=false&sort=plf-f&tabSelected=docLi&authorId=56344636600&txGid=17441bcd80bf1c2eb8245e534261d27b',
                                'scheme': 'https',
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                'accept-encoding': 'gzip, deflate, br',
                                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
                                'cache-control': 'max-age=0',
                                'referer': 'https://www.scopus.com/authid/detail.uri?authorId=56344636600',
                                'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-fetch-dest': 'document',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-site': 'same-origin',
                                'sec-fetch-user': '?1',
                                'upgrade-insecure-requests': '1',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
    
    bibitems = str(resp.content).split('\\n\\n')
    bibitems.pop(0)
    for bibitem in bibitems:
        bib.add(bibitem)

with open('../refs.bib', 'w') as file:
    for bibitem in bib:
        file.write(bibitem.replace('\\n', '\n').replace("\\xc2\\xa", " "))
        file.write('\n')
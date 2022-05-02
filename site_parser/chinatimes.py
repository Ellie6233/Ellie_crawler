from bs4 import BeautifulSoup as bs
import requests
import json


def crawl_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        print("有資料")
        
        soup = bs(res.text,'lxml')
    else:
        print("未取得資料")
        
    
    item_dict = {}
    item_dict['title'] = soup.select_one('h1.article-title').string #soup.select_one : 尋找符合條件的第一個元素(只會有一個元素)
    item_dict['time'] = soup.select_one('span.date').string
    item_dict['reporter'] = soup.select_one('div.author a').string
    item_dict['jpg_url'] = soup.select_one('div.photo-container img').string  #soup.select :尋找符合條件的所有元素(因為可能會有多個元素,所以會回傳一個列表)
    
    crawl_page_list = soup.select('div.article-body p')
    item_dict['article'] = " "
    
    #item_dict['news_link'] = soup.select('div._popIn_recommend_art_title')
    
    for article in crawl_page_list:
        if article.string is not None: #因為網頁與法裡面有空值(None)所以要用判斷式把None篩選掉
            #print(article.string)
            #item_dict_article = " ".join(list(article.string)) #因為網頁與法裡面有空值(None)所以無法存進list列表裡面
            item_dict['article'] += article.string + '\n'
            
    item_dict['related_news'] = []
    
    for item in soup.select('div.col h4.title a'):
        #if item['href'].find('beap.gemini'):
        if 'beap.gemini'in item['href']:
            continue
        if item['href'].find('chinatimes.com'):
            item_dict['related_news'].append(item['href'])
        else:
            item_dict['related_news'].append('https://www.chinatimes.com/'+item['href'])
            

        
    return item_dict

first_url = "https://www.chinatimes.com/realtimenews/20220308001524-260407?chdtv"

if __name__ == "__main__":

    url_list = [
        'https://www.chinatimes.com/realtimenews/20220308001524-260407?chdtv',
    'https://www.chinatimes.com/realtimenews/20220308001546-260407?chdtv',
    'https://www.chinatimes.com/realtimenews/20220308001488-260407?chdtv',
    'https://www.chinatimes.com/realtimenews/20220308001474-260407?chdtv',
    'https://www.chinatimes.com/realtimenews/20220303003251-260407?utm_source=traffic.popin.cc&utm_medium=referral&utm_campaign=recmd2&chdtv'
    ]

    #item_dict_list = []

    for url in url_list:
        #item_dict_list.append(crawl_page(url))
        print(json.dumps(crawl_page(url), ensure_ascii = False, indent = 4))
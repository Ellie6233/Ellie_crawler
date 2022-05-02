from bs4 import BeautifulSoup as bs
import requests
import re
import json

def crawl_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        print('有資料')
        
        soup = bs(res.text,'lxml')
    else:
        print('沒有資料')
        

    get_news_dict = {}
    
    get_news_dict['title'] = soup.select_one('h1.content_title').string
    get_news_dict['post_time'] = soup.select_one('div.content_date').string.strip()
    get_news_dict['reporter'] = soup.select_one('div.content_reporter a').string
    get_news_dict['jpg_url'] = soup.select_one('div.image-box img')['src']
    #get_news_dict['jpg_text'] = soup.select_one('div.mainpic_text').string.replace('\xa0',' ').strip()
    jpg_text_elem = soup.select_one('div.mainpic_text').string
    get_news_dict['jpg_text'] =  re.sub(r'\s', '', jpg_text_elem)
    
    get_news_dict['article'] = ''
    article_text = soup.select('div[itemprop=articleBody] p')
    #print(article_text)
    for elem in article_text:
        if elem.string is None:
            continue
        get_news_dict['article'] += elem.string + '\n'
        
    get_news_dict['related_news'] = []
    
    for news in soup.select('div.gray_box.extend_news_url a'):
        #get_news_dict['related_news'].append(news['href'])
        if news['href'].find('tag') != -1 or news['href'].find('subcategory') != -1:
            continue
        
        if news['href'].startswith('http'):
            get_news_dict['related_news'].append(news['href'])
            
        else:
            get_news_dict['related_news'].append('https://newtalk.tw/'+news['href'])
           
    
    return get_news_dict

first_url = "https://newtalk.tw/news/view/2022-03-16/724706"

if __name__ == "__main__":
    url_list = [
        'https://newtalk.tw/news/view/2022-03-16/724706',
        'https://newtalk.tw/news/view/2022-03-16/724639',
        'https://newtalk.tw/news/view/2022-03-16/724553',
        'https://newtalk.tw/news/view/2022-03-16/724466?utm_source=dable&utm_medium=referral',
        'https://newtalk.tw/news/view/2022-03-16/724880'
    ]

    for url in url_list:
        #print(crawl_page(url),ensure_ascii = False)
        #print(crawl_page(url), indent = 4 )
        #print(json.dumps(crawl_page(url), ensure_ascii = False))
        #print(crawl_page(url)) #執行結果同上

        print(json.dumps(crawl_page(url), ensure_ascii = False, indent = 4))
        print()
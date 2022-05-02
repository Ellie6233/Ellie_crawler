from bs4 import BeautifulSoup as bs
import requests
import json


def crawl_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        print('有資料')
        
        soup = bs(res.text,'lxml')
    else:
        print('沒有資料')
        
    
    
    get_news_dict = {}
    
    get_news_dict['url'] = url
    get_news_dict['title'] = soup.select_one('h1').string
    get_news_dict['post_time'] = soup.select_one('div.caas-attr-time-style time').string
    get_news_dict['reporter'] = soup.select_one('span.caas-author-byline-collapse').string
    #get_news_dict['jpg_text'] = soup.select_one('div.caption-wrapper caption-aligned-with-image')['figcaption'].string
    jpg_elem = soup.select_one('div.caas-img-container')
    
    if jpg_elem is not None:
        #get_news_dict['jpg_url'] = jpg_elem.select_one('img')['src']
        get_news_dict['jpg_url'] = jpg_elem.get('src')
        get_news_dict['jpg_text'] = soup.select_one('figcaption').string
        
    else:
        get_news_dict['jpg_url'] = None
        get_news_dict['jpg_text'] = None
    
    get_news_dict['article'] = ''
    
    get_news_article = soup.select_one('div.caas-body')
    
    if  get_news_article is not None:
        for elem in soup.select('div.caas-body p'):
            if elem.string is not None:
                get_news_dict['article'] += elem.string
        
    else:
        get_news_dict['article'] = None
        
    get_news_dict['relacted_news'] = []
    
    for news in soup.select('div.item-hover-trigger a'):
        #if news['href'] == soup.select('div.gemini-item-content,Bdrsbend(4px),Bdrsbstart(4px)'):
            #continue
        if news['href'].startswith('http'):
            get_news_dict['relacted_news'].append(news['href'])
            
        else:
             get_news_dict['relacted_news'].append('https://tw.news.yahoo.com/'+ news['href'])
    
  
    
    return get_news_dict 
if __name__=="__main__":
    url_list = [
        'https://tw.news.yahoo.com/%E7%BF%92%E8%BF%91%E5%B9%B3%E7%88%86%E7%9B%A4%E7%AE%97-%E7%A7%8B%E5%A4%A9-%E6%94%BB%E5%8F%B0-%E5%90%B3%E9%87%97%E7%87%AE-%E5%8F%B0%E7%81%A3%E9%9A%A8%E6%99%82%E5%81%9A%E5%A5%BD%E8%87%AA%E8%A1%9B%E6%BA%96%E5%82%99-020707182.html',
        'https://tw.news.yahoo.com/%E5%8F%B2%E4%B8%8A%E9%A6%96%E6%AC%A1-%E6%AD%90%E6%B4%B2%E7%90%86%E4%BA%8B%E6%9C%83%E5%A4%A7%E6%9C%83%E9%80%9A%E9%81%8E%E9%96%8B%E9%99%A4%E4%BF%84%E7%BE%85%E6%96%AF%E6%9C%83%E7%B1%8D-223040853.html',
        'https://tw.news.yahoo.com/%E5%80%9F%E9%8F%A1%E7%83%8F%E4%BF%84%E6%88%B0%E7%88%AD-%E5%8F%B0%E6%B5%B7%E8%8B%A5%E9%96%8B%E6%89%93-%E5%B0%88%E5%AE%B6-%E5%BB%BA%E6%A7%8B3%E9%81%93%E9%98%B2%E7%B7%9A-150203055.html',
        'https://tw.news.yahoo.com/%E6%AA%A2%E8%A8%8E%E5%8F%B0%E5%8D%97%E6%8E%8930%E5%B9%BE%E8%90%AC%E7%A5%A8-%E9%BB%83%E5%81%89%E5%93%B2-%E7%A5%A8%E6%BA%90%E8%B7%91%E5%88%B0%E7%84%A1%E9%BB%A8%E7%B1%8D%E8%BA%AB%E4%B8%8A-092538889.html',
        'https://tw.news.yahoo.com/%E5%8D%B0%E5%BA%A6%E7%A5%9E%E7%AB%A5%E9%A0%90%E8%A8%80-%E7%83%8F%E4%BF%84%E6%88%B0%E7%88%AD%E7%B5%90%E5%B1%80-7%E5%B9%B4%E5%BE%8C%E6%81%90%E7%88%86%E4%B8%89%E6%88%B0-091300166.html'
    ]

    for url in url_list:
        print(json.dumps(crawl_page(url), ensure_ascii = False, indent = 4))
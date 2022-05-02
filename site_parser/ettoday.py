from bs4 import BeautifulSoup as bs
import requests

def crawl_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        print('有資料')
        
        soup = bs(res.text,'lxml')
        
    else:
        print('沒有取得資料')
        
        
    get_news_dict = {}
    get_news_dict['title'] =soup.select_one('h1.title').string 
    get_news_dict['time'] = soup.select_one('time.date').string.strip()
    reporter = soup.select('div.story p')[2].string #找div底下的第三個p標籤
    reporter = reporter[2:reporter.find('／')]
    print(reporter)
    get_news_dict['reporter'] = reporter
    get_news_dict['jpg_url'] = soup.select('div.story p')[1].string #找div底下的第二個p標籤
    
    crawl_page_list = soup.select('div.story p')
    get_news_dict['article'] = " "
    
    for article in crawl_page_list[3:]:
        if article.string is not None:
            get_news_dict['article'] += article.string + '\n'
            
    
    get_news_dict['related_news'] = []
    get_news_list = soup.select('div.part_list_3 a') 
    
    for url in get_news_list:
        get_news_dict['related_news'].append('https://www.ettoday.net'+url['href']) #找 推薦新聞 的每一個 'href' 標籤的網址
        
        
            

    return get_news_dict

if __name__=="__main__":
    url_list = [
        'https://www.ettoday.net/news/20220308/2203530.htm',
    'https://www.ettoday.net/news/20220308/2203320.htm?ercamp=sorted_hot_news',
    'https://www.ettoday.net/news/20220307/2203248.htm?ercamp=sorted_hot_news',
    'https://www.ettoday.net/news/20220308/2203465.htm?ercamp=sorted_hot_news',
    'https://www.ettoday.net/news/20220307/2202985.htm?ercamp=sorted_hot_news'
    ]


    #print(crawl_page('https://www.ettoday.net/news/20220308/2203530.htm'))
    ettoday_list = []
    for url in url_list:
        ettoday_list.append(crawl_page(url))
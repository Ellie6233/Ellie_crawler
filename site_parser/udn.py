from bs4 import BeautifulSoup as bs
import requests
import json
import re

def crawl_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        print('取得資料')
        
        soup = bs(res.text,'lxml')
        
    else:
        print('未取得資料')
        
    output_dict = {}
    
    output_dict['url'] = url
    output_dict['title'] = soup.select_one('h1.article-content__title').string
    output_dict['post_time'] = soup.select_one('time.article-content__time').string
    journalist_string_generator = soup.select_one('span.article-content__author').stripped_strings
    #output_dict['journalist'] = ''.join(list(journalist_string_generator)).replace(' ','')
    #output_dict['journalist'] = ''.join(list(journalist_string_generator)).replace(' ','').replace('\n','')
    output_dict['journalist'] = re.sub('\s', '', ''.join(list(journalist_string_generator))) 
    
    
    #output_dict[imge_elem] = soup.select_one('img. ls-is-cached lazyloaded') 找不到圖片
    
    image_elem = soup.select_one('figure.figure.article-content__cover')
    if image_elem is not None:
        output_dict['image_url'] = image_elem.select_one('img')['src']
        output_dict['image_text'] = soup.select_one('figcaption').string
        
    else:
        second_image_elem = soup.select_one('article-content__editor img')
        if second_image_elem is not None:
            output_dict['image_url'] = second_image_elem['src']
            output_dict['image_text'] = None  #因為此篇網址的新聞圖片沒有說明所以設定None
            
        else:
            output_dict['image_url'] = None
            output_dict['image_text'] = None
            
    output_dict['article'] = ''
    
    for item in soup.select('section.article-content__editor > p'):
        if len(list(item.stripped_strings)) > 0:
            output_dict['article'] += ''.join(list(item.stripped_strings)) + '\n'
            
    output_dict['related_news'] = []
    
    for item in soup.select('div.story-list__news a'):
        if item['href'] == '#':
            continue
        if item['href'].startswith('http'):
            output_dict['related_news'].append(item['href'])
        else:
            output_dict['related_news'].append('https://udn.com'+item['href'])
    
    
    return output_dict
if __name__=="__main__":
    url_list = [
        'https://udn.com/news/story/122663/6148268?from=udn-catebreaknews_ch2',
        'https://udn.com/news/story/6897/6148131',
        'https://udn.com/news/story/122663/6148084?from=udn-catebreaknews_ch2',
        'https://udn.com/news/story/122699/6148203?from=udn-catebreaknews_ch2',
        'https://udn.com/news/story/122699/6147875?from=udn-catebreaknews_ch2',
    ]

    for url in url_list:
        print(json.dumps(crawl_page(url), ensure_ascii = False, indent = 4))
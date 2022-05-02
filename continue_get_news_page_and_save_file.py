
from argparse import ArgumentParser 

import requests
from bs4 import BeautifulSoup
import importlib
import traceback  #錯誤資訊的報告,當程式異常時會列印異常資訊報告幫助找出錯誤。
import json
import time

from collections import deque

job_queue = deque()
news_id_set = set()

def process_args():
    parser = ArgumentParser()
    parser.add_argument("-o", "--output_file", default="output_data", help="寫入已經抓取的資料")
    parser.add_argument("-s", "--success_log", default="s.log", help="寫入成功抓取的url")
    parser.add_argument("-f", "--fail_log", default='f.log')
    parser.add_argument("-q", "--queue_log", default="q.log", help="")
    parser.add_argument("-t", "--crawl_type", default="newtalk", help="")
    return parser.parse_args()

if __name__ == "__main__":

    args = process_args()

    crawl_page = importlib.import_module("site_parser.{0}".format(args.crawl_type)).crawl_page
    first_url = importlib.import_module("site_parser.{0}".format(args.crawl_type)).first_url


    job_queue.append(first_url)
    news_id_set.add(first_url)

    with open(args.output_file, 'at', encoding='utf8') as data_wf,\
        open(args.success_log, 'at', encoding='utf8') as success_wf,\
        open(args.queue_log, 'at', encoding='utf8') as queue_wf,\
        open(args.fail_log, 'at', encoding='utf8') as fail_wf:

        while len(job_queue) > 0:
            url = job_queue.popleft()
            try:
                time.sleep(1)
                result_json = crawl_page(url)
                data_wf.write(json.dumps(result_json, ensure_ascii=False) + '\n')

                for related_url in result_json['related_news']:
                    #news_id = get_news_id(related_url)
                    news_id = related_url
                    if news_id not in news_id_set:
                        queue_wf.write(json.dumps({"url": related_url}, ensure_ascii=False) + '\n')
                        job_queue.append(related_url)
                        news_id_set.add(news_id)


                success_wf.write(json.dumps({"url": url}, ensure_ascii=False) + '\n')

            except Exception:

                fail_wf.write(json.dumps({"url": url, "error": traceback.format_exc()}, ensure_ascii=False) + '\n')


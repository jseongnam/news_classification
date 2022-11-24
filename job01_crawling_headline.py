from bs4 import BeautifulSoup
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import re
import requests

category = ['Politics','Economic','Social','Culture','IT','World']


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers = headers)
    #print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print(soup)
    title_tags = soup.select('.cluster_text_headline')
    titles= []
    for title_tag in title_tags:
        title = title_tag.text
        title = re.compile('[^가-힣 ]').sub(' ',title)
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns = ['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis ='rows', ignore_index = True)
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawlind_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')
),index=False)
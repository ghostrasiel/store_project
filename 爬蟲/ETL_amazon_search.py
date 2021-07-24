import requests
from bs4 import BeautifulSoup
import re
import os
import time
import random

file = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(f'{file}/Amazon_image') == False: #檢查路徑是否存在
    os.mkdir(f'{file}/Amazon_image') #創建目錄

data = []
search_keyword =['BREAD']
# search_keyword = product_df['COMMODITY_DESC'].dropna().unique()
proxy_ips = ['51.15.227.220:3128' , '106.14.43.86:8080'  , '118.185.38.153:35101' , '58.32.10.253:8090' ]
headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
           "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]


for search in search_keyword:
    print(search)
    s = search.replace(' ','+')
    url = f'https://www.amazon.com/s?k={s}'
    while True:
        ip = random.choice(proxy_ips) #隨機選擇ip
        user_agent = random.choice(headerlist)
        headers = {"User-Agent":user_agent}
        res = requests.post(url , headers=headers , proxies={'http': 'http://' + ip})
        soup = BeautifulSoup(res.text ,'html.parser')
        products = soup.select('div.sg-col-inner')
        try:
            Next =soup.select('div.a-section.a-section.a-spacing-none.a-padding-base')[0].select('li.a-last a')[0]['href']
        except:
            Next = None
        print(Next)
        for product in products:
            data_dict = dict()
            try:
                product_title = product.select('div.a-section.a-spacing-none h2')[0].text.strip()
                product_price = product.select('span.a-price span.a-offscreen')[0].text
                product_comments = product.select('span.a-size-base')[0].text
                product_star = product.select('span.a-declarative a i')[0].text[:3]
                product_url = 'https://www.amazon.com/'+product.select('a.a-link-normal.s-no-outline')[0]['href']
                try:
                    time.sleep(1)
                    ip = random.choice(proxy_ips) #隨機選擇ip
                    user_agent = random.choice(headerlist)
                    headers = {"User-Agent":user_agent}
                    product_res = requests.post(url=product_url , headers=headers , proxies={'http': 'http://' + ip})
                    product_soup = BeautifulSoup(product_res.text , 'html.parser')
                    product_concents = product_soup.find_all('div' ,{"id":"feature-bullets"})[0].find('ul').find_all('li' , id=False)
                    product_concent = [i.text.replace('\n' , '') for i in product_concents]
                    product_concent = ' '.join(product_concent)
                except:
                    product_concent = None
                product_img_url = product.select('img.s-image')[0]['src']
                # product_image =requests.get(product_img_url)
                # time.sleep(1)
                # jpg_title =re.sub('\*|\\|-|\?|"|<|>|\||/|\\\\|:','_', product_title)
                # if os.path.isfile(f'{file}/Amazon_image/{jpg_title}.jpg') == False: 
                #     with open(f'{file}/Amazon_image/{jpg_title}.jpg' , 'wb') as file_obj :
                #         file_obj.write(product_image.content)
                # else :
                #     print('檔案已存在')
                
                data_dict['中分類'] = search
                data_dict['商品名'] = product_title
                data_dict['價格'] = product_price
                data_dict['商品描述'] = product_concent
                data_dict['評論數'] = product_comments
                data_dict['評分'] = product_star
                data_dict['圖片url'] = product_img_url
                # data_dict['圖片名'] = f'{jpg_title}.jpg'
                # data_dict['路徑'] = f'./Amazon_image/{jpg_title}.jpg'
                data.append(data_dict)
                # print(data_dict)
            except:
                pass
        
        if Next != None:
            url = 'https://www.amazon.com'+Next
            time.sleep(random.randint(1 , 3))
        else:
            break

print(len(data))
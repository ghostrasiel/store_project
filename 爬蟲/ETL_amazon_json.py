import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver as sw
from webdriver_manager.chrome import ChromeDriverManager

file = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(f'{file}/Amazon_image') == False: #檢查路徑是否存在
    os.mkdir(f'{file}/Amazon_image') #創建目錄
data = []
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

#<-------------selenium設定-----------
options = Options()
options.add_argument("--disable-notifications") #阻止google視窗通知跳出
options.add_argument('--headless') # 啟動無頭模式
options.add_argument('--disable-gpu') # windows必須加入此行
options.experimental_options['prefs']={'profile.default_content_settings':{'images':2},'profile.managed_default_content_settings':{"images":2}} #不顯示圖片
#------------------------->
url_class =['https://www.amazon.com/gcx/Tools-&-Home-Improvement/gfhz/events?canBeGiftWrapped=false&categoryId=GRFWW21-THI&isLimitedTimeOffer=false&isPrime=false'
 ,'https://www.amazon.com/gcx/College-Electronics/gfhz/events?canBeGiftWrapped=false&categoryId=OTC21-College-Tech&isLimitedTimeOffer=false&isPrime=false&scrollState=eyJpdGVtSW5kZXgiOjAsInNjcm9sbE9mZnNldCI6MTEwLjE0MDYyNX0%3D&sectionManagerState=eyJzZWN0aW9uVHlwZUVuZEluZGV4Ijp7ImFtYWJvdCI6MX19',]
for u in url_class:
    driver = sw.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(u)
    top = driver.find_element_by_xpath('//*[@id="navBackToTop"]/div/span')
    ActionChains(driver).move_to_element(top).perform() #視窗往下移

    soup = BeautifulSoup(driver.page_source , 'html.parser')
    big_tag = [] #大分類
    big_tag_url = [] #大分類url
    for r in range(0 , 10):
        for i in soup.select(f'div#sobe_d_aw_{r}-container ol li'):
            tag_url = 'https://www.amazon.com'+i.select('div.sl-sobe-carousel-sub-card-footer a')[0]['href']
            tag_name = i.select('div.sl-sobe-carousel-sub-card-footer a')[0].text.strip()
            big_tag.append(tag_name)
            big_tag_url.append(tag_url)
            print(tag_name)

    driver.close()

    print(big_tag_url[0]) #喚醒python 
    #進入爬取頁面
    for v in range(0 , len(big_tag)):
        driver = sw.Chrome(ChromeDriverManager().install(), chrome_options=options)
        print(big_tag_url[v])
        driver.get(big_tag_url[v])
        top = driver.find_element_by_xpath('//*[@id="navBackToTop"]/div/span')
        ActionChains(driver).move_to_element(top).perform()
        soup = BeautifulSoup(driver.page_source , 'html.parser')
        categorys = soup.select('div.sc-1wcpl6x-0.cIlFpO ul li')
        medium_tag = [] #中分類
        tag = set() #中分類_tag
        for category in categorys:
            tag.add(category.select('button')[0]['data-test'].split(':')[1])
            medium_tag.append(category.select('button')[0]['data-test'].split(':')[2])
        driver.close()
        count = 1000
        tag = list(tag)

        for mt in medium_tag:
            url = f'https://www.amazon.com/gcx/-/gfhz/api/scroll?canBeGiftWrapped=false&categoryId={tag[0]}&count={count}&isLimitedTimeOffer=false&isPrime=false&offset=0&priceFrom&priceTo&searchBlob&subcategoryIds={tag[0]}%3A{mt}'
            res = requests.get(url=url , headers=headers)
            json_data = json.loads(res.text)
            for i in json_data['asins']:
                a=0
                data_dict = dict()
                product_title = i['title']#品名
                product_price = i['price'] #價格
                product_comments = i['reviewCount'] #評論數
                product_star = i['starRating'] #評分
                product_image =requests.get(i['displayLargeImageURL'])
                time.sleep(1)
                jpg_title =re.sub('\*|\\|-|\?|"|<|>|\||/|\\\\|:','_', product_title)
                if os.path.isfile(f'{file}/Amazon_image/{jpg_title}.jpg') == False: 
                    with open(f'{file}/Amazon_image/{jpg_title}.jpg' , 'wb') as file_obj :
                        file_obj.write(product_image.content)
                else :
                    print('檔案已存在')

                data_dict['商品名'] = product_title
                data_dict['價格'] = product_price
                data_dict['大分類'] = big_tag[v]
                data_dict['中分類'] = mt
                data_dict['評論數'] = product_comments
                data_dict['評分'] = product_star
                data_dict['圖片名'] = f'{jpg_title}.jpg'
                data_dict['路徑'] = f'./Amazon_image/{jpg_title}.jpg'
                data.append(data_dict)

                a = a+1
                if a == 1 :
                    print(a)
                    break

print(data)






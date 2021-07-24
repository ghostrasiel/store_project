import requests
from bs4 import BeautifulSoup
import re
import os

file = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(f'{file}/Amazon_image') == False: #檢查路徑是否存在
    os.mkdir(f'{file}/Amazon_image') #創建目錄

url = 'https://www.amazon.com/dp/B07YQM3NLM/ref=cm_gf_abas_iaac_d_zp0_qd0_v6YFQxMQk0N4yKLcL4hh'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
data={
'dimensions':{"subtype": "impression"," value": 1, "template_name": "Dynamic eCommerce_SD_CI_US_DESKTOP"}
}

res = requests.post(url=url , headers=headers)
soup = BeautifulSoup(res.text , 'html.parser')
product_title = soup.select('span#productTitle')[0].text.strip() #品名
try:
    product_price = soup.select('span#priceblock_ourprice')[0].text.strip() #價格
except:
    product_price = re.search( '\$.+' , soup.select('span#style_name_0_price')[0].text.strip()).group() 
product_class_1 = soup.select('ul.a-unordered-list.a-horizontal.a-size-small li')[0].text.strip() #大分類
product_class_1_1 = soup.select('ul.a-unordered-list.a-horizontal.a-size-small li')[2].text.strip() #中分類
product_comments = re.search('[0-9]*,*[0-9]+',soup.select('span#acrCustomerReviewText')[0].text.strip()).group() #評論數
product_star = soup.select('span#acrPopover')[0].text.strip()[:3] #評分
product_image =requests.get(soup.select('div#imgTagWrapperId img')[0]['src'])
product_concents = soup.find_all('div' ,{"id":"feature-bullets"})[0].find('ul').find_all('li' , id=False)
product_concent = [i.text.replace('\n' , '') for i in product_concents]
product_concent = ' '.join(product_concent)
    

# with open(f'{file}/Amazon_image/{product_title[:4]}.jpg' , 'wb') as file :
#     file.write(product_image.content)


print('商品名:',product_title)
print('價格:',product_price)
print('大分類:',product_class_1)
print('中分類:',product_class_1_1)
print('評論數:',product_comments)
print('評分:',product_star)
# print('圖片名:', f'{product_title[:4]}.jpg')
# print('路徑:', f'./Amazon_image/{product_title[:4]}.jpg')
print('商品描述:' , product_concent)

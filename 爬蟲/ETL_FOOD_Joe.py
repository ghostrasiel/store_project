import requests
from bs4 import BeautifulSoup
import os
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver as sw
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
import time


#<-------------selenium設定-----------
options = Options()
options.add_argument("--disable-notifications") #阻止google視窗通知跳出
options.add_argument('--headless') # 啟動無頭模式
options.add_argument('--disable-gpu') # windows必須加入此行
options.experimental_options['prefs']={'profile.default_content_settings':{'images':2},'profile.managed_default_content_settings':{"images":2}} #不顯示圖片
#------------------------->

file = os.path.dirname(os.path.realpath("__file__"))
if os.path.exists(f'{file}/Trader_joe_image') == False: #檢查路徑是否存在
    os.mkdir(f'{file}/Trader_joe_image') #創建目錄

url='https://www.traderjoes.com/api/graphql'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
,"referer": "https://www.traderjoes.com/home/products/category?categoryId=8" ,"cookie": '_ga=GA1.2.1835251598.1624734482; affinity="84e5c3bccfdad25f"; _gid=GA1.2.1923943996.1624890854; _gat_UA-15671700-1=1'}
cookies = {'affinity':"aa6f525ba9811935"}
data_list=[]
a = 0
driver =sw.Chrome(ChromeDriverManager().install(), chrome_options=options)
for i in range(1 , 30+1):
    data ={ "operationName": "SearchProducts",
    "query": f"query SearchProducts($categoryId: String, $currentPage: Int= {i} , $pageSize: Int = 15, $storeCode: String = \"TJ\", $availability: String = \"1\", $published: String = \"1\")"+"{\n  products(\n    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}\n    currentPage: $currentPage\n    pageSize: $pageSize\n  ) {\n    items {\n      sku\n      item_title\n      category_hierarchy {\n        id\n        name\n        __typename\n      }\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      sales_size\n      sales_uom_description\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      fun_tags\n      item_characteristics\n      __typename\n    }\n    total_count\n    pageInfo: page_info {\n      currentPage: current_page\n      totalPages: total_pages\n      __typename\n    }\n    aggregations {\n      attribute_code\n      label\n      count\n      options {\n        label\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    res = requests.post(url = url , headers=headers , data=json.dumps(data) , cookies=cookies)
    json_datas = json.loads(res.text)['data']['products']['items']
    for json_data in json_datas :
        data_dict={}
        product_title = json_data["item_title"]
        image = "https://www.traderjoes.com/"+json_data["primary_image"]
        price = json_data["retail_price"]
        try:
            product_class_1 =json_data["category_hierarchy"][1]['name']
        except:
            product_class_1 = None
        try:
            product_class_2 =json_data["category_hierarchy"][2]['name']
        except:
            product_class_2 = None
        product_image =requests.get(image)

        jpg_title =re.sub('\*|\\|-|\?|"|<|>|\||/|\\\\|:' , '_' ,product_title)
        if os.path.isfile(f'{file}/Trader_joe_image/{jpg_title}.jpg') == False: 
            with open(f'{file}/Trader_joe_image/{jpg_title}.jpg' , 'wb') as file_obj :
                file_obj.write(product_image.content)
        else :
            print('檔案已存在')
        
        product_id = json_data['sku']
        page_url = f'https://www.traderjoes.com/home/products/pdp/{product_id}'
        driver.get(page_url)
        
        while True:
            try:
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source , 'html.parser')
                try:
                    product_size = soup.select('span.ProductPrice_productPrice__unit__2jvkA')[0].text.replace('/' , '')
                except:
                    product_size = None
                    pass
                try:
                    product_conecnt = soup.select('div.Expand_expand__container__3COzO')[0].text.replace('\n' , '')
                except:
                    product_conecnt = None
                    pass
                break
            except:
                print(product_title)
                pass
            
        
        
        data_dict['商品名']=product_title
        data_dict['規格'] = product_size
        data_dict['描述'] = product_conecnt
        data_dict['價格']=price
        data_dict['大分類']=product_class_1
        data_dict['中分類']=product_class_2
        data_dict['圖片url'] = image
        data_dict['圖片名'] = f'{jpg_title}.jpg'
        data_dict['路徑'] = f'./Amazon_image/{jpg_title}.jpg'
        data_list.append(data_dict)
        a = a+1
        print(a)

driver.close()
print('count:',a)
print(data_list)
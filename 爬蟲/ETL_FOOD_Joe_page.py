import requests
from bs4 import BeautifulSoup
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


url = 'https://www.traderjoes.com/home/products/pdp/063980'
driver =sw.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.get(url)

while True:
    try:
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source , 'html.parser')
        product_size = soup.select('span.ProductPrice_productPrice__unit__2jvkA')[0].text
        # num = soup.select('div.ProductDetails_detail__1P1Sc')[0]
        product_conecnt = soup.select('div.Expand_expand__container__3COzO')[0].text.replace('\n' , '')
        break
    except:
        pass

driver.close()


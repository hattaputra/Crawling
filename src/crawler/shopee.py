import requests
import time
import re
from src import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType


class Shopee:
    def __init__(self):
        self.base_link = 'https://www.shopee.co.id'
        self.shop_link = 'https://shopee.co.id/api/v4/shop/get_shop_detail?username='
        self.shop_image_link = 'https://cf.shopee.co.id/file/'
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

    def get_shop_detail(self, username, result):
        req_session = requests.Session()
        response_data = req_session.get(f"{self.shop_link}{username}", headers=self.headers)

        data_mapping = response_data.json()

        result['user_id'] = data_mapping['data']['userid']
        result['shop_id'] = data_mapping['data']['shopid']
        result['name'] = data_mapping['data']['name']
        result['desc'] = data_mapping['data']['description']
        result['shop_image'] = f"{self.shop_image_link}{data_mapping['data']['account']['portrait']}"
        result['product_count'] = data_mapping['data']['item_count']
        result['follower_count'] = data_mapping['data']['follower_count']
        result['following_count'] = data_mapping['data']['account']['following_count']
        result['location'] = data_mapping['data']['shop_location']

        return result


    def get_browser_open(self, user_id, result):
        """update browser"""
        try:
            list_item_id = []

            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            prox.http_proxy = PROXY

            capabilities = webdriver.DesiredCapabilities.CHROME
            prox.add_to_capabilities(capabilities)

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument('user-agent={0}'.format(self.user_agents))
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options,
                                      desired_capabilities=capabilities)

            driver.get(f"https://shopee.co.id/shop/{user_id}/search?sortBy=ctime")
            time.sleep(2)

            max_page = driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div/div[2]/div/div[1]/div[2]/div/span[2]').text

            for page in range(int(max_page)):
                driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div/div[2]/div/div[1]/div[2]/button[2]').click()
                time.sleep(3)

                row_tag = driver.find_elements_by_xpath('//*[@id="main"]/div/div[3]/div/div/div[2]/div/div[2]/div/div')

                product_index = 1
                for item in row_tag:
                    product = {}

                    itemId = item.find_element_by_tag_name('a').get_attribute('href')
                    productName = item.find_element_by_xpath('//*/a/div/div/div[2]/div/div[1]/div').text

                    try:
                        price_current = item.find_element_by_xpath(f'//*/div[{product_index}]/a/div/div/div[2]/div[2]/div/span[2]').text
                        price_ori = item.find_element_by_xpath(f'//*/div[{product_index}]/a/div/div/div[2]/div[2]/div').text

                        price_current = re.sub(r"\D", '', price_current)
                        price_ori = re.sub(r"\D", '', price_ori)
                    except:
                        price_current = item.find_element_by_xpath(f'//*/div[{product_index}]/a/div/div/div[2]/div[2]/div').text
                        price_ori = item.find_element_by_xpath(f'//*/div[{product_index}]/a/div/div/div[2]/div[2]/div').text

                        price_current = re.sub(r"\D", '', price_current)
                        price_ori = re.sub(r"\D", '', price_ori)

                    product['item_id'] = re.sub(r"\b(?:(?!.\d\?)\w|\W)+\b", '', itemId)
                    product['product_name'] = productName
                    product['price_ori'] = price_ori
                    product['price_current'] = price_current

                    req_session = requests.Session()
                    response_data = req_session.get(f"https://shopee.co.id/api/v2/item/get?itemid={product['item_id']}&shopid=37146675", headers=self.headers)

                    data_mapping = response_data.json()

                    list_image = []

                    for img in data_mapping['item']['images']:
                        list_image.append(f"https://cf.shopee.co.id/file/{img}")

                    product['desc'] = data_mapping['item']['description']
                    product['stock'] = data_mapping['item']['normal_stock']
                    product['product_image'] = list_image

                    list_item_id.append(product)

            driver.close()
            print(len(list_item_id))
            result['product_detail'] = list_item_id

        except Exception as e:
            raise e

        return result

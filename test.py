from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def setup_driver():
    # 设置Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def search_google_maps(driver, keyword, lat, lng, zoom):
    # 构建谷歌地图搜索URL
    url = f"https://www.google.com/maps/search/{keyword}/@{lat},{lng},{zoom}z"
    driver.get(url)
    time.sleep(5)

def extract_info(driver):
    # 使用BeautifulSoup提取信息
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stores = []

    for store_div in soup.find_all("div", class_="Nv2PK THOPZb CpccDe"):
        store = {}
        # 商店名称
        store['name'] = store_div.find("a").get("aria-label")
        
        # 评分
        rating_span = store_div.find("span", {"role": "img"})
        if rating_span:
            store['rating'] = rating_span.get("aria-label").split(" ")[0]  # 获取评分数值
            store['reviews'] = rating_span.find("span", class_="UY7F9").text.strip("()")  # 获取评价数量

        # 商店类型和地址
        details_spans = store_div.find_all("span")
        store['type'] = details_spans[0].text if len(details_spans) > 0 else ""
        store['address'] = details_spans[2].text if len(details_spans) > 2 else ""

        # 营业时间和联系电话
        open_info = store_div.find("div", class_="W4Efsd").find_all("span")[0].text
        phone_info = store_div.find("div", class_="W4Efsd").find_all("span")[1].text if len(store_div.find("div", class_="W4Efsd").find_all("span")) > 1 else ""

        store['open_info'] = open_info.split(" ⋅ ")[-1] if " ⋅ " in open_info else open_info
        store['phone'] = phone_info

        stores.append(store)
    return stores

def main():
    keyword = "shop"
    lat, lng = 22.3338997, 114.1022003
    zoom = 13

    driver = setup_driver()
    search_google_maps(driver, keyword, lat, lng, zoom)
    results = extract_info(driver)
    driver.quit()

    for result in results:
        print(result)

if __name__ == "__main__":
    main()

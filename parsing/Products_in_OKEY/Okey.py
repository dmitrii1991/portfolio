import bs4
import datetime
import re
from selenium import webdriver
import time

re_find_price = r'(data-price=(\"\d*\.\d*\"))'
re_find_name = r'(title=\".*\")'
i = 0
time1 = datetime.datetime.now().date()

with open(str(time1) + '.txt', 'w', encoding='utf-8') as file:
    browser = webdriver.Chrome()
    while True:
        page_link = "https://www.okeydostavka.ru/spb/molochnye-produkty-syry-iaitso-16100-20/molochnye-produkty-16101-20/moloko-i-slivki-16110-20#facet:&productBeginIndex:" + str(i) + "&orderBy:2&pageView:grid&minPrice:&maxPrice:&pageSize:&"
        browser.get(page_link)
        time.sleep(5)
        response_text = browser.page_source
        soup = bs4.BeautifulSoup(response_text, features="html.parser")
        elems = soup.select("div[class='product ok-theme']")
        for elem in elems:
            milk = bs4.BeautifulSoup(str(elem), features="html.parser")
            price = re.search(re_find_price, str(milk.select('a[class="btn cartIcon"]'))).group().split('=')[1]
            name = re.search(re_find_name, str(milk)).group().split('=')[1]
            file.write(f"{name}, {price}\n")
        print("Собрано: ", len(elems))
        if len(elems) == 72:
            i += 72
        else:
            break

import bs4
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pprint
import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)  # отключение протоколирования

def GetOkeyPrice(town: str):
    """
    Выводит название товара и цены
    :param town: spb/msk
    :return:
    """
    logging.info(f'Start GetOkeyPrice{town}')
    time_for_file = datetime.datetime.now().date()
    browser = webdriver.Chrome()


    def GetCategory(browser):
        '''
        Не посредственно получает ссылки и названия категорий для анализа цен в виде списка
        :param browser: webdriver
        :return: list
        '''
        logging.info(f'start GetCategory()')
        re_find_href = r'(href="(\S*)")'
        re_find_name_category = r'([А-Яа-я]+(\s{1}|([,]\s{1})))+'
        categories_list = []
        # выполняем анализ цен и выдергиваем названия категорий и их ссылки
        homePageOkey = 'https://www.okeydostavka.ru/'
        browser.get(homePageOkey + str(town))
        mainPageHIML = browser.page_source
        soup = bs4.BeautifulSoup(mainPageHIML, features="html.parser")
        categories = soup.select("li[data-parent='allDepartmentsMenu'] > a[class='link menuLink']")
        logging.info(f'Categories: {len(categories)}')
        for category in categories:
            name_category = re.search(re_find_name_category, str(category)).group()
            href = re.search(re_find_href, str(category)).group().split('="')[1]
            categories_list.append([name_category, href])
        logging.info(f'End GetCategory()')
        return categories_list


    def Get_prices(browser, href):
        '''
        Вытягивает цену, название товара
        :param browser:
        :param href:
        :return:
        '''
        re_find_pages = r'(Перейти к странице \d*)'
        i = 72
        all_prices_subcategory = {}
        browser.get("https://www.okeydostavka.ru" + href[:-1])
        HIML_whith_prices = browser.page_source
        # ищем сколько всего страниц на сайте. Тк на сайте по умолчанию стоит 36 ли 72 позиции, то просим показать
        # максимально возможный вариант: кол-во стр * 72
        try:
            end_page = re.findall(re_find_pages, str(HIML_whith_prices))[-1]
        except IndexError:
            end_page = pages = 0
        if end_page:
            pages = int(end_page.split(' ')[-1])
            i = 72 * pages
        find_number = '#facet:&productBeginIndex:0&orderBy:2&pageView:grid&minPrice:&maxPrice:&pageSize:' + str(i) + '&'
        logging.info(f'pages: {pages}')
        re_find_price = r'(data-price=(\"\d*\.\d*\"))'
        re_find_name = r'(title=\".*\")'
        browser.get("https://www.okeydostavka.ru" + href[:-1] + find_number)
        try:
            element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bodycontent")))
            element = WebDriverWait(browser, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "bodycontent")))
        except TimeoutException:
            pass
        finally:
            HIML_whith_prices = browser.page_source

        soup = bs4.BeautifulSoup(HIML_whith_prices, features="html.parser")
        elems = soup.select("div[class='product ok-theme']")
        for elem in elems:
            try:
                product = bs4.BeautifulSoup(str(elem), features="html.parser")
                price = re.search(re_find_price, str(product.select('a[class="btn cartIcon"]'))).group().split('=')[1]
                name = re.search(re_find_name, str(product)).group().split('=')[1]
                all_prices_subcategory[name] = price[1:-1]
            except AttributeError:
                name, price = "неопределен", 0
        logging.info(f'items= : {len(elems)}')
        return all_prices_subcategory


    def Subcategory(browser, categories_list: str):
        re_find_href = r'(href=\"[/spb/](\S*)\")'
        re_find_name_category = r'(([А-Яа-я]+(\s{1}|([,]\s{1})))+[А-Яа-я]+)|[А-Яа-я]+'
        category_prices = {}
        # выполняем анализ цен и выдергиваем название подкатегорий и их ссылки
        for name_category, href in categories_list:
            homePageCategory = "https://www.okeydostavka.ru" + href[:-1]
            browser.get(homePageCategory)
            PageHIMLCategory = browser.page_source
            soup = bs4.BeautifulSoup(PageHIMLCategory, features="html.parser")
            subcategories = soup.select("div[class='row categories'] > div[class='col-xs-3 col-lg-2 col-xl-special']")
            logging.info(f'<<<< {name_category} >>>>')
            logging.info(f'subcategories:  {len(subcategories)}')
            all_subcategory_prices = {}
            if len(subcategories) == 0:
                all_prices = Get_prices(browser, href[:])
                category_prices[name_category] = all_prices
            else:
                for subcategory in subcategories:
                    name_subcategory = re.search(re_find_name_category, str(subcategory)).group()
                    subcategory_href = re.search(re_find_href, str(subcategory)).group().split('="')[1]
                    logging.info(f'start Get_prices(---{name_subcategory}---)')
                    all_prices = Get_prices(browser, subcategory_href)
                    all_subcategory_prices[name_subcategory] = all_prices
                category_prices[name_category] = all_subcategory_prices
        with open(f"{str(time_for_file)}.py", "w", encoding='utf-8') as write_file:
            write_file.write('cats = ' + pprint.pformat(category_prices) + '\n')

    list_ = GetCategory(browser)
    Subcategory(browser, list_)
    logging.info(f'End GetOkeyPrice{town}')


if __name__ == '__main__':
    logging.info('Start programm')
    GetOkeyPrice('spb')
    logging.info('End programm')
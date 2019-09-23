import urllib.request
import xml.dom.minidom

valute_min = valute_max = dict()

url = "http://www.cbr.ru/scripts/XML_daily.asp"
file = urllib.request.urlopen(url)
data = file.read()
dom = xml.dom.minidom.parseString(data)
dom.normalize()

template = '''
{}
Цифровой код валюты: {}
Буквенный код валюты: {}
Наименоване валюты: {}
Размер 1 ед. = {} руб. 
'''

valutes = dom.getElementsByTagName("Valute")
for valute in valutes:
    if not valute_min:
        valute_min['NumCode'] = valute.getElementsByTagName('NumCode')[0].firstChild.data
        valute_min["CharCode"] = valute.getElementsByTagName("CharCode")[0].firstChild.data
        valute_min["Name"] = valute.getElementsByTagName("Name")[0].firstChild.data
        value = valute.getElementsByTagName("Value")[0].firstChild.data
        nominal = valute.getElementsByTagName("Nominal")[0].firstChild.data
        valute_min["Value"] = round(float(value.replace(',', '.')) / int(nominal), 2)
        valute_max = valute_min.copy()
    else:
        value = valute.getElementsByTagName("Value")[0].firstChild.data
        nominal = valute.getElementsByTagName("Nominal")[0].firstChild.data
        val = round(float(value.replace(',', '.')) / int(nominal), 2)
        if val > valute_max["Value"]:
            valute_max['NumCode'] = valute.getElementsByTagName('NumCode')[0].firstChild.data
            valute_max["Name"] = valute.getElementsByTagName("Name")[0].firstChild.data
            valute_max["CharCode"] = valute.getElementsByTagName("CharCode")[0].firstChild.data
            valute_max["Value"] = val
        elif val < valute_min["Value"]:
            valute_min['NumCode'] = valute.getElementsByTagName('NumCode')[0].firstChild.data
            valute_min["Name"] = valute.getElementsByTagName("Name")[0].firstChild.data
            valute_min["CharCode"] = valute.getElementsByTagName("CharCode")[0].firstChild.data
            valute_min["Value"] = val

print(template.format('Самая дорогая валюта', valute_max['NumCode'], valute_max["CharCode"], valute_max["Name"],
                      valute_max["Value"]))
print(template.format('Самая дешевая валюта', valute_min['NumCode'], valute_min["CharCode"], valute_min["Name"],
                      valute_min["Value"]))

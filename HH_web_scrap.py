import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json

headers = Headers(browser="chrome", os="win")
hh_data = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers.generate()).text
hh_soup = BeautifulSoup(hh_data, 'lxml')
vacancies = hh_soup.find_all("div", class_="vacancy-serp-item-body__main-info")
keywords = ["Django", "Flask"]
vacancy_dict = {}
n = 0

for vacancy_info in vacancies:
    n += 1
    tag_link = vacancy_info.find("a", class_="serp-item__title")["href"]
    req1 = requests.get(tag_link, headers=headers.generate())
    description_soup = BeautifulSoup(req1.text, "lxml")
    tag_salary = description_soup.find(
        "span", class_="bloko-header-section-2 bloko-header-section-2_lite"
    )
    tag_city = vacancy_info.find(
        "div", {"data-qa": "vacancy-serp__vacancy-address"}, class_="bloko-text"
    )
    tag_position = vacancy_info.find("a", class_="serp-item__title")
    tag_company = vacancy_info.find(
        "a",
        {"data-qa": "vacancy-serp__vacancy-employer"},
        class_="bloko-link bloko-link_kind-tertiary",
    )
    tag_position_description = description_soup.find(
        "div", {"data-qa": "vacancy-description"})
    for word in keywords:
        if word in tag_position_description.text:
            vacancy_dict[f"Vacancy {n}:"] = {
                "Должность:": tag_position.text.replace("\xa0", " "),
                "Компания:": tag_company.text.replace("\xa0", " "),
                "Город:": tag_city.text.replace("\xa0", " "),
                "ЗП:": tag_salary.text.replace("\xa0", " "),
                "Ссылка:": tag_link,
            }
        else:
            continue


with open("data.json", "w", encoding="utf-8") as file:
    json.dump(vacancy_dict, file, indent=2, sort_keys=False, ensure_ascii=False)

pprint(vacancy_dict)



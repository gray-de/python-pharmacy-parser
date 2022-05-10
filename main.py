import re
from bs4 import BeautifulSoup
import requests
import csv
import time


url = "https://www.spr.ru/all/apteki/"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
prot = "http://"

req = requests.get(url=url)

soup = BeautifulSoup(req.text, "html.parser")
table = soup.find("section", class_="moduleFirmsListWide").find_all("div", class_="item")

sait_list = []

for item in table:
    sait = item.find("div", class_="itemFlexInfo").find("a").get("href")
    sait1 = prot + sait[2:]
    sait_list.append(sait1)

title_list = ["Название компании","Телефон(Ссылка)","Адрес", "Хорошие оценки", "Плохие оценки", "Ссылка"]

with open("apteka_table.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(title_list)

for item in sait_list:
    time.sleep(1)
    def test_request(item, retry = 5):
        try:
            req3 = requests.get(url = item, headers = headers)
        except Exception:
            if retry:
                print(f"retry = {retry} => {url}")
                return test_request(item, retry = retry - 1)
            else:
                raise
        else:
            return req3
    try:
        req3 = test_request(item)
        soup3 = BeautifulSoup(req3.text, "html.parser")
    except Exception:
        continue

    comp_name = soup3.find("h1", class_="firstHeader")

    if comp_name == None:
        comp_name = soup3.find("h1", class_="HeaderFirst").text
    else:
        comp_name = soup3.find("h1", class_="firstHeader").text

    tel = soup3.find("div", class_="firstPhone")

    if tel == None:
        if tel == None:
            tel = "Не имеется"
        else:
            tel = prot + str(soup3.find("div", class_="allBtn_adaptive firm_link").find("a"))
    else:
        tel = soup3.find("div", class_="firstPhone").text

    pre_address = soup3.find("div", class_="contactBox_right")
    address = ""
    if pre_address == None:
        address = None
    else:
        address = soup3.find("div", class_="contactBox_right").find("div", class_="contactBox_side__el").find("a").text

    if address == None:
        if address == None:
            address = "Не имеется"
        else:
            pass
    else:
        address = soup3.find("div", class_="contactBox_right").find("div", class_="contactBox_side__el").find("a").text

    good_mark = soup3.find("div", class_="good_review")
    if good_mark == None:
        link = item + "reviews/"
        req = requests.get(url = link)
        soup = BeautifulSoup(req.text, "html.parser")
        good_mark = soup.find("div", class_="reviewsListPositive")
        if good_mark == None:
            continue
        else:
            good_mark = soup.find("div", class_="reviewsListPositive").find("span", class_="listReviewsQuantity").text
    else:
        good_mark = soup3.find("div", class_="good_review").text

    bad_mark = soup3.find("div", class_="bad_review")
    if bad_mark == None:
        link = item + "reviews/"
        req = requests.get(url=link)
        soup = BeautifulSoup(req.text, "html.parser")
        bad_mark = soup.find("div", class_="reviewsListNegative")
        if bad_mark == None:
            continue
        else:
            bad_mark = soup.find("div", class_="reviewsListNegative").find("span", class_="listReviewsQuantity").text
    else:
        bad_mark = soup3.find("div", class_="good_review").text


    with open("apteka_table.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([comp_name, tel, address, good_mark, bad_mark, item])











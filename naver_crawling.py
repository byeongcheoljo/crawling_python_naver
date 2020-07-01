# -*-coding:utf-8 -*-
# -*-coding:cp949 -*-
import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
from tqdm import tqdm
from tqdm import trange
from random import randint
import math
import re
from fake_useragent import UserAgent

date = datetime.date(2016, 5, 28)
date_now = datetime.datetime.now()
query = "고혈압"

MAX_SLEEP_TIME = 15
rand_value = randint(1, MAX_SLEEP_TIME)
total_end = 0
def total_link(query, start_date, end_date):
    global total_end
    page = 1
    # end_page = 2
    href_links_list = []
    ua = UserAgent()
    headers = {"User-Agent":ua.random}

    url2= "https://kin.naver.com/search/list.nhn?sort=none&query="+query+"&period="+str(start_date)+".%7C"+str(end_date)+".&section=kin&page=2"
    res1 = requests.get(url2, headers=headers)
    soup1 = BeautifulSoup(res1.text, "html.parser")
    end_page = soup1.find("span",class_="number").find_all("em")[0].get_text()
    print("end1",end_page)
    end_page = end_page.split("/")
    end_page = math.floor(int(end_page[1].replace(",",""))/10)
    print("end2",end_page)


    if(end_page >= 150):
        end_page = 150
    elif end_page >= 90:
        end_page = end_page - 4
    elif end_page > 60:
        end_page = end_page - 3
    elif end_page > 10:
        end_page = end_page - 2
    else:
        end_page = end_page

    end_page = end_page
    print("end3",end_page)
    total_end += end_page
    print (total_end)

    url1 = "https://kin.naver.com/search/list.nhn?sort=none&query="+query+"&period="+str(start_date)+".%7C"+str(end_date)+".&section=kin&page={}".format(end_page)
    res2 =  requests.get(url1, headers=headers)
    soup1 = BeautifulSoup(res1.text, "html.parser")
    end_page = math.floor(int(end_page))
    print("end5",end_page)

    while True:
        try:

            url = "https://kin.naver.com/search/list.nhn?sort=none&query="+query+"&period="+str(start_date)+".%7C"+str(end_date)+".&section=kin&page={}".format(page)
            headers={"User-Agent":ua.random}
            res = requests.get(url, headers=headers)

            soup = BeautifulSoup(res.text, "html.parser")

            href_links = soup.find("ul", class_="basic1").find_all("li")

            if page > int(end_page):
                break
            page += 1
            for href in href_links:
                href_link = href.find("a")["href"]
                href_links_list.append(href_link)

        except Exception as ex:
            print("error", ex)

    return href_links_list

title_content_answer = []
answer_list = []
title_list = []
content_list = []
reg_dates = []


title_content_answer_month = []
answer_list_month = []
title_list_month = []
content_list_month = []
reg_dates_month = []
while True:

    start_date = (date.strftime("%Y.%m.%d"))
    year,month,day = start_date.split(".")

    if date.year >= 2015:
        date  = date + datetime.timedelta(days=3)
    elif date.year >= 2010:
        date = date + datetime.timedelta(days=5)
    else:
        date = date + datetime.timedelta(days=30)
    end_date = (date.strftime("%Y.%m.%d"))

    if int(year) >= date_now.year and int(month) >= date_now.month and int(day) > date_now.day:
        break
    print(start_date)
    print(end_date)

    links_knowledge_in = total_link(query, start_date, end_date)
    date = date + datetime.timedelta(days=1)


    for ln in tqdm(range(len(links_knowledge_in))):

        try:
            cleanr = re.compile('<.*?>|P {MARGIN-TOP: 2px; MARGIN-BOTTOM: 2px}|Untitled')
            res = requests.get(links_knowledge_in[ln])
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.select("div.title")
            title = (title[0].text.strip())
            title = re.sub(cleanr, '', title)
        except Exception as ex:
            title = title
        try:
            content = soup.select("div.c-heading__content")
            content = content[0].text.strip()
            content = re.sub(cleanr, '', content)
        except Exception as ex:
            if len(content) == 0:
                content = " "
            else:
                content = content
                content = re.sub(cleanr, '', content)


        try :
            reg_date = soup.select(".c-userinfo__info")
            reg_date = reg_date[0].text.replace("작성일","")
            reg_dates.append(reg_date)
            reg_dates_month.append(reg_date)

        except Exception as ex:
            reg_date = " "
            reg_dates.append(reg_date)
        try:
            answer = soup.select("div._endContents")[0]
            answer = answer.select("div._endContentsText")

            answer = answer[0].text.strip()
            answer = re.sub(cleanr, '', answer)
            pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
            answer = re.sub(pattern, '', answer)
            pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
            answer = re.sub(pattern, '', answer)
            pattern = '[^\w\s]'
            answer = re.sub(pattern, '', answer)

            answer_list.append(answer)
            answer_list_month.append(answer)


        except Exception as ex:
            title = title

            if len(answer) == 0:

                answer_list.append(" ")
            else:
                answer = answer
                answer = re.sub(cleanr, '', answer)
                pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
                answer = re.sub(pattern, '', answer)
                pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
                answer = re.sub(pattern, '', answer)
                pattern = '<[^>]*>'
                answer = re.sub(pattern, '', answer)

        title_list.append(title)
        content_list.append(content)

        title_list_month.append(title)
        content_list_month.append(content)

        title_content_answer_month = {"question_title": title_list_month, "question_content": content_list_month, "answer_content": answer_list_month,"reg_date":reg_dates_month}
        pd_test = pd.DataFrame(title_content_answer_month)
        pd_test.to_csv("D:/test_python/고혈압/"+query + "_KnowledgeIn_"+year+"_"+month+"_"+day+".csv", encoding='utf-8-sig')

    title_content_answer_month = []
    answer_list_month = []
    title_list_month = []
    content_list_month = []
    reg_dates_month = []
title_content_answer = {"question_title": title_list, "question_content": content_list, "answer_content": answer_list,"reg_date":reg_dates}
# total = title_content_answer
pd_test = pd.DataFrame(title_content_answer)
pd_test.to_csv("D:/test_python/고혈압/"+query + "_KnowledgeIn.csv", encoding='utf-8-sig')
print("title", len(title_list))
print("content", len(content_list))
print("answer_list", len(answer_list))

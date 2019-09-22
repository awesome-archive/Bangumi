# -*- coding: utf-8 -*-
import os
import re
import json
import time
from multiprocessing.pool import ThreadPool

import requests
from bs4 import BeautifulSoup
from app.models.crud import Database
from urllib.request import urlretrieve

# database_videos = Database.get_videos()

page_max_num_list = [64, 919, 421]
links = []
for index in reversed(range(1, page_max_num_list[0])):
    links.append("http://www.007hd.com/dongman/index_" + str(index) + "_____hits__1.html")
for index in reversed(range(1, page_max_num_list[1])):
    links.append("http://www.007hd.com/dianying/index_" + str(index) + "_____hits__1.html")
for index in reversed(range(1, page_max_num_list[2])):
    links.append("http://www.007hd.com/dianshiju/index_" + str(index) + "_____hits__1.html")

os.mkdir("./temp/")


def get_videos(url_page):
    print(url_page)

    try:
        req = requests.get(url_page, timeout=15)
    except:
        return

    req.encoding = "utf8"
    soup = BeautifulSoup(req.text, "lxml")
    links = soup.select(
        "body > div.movie-wrap > div.container > div > div.filtrate > div > div > div.filtrate-container > div.filtrate-container-body > div > ul > li > a")
    inner_links = []
    for link in links:
        inner_links.append("http://www.007hd.com" + link.get("href"))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    for inner_one in inner_links:

        try:
            req = requests.get(inner_one, timeout=15)
        except:
            continue

        req.encoding = "utf8"
        soup = BeautifulSoup(req.text, "lxml")

        if len(soup.select("ul.playurl > li")) != 0:
            video = dict()
            video["name"] = str(soup.select("div.art-title > h1")[0].string)
            video["logo"] = str(soup.select("div.details-con1 > a > img")[0].get("data-url"))

            try:
                urlretrieve(video["logo"], './temp/' + str(time.time()) + '.png')
            except:
                continue

            video["links"] = ""
            video_link = "http://www.007hd.com" + soup.select("ul.details-con2-list > li > a")[0].get("href")

            try:
                req = requests.get(video_link, headers=headers, timeout=15)
            except:
                continue

            req.encoding = "utf8"
            if req.text.find(".m3u8") == -1:
                continue

            links = re.findall(r"ff_urls='(.*?)'", req.text)
            video_link_json = json.loads(links[0])
            try:
                for url in video_link_json["Data"][0]["playurls"]:
                    video["links"] += url[0] + "@" + url[1] + "\r\n"
                video["links"] = str(video["links"][:-2])
            except:
                continue

            video["actors"] = ""
            actors_many = soup.select(
                "body > div.movie-wrap > div.details-body > div.details-left.fl > div.details-con1 > div > div.synopsis > p:nth-child(2) > a")
            try:
                for actors in actors_many:
                    video["actors"] += actors.string + " / "
                video["actors"] = str(video["actors"][:-3])
            except:
                pass

            video["director"] = ""
            video["tags"] = ""
            try:
                zha_links = soup.select("div.details-con1 > div > div.synopsis > p:nth-child(1) > a")
                for zha in zha_links:
                    video["tags"] += zha.string + " / "
                temp = video["tags"][:-3]
                video["tags"] = str(temp[0:temp.rfind("/") - 1])
                video["director"] = str(temp[temp.rfind("/") + 2:])
            except:
                pass

            video["area"] = str(soup.select("div.details-content > div.synopsis > p:nth-child(3) > a")[0].string)
            p = soup.select("div.synopsis > p:nth-child(1)")[0].text
            video["language"] = str(p.replace("	", "")[-2:])
            y = soup.select("div.details-content > div.synopsis > p:nth-child(3)")[0].text
            y = y.replace(" ", "")
            video["year"] = str(y[y.find("上映") + 4:y.find("更新")])

            if url_page.find("dongman") != -1:
                video["vclass"] = "动漫"
            elif url_page.find("dianying") != -1:
                video["vclass"] = "电影"
            elif url_page.find("dianshiju") != -1:
                video["vclass"] = "电视剧"

            video["status"] = ""
            try:
                video["status"] = str(soup.select("div.details-con1 > div > div.vod_t > font")[0].string)
            except:
                pass

            video["desc"] = str(soup.select("div.details-con1 > div > div.synopsis > p.synopsis-article")[0].text)

            for k, v in video.items():
                if not v:
                    video[k] = ""

            # for video_data in database_videos:
            #     if video["name"] == video_data.name:
            #         if video["links"] != video_data.links:
            #             Database.update_video_2(video_data.id, video)
            #             break
            # else:
            #     Database.create_video_2(video)

            Database.create_video_2(video)
            print(video)


pool = ThreadPool(processes=10)
results = pool.map(get_videos, links)
pool.close()
pool.join()

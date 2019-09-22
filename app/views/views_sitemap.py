# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.models.crud import Database


class SitemapHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        videos = Database.get_videos()
        data = dict()
        tags = []
        for video in videos:
            for tag in video.tags.split(" / "):
                if tag:
                    tags.append(tag)
        tags = {}.fromkeys(tags).keys()

        data["tags"] = []
        index = 4
        for tag in tags:
            index += 1
            temp = dict()
            temp["index"] = index
            temp["name"] = tag
            data["tags"].append(temp)

        self.render("sitemap.html", data=data)

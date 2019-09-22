# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class SearchHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        q = self.get_argument("q", None)
        data = dict()
        if q:
            data["query"] = q
            data["site_title"] = "搜索_" + q + "_下的视频列表_" + self.site_name
            videos = Database.query_videos(q)
            data["video"] = self.page(videos)
            self.html("normal/search.html", data=data)
        else:
            data["site_name"] = self.site_name
            self.html("404.html", data=data)

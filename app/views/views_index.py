# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class IndexHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        data["site_title"] = self.site_name
        data['dy_hot_video'] = Database.get_hot_videos("电影")
        data['dsj_hot_video'] = Database.get_hot_videos("电视剧")
        data['dm_hot_video'] = Database.get_hot_videos("动漫")
        self.html("normal/index.html", data=data)

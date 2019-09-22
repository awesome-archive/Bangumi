# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class VClassHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        vclass = ""
        tag = self.get_argument("n", None)
        type = self.get_argument("t", None)
        if type == "dy":
            vclass = "电影"
        elif type == "dm":
            vclass = "动漫"
        elif type == "dsj":
            vclass = "电视剧"

        data = dict()
        if type:
            data["type"] = type
            data["vclass"] = vclass
            data["site_title"] = "最新" + vclass + "_推荐" + vclass + "_" + self.site_name
            videos = Database.get_vclass_videos(vclass)
            data["tag"] = None
            if tag:
                data["tag"] = tag
                videos = Database.get_vclass_tag_videos(vclass, tag)
                data["site_title"] = "标签_" + tag + "_最新" + vclass + "_推荐" + vclass + "_" + self.site_name
            data["video"] = self.page(videos)
            self.html("normal/vclass.html", data=data)
        else:
            data["site_name"] = self.site_name
            self.render("404.html", data=data)

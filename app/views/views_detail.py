# -*- coding: utf-8 -*-
import random

import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class DetailHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        id = self.get_argument("id", None)
        if id:
            video = Database.get_video(id)
            data = dict()
            data["site_title"] = video.name + "_" + self.site_name
            data['video'] = video
            data['hot'] = random.randint(45, 99)
            data['tags'] = video.tags.replace(' ', '').split("/")
            subvideo = []

            for sub in video.links.split("\r\n"):
                try:
                    temp = dict()
                    temp["episode"] = sub.split("@")[0]
                    temp["link"] = sub.split("@")[1]
                    subvideo.append(temp)
                except:
                    break

            data['sub_video'] = subvideo
            self.html("normal/detail.html", data=data)

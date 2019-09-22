# -*- coding: utf-8 -*-
import random

import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class PlayHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        id = self.get_argument("id", None)
        vsb = self.get_argument("vsb", None)
        Database.add_hot(id)
        if id and vsb:
            video = Database.get_video(id)
            data = dict()

            data["site_title"] = "正在播放_" + video.name + "_" + vsb + "_" + self.site_name
            data['video'] = video

            subvideo = []
            curvideo = []
            for sub in video.links.split("\r\n"):
                temp = dict()
                temp["episode"] = sub.split("@")[0]
                temp["link"] = sub.split("@")[1]
                if temp["episode"] == vsb:
                    curvideo.append(temp)
                subvideo.append(temp)

            data['video'] = video
            data["online"] = random.randint(1, 50)
            data['sub_video'] = subvideo
            data['cur_video'] = curvideo[0]
            self.html("normal/play.html", data=data)

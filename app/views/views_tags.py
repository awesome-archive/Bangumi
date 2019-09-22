# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.tools.orm import DBConnetor
from app.models.models import Video


class TagsHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        tag = self.get_argument("n", "")
        data = dict()
        data["site_title"] = "标签_" + tag + "下的视频_" + self.site_name
        session = DBConnetor.db()
        try:
            model = session.query(Video).filter(Video.tags.like('%{}%'.format(tag))).order_by(Video.createdAt.desc())
            data['video'] = self.page(model)
            data['tag'] = tag
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        self.html("normal/tags.html", data=data)

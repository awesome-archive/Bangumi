# -*- coding: utf-8 -*-
import json
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.tools.rd import rd


class DMHandler(CommonHandler):
    def check_xsrf_cookie(self):
        return True

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        id = self.get_argument("id", None)
        if id:
            key = 'dm{}'.format(id)
            if rd.llen(key):
                data = rd.lrange(key, 0, 3000)
                data = [json.loads(v) for v in data]
                res = {
                    "code": 0,
                    "data": [
                        [v['time'], v['type'], v['color'], v['author'], v['text']]
                        for v in data
                    ]
                }
            else:
                res = {
                    "code": 0,
                    "data": []
                }
            self.write(res)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        data = self.request.body
        data = json.loads(data.decode("utf-8"))
        rd.lpush('dm{}'.format(data['id']), json.dumps(data))
        self.write(dict(
            code=0,
            data=data
        ))

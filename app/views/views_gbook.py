# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent

from app.tools.orm import DBConnetor
from app.models.crud import Database
from app.tools.forms import GbookForm
from app.views.views_common import CommonHandler
from app.models.models import Gbook


class GbookHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        data["site_title"] = "留言板_" + self.site_name
        session = DBConnetor.db()
        try:
            model = session.query(Gbook).order_by(Gbook.createdAt.desc())
            data['gbook'] = self.page(model)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        self.html("normal/gbook.html", data=data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        gbooks = None
        sendflag = False
        if self.request.remote_ip:
            try:
                gbooks = Database.get_gbook_for_ip(self.request.remote_ip)
            except:
                pass

        if len(gbooks) == 3:
            _a = str(gbooks[0].createdAt)[:-3]
            _b = str(gbooks[1].createdAt)[:-3]
            _c = str(gbooks[2].createdAt)[:-3]
            if _a == _b == _c:
                sendflag = True
                Database.create_black(self.request.remote_ip)
                Database.delete_gbook(self.request.remote_ip)

        form = GbookForm(self.fdata)
        res = dict(code=0)
        if (not sendflag) and form.validate() and (form.chkcode.data.lower() == self.session["chkcode"].lower()):
            if Database.create_gbook(form, self.request.remote_ip):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        self.write(res)

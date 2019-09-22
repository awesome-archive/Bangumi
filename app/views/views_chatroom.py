# -*- coding: utf-8 -*-
import json
import datetime
from sockjs.tornado import SockJSConnection
from app.models.crud import Database


class ChatRoomHandler(SockJSConnection):
    waiters = set()

    def on_open(self, request):
        self.waiters.add(self)

    def on_message(self, message):
        try:
            data = json.loads(message)
            data['datenow'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)

            sendflag = False
            if data['code'] == 2:
                msgs = Database.get_msg_for_ip(self.session.conn_info.ip)
                if len(msgs) == 5:
                    _a = str(msgs[0].createdAt)[:-3]
                    _b = str(msgs[1].createdAt)[:-3]
                    _c = str(msgs[2].createdAt)[:-3]
                    _d = str(msgs[3].createdAt)[:-3]
                    _e = str(msgs[4].createdAt)[:-3]

                    if _a == _b == _c == _d == _e:
                        sendflag = True
                        Database.create_black(self.request.remote_ip)
                        Database.delete_gbook(self.request.remote_ip)

                if not sendflag:
                    Database.create_msg(int(data['vid']), data["vsb"], content, self.session.conn_info.ip)

            self.broadcast(self.waiters, content)
        except:
            pass

    def on_close(self):
        self.waiters.remove(self)

# -*- coding: utf-8 -*-
from app.views.views_index import IndexHandler as index
from app.views.views_vclass import VClassHandler as vclass
from app.views.views_detail import DetailHandler as detail
from app.views.views_search import SearchHandler as search
from app.views.views_play import PlayHandler as play
from app.views.views_sitemap import SitemapHandler as sitemap
from app.views.views_dm import DMHandler as dm
from app.views.views_chatroom import ChatRoomHandler as chatroom
from app.views.views_msg import MsgHandler as msg
from app.views.views_gbook import GbookHandler as gbook

from app.views.views_login import LoginHandler as login
from app.views.views_logout import LogoutHandler as logout
from app.views.views_upload import UploadHandler as upload
from app.views.views_regist import RegistHandler as regist
from app.views.views_profile import ProfileHandler as profile

from app.views.views_manage import ManageHandler as manage
from app.views.views_insert import InsertHandler as insert
from app.views.views_edit import EditHandler as edit
from app.views.views_delete import DeleteHandler as delete
from app.views.views_checkcode import CheckCodeHandler as checkcode
from app.views.views_tags import TagsHandler as tags
from app.views.views_inblack import InBlackHandler as inblack
from sockjs.tornado import SockJSRouter

urls = [
           (r"/", index),
           (r"/index/", index),
           (r"/vclass/", vclass),
           (r"/detail/", detail),
           (r"/search/", search),
           (r"/play/", play),
           (r"/sitemap/", sitemap),
           (r"/msg/", msg),
           (r"/tags/", tags),
           (r"/dm/v3/", dm),
           (r"/gbook/", gbook),
           (r"/checkcode/", checkcode),
           (r"/inblack/", inblack),

           (r"/login/", login),
           (r"/logout/", logout),
           (r"/upload/", upload),
           (r"/regist/", regist),
           (r"/profile/", profile),

           (r"/manage/", manage),
           (r"/manage/edit/", edit),
           (r"/manage/insert/", insert),
           (r"/manage/delete/", delete),
       ] + SockJSRouter(chatroom, "/chatroom").urls

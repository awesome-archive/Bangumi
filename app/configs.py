# -*- coding: utf-8 -*-
import os  # 文件目录操作模块
from app.ui.ui_page import ManagePageUI, TagsPageUI, VClassPageUI, SearchPageUI

root_path = os.path.dirname(__file__)

configs = dict(
    debug=True,
    template_path=os.path.join(root_path, "templates"),
    static_path=os.path.join(root_path, "static"),
    xsrf_cookies=True,
    cookie_secret='84a7773b8a6546378b000d401c7989ed',
    ui_modules=dict(
        manage_page=ManagePageUI,
        tags_page=TagsPageUI,
        vclass_page=VClassPageUI,
        search_page=SearchPageUI,
    )
)

mysql_configs = dict(
    db_host="127.0.0.1",
    db_port=3306,
    db_name="",
    db_user="",
    db_pwd=""
)

redis_configs = dict(
    host="localhost",
    password="",
    port=6379,
    db=0
)

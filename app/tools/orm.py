# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.configs import mysql_configs


class DBConnetor:
    @classmethod
    def db(cls):
        link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8".format(
            **mysql_configs
        )

        engine = create_engine(
            link,
            encoding="utf-8",
            echo=False,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': "utf8"}
        )

        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )

        return Session()

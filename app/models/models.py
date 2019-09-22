# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BIGINT, TEXT, TINYINT, LONGTEXT
from werkzeug.security import check_password_hash

Base = declarative_base()
metadata = Base.metadata


class Video(Base):
    __tablename__ = "video"
    id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    logo = Column(VARCHAR(255), nullable=False)
    links = Column(LONGTEXT, nullable=False)
    actors = Column(TEXT, nullable=False)
    tags = Column(VARCHAR(255), nullable=False)
    director = Column(TEXT, nullable=False)
    area = Column(VARCHAR(255), nullable=False)
    language = Column(VARCHAR(255), nullable=False)
    year = Column(VARCHAR(255), nullable=False)
    status = Column(VARCHAR(255), nullable=False)
    hot = Column(BIGINT, nullable=False, default=0)
    desc = Column(TEXT, nullable=False)
    vclass = Column(VARCHAR(255), nullable=False)
    createdAt = Column(DATETIME, nullable=False)
    updatedAt = Column(DATETIME, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(20), nullable=False, unique=True)
    pwd = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    phone = Column(VARCHAR(11), nullable=False, unique=True)
    sex = Column(TINYINT, nullable=True)
    xingzuo = Column(TINYINT, nullable=True)
    face = Column(VARCHAR(100), nullable=True)
    info = Column(VARCHAR(600), nullable=True)
    createdAt = Column(DATETIME, nullable=False)
    updatedAt = Column(DATETIME, nullable=False)

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


class Black(Base):
    __tablename__ = "black"
    id = Column(INTEGER, autoincrement=True, primary_key=True)
    ipaddr = Column(VARCHAR(255), nullable=False, unique=True)
    createdAt = Column(DATETIME, nullable=False)


class Gbook(Base):
    __tablename__ = "gbook"
    id = Column(BIGINT, primary_key=True)
    user = Column(VARCHAR(255), nullable=False)
    ipaddr = Column(VARCHAR(255), nullable=False)
    content = Column(TEXT)
    createdAt = Column(DATETIME, nullable=False)


class Msg(Base):
    __tablename__ = "msg"
    id = Column(BIGINT, primary_key=True)
    vid = Column(INTEGER, nullable=False)
    vsb = Column(VARCHAR(255), nullable=False)
    ipaddr = Column(VARCHAR(255), nullable=False)
    content = Column(TEXT)
    createdAt = Column(DATETIME, nullable=False)


if __name__ == "__main__":
    from sqlalchemy import create_engine

    mysql_configs = dict(
        db_host="127.0.0.1",
        db_port=3306,
        db_name="",
        db_user="",
        db_pwd=""
    )

    link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
        **mysql_configs
    )

    engine = create_engine(
        link,
        encoding="utf-8",
        echo=True
    )

    metadata.create_all(engine)

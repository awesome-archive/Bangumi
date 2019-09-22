# -*- coding: utf-8 -*-
import datetime
from app.models.models import User, Video, Msg, Gbook, Black
from app.tools.orm import DBConnetor
from werkzeug.security import generate_password_hash
from sqlalchemy import and_


class Database:
    @staticmethod
    def datenow():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def user_unique(data, method=1):
        session = DBConnetor.db()
        user = None
        try:
            model = session.query(User)
            if method == 1:
                user = model.filter_by(name=data).first()
            if method == 2:
                user = model.filter_by(email=data).first()
            if method == 3:
                user = model.filter_by(phone=data).first()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        if user:
            return True
        else:
            return False

    @staticmethod
    def delete_video(id):
        session = DBConnetor.db()
        try:
            session.query(Video).filter_by(id=int(id)).delete(synchronize_session=False)
        except:
            return False
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def get_videos():
        session = DBConnetor.db()
        videos = None
        try:
            videos = session.query(Video).order_by(Video.createdAt.desc())
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return videos

    @staticmethod
    def get_video(id):
        session = DBConnetor.db()
        video = None
        try:
            video = session.query(Video).filter_by(id=id).first()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return video

    @staticmethod
    def get_hot_videos(vclass):
        session = DBConnetor.db()
        videos = None
        try:
            videos = session.query(Video).filter_by(vclass=vclass).order_by(Video.hot.desc()).limit(6)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return videos

    @staticmethod
    def get_vclass_tag_videos(vclass, tag):
        session = DBConnetor.db()
        videos = None
        try:
            videos = session.query(Video).filter(
                and_(Video.vclass == vclass, Video.tags.like("%{}%".format(tag)))).order_by(Video.updatedAt.desc())
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return videos

    @staticmethod
    def get_vclass_videos(vclass):
        session = DBConnetor.db()
        videos = None
        try:
            videos = session.query(Video).filter_by(vclass=vclass).order_by(Video.updatedAt.desc())
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return videos

    @staticmethod
    def query_videos(query):
        session = DBConnetor.db()
        videos = None
        try:
            videos = session.query(Video).filter(Video.name.like('%{}%'.format(query))).order_by(
                Video.updatedAt.desc())
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return videos

    @staticmethod
    def add_hot(id):
        session = DBConnetor.db()
        try:
            video = session.query(Video).filter_by(id=id).first()
            session.query(Video).filter(Video.id == int(id)).update({"hot": video.hot + 1})
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def update_video(form):
        session = DBConnetor.db()
        try:
            session.query(Video).filter(Video.id == int(form.data["id"])).update({
                "name": form.data["name"],
                "nick": form.data["nick"],
                "logo": form.data["logo"],
                "actors": form.data["actors"],
                "tags": form.data["tags"],
                "links": form.data["links"],
                "director": form.data["director"],
                "area": form.data["area"],
                "language": form.data["language"],
                "year": form.data["year"],
                "status": form.data["status"],
                "writer": form.data["writer"],
                "desc": form.data["desc"],
                "type": form.data["type"],
                "updatedAt": Database.datenow()
            })
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def update_video_2(id, video):
        session = DBConnetor.db()
        try:
            session.query(Video).filter(Video.id == id).update({
                "links": video["links"],
                "status": video["status"],
                "updatedAt": Database.datenow()
            })
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def create_video(form):
        session = DBConnetor.db()
        try:
            video = Video(
                name=form.data["name"],
                logo=form.data["logo"],
                links=form.data["links"],
                actors=form.data["actors"],
                tags=form.data["tags"],
                director=form.data["director"],
                area=form.data["area"],
                language=form.data["language"],
                year=form.data["year"],
                status=form.data["status"],
                desc=form.data["desc"],
                vclass=form.data["vclass"],
                createdAt=Database.datenow(),
                updatedAt=Database.datenow(),
            )
            session.add(video)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def create_video_2(video):
        session = DBConnetor.db()
        try:
            video_one = Video(
                name=video["name"],
                logo=video["logo"],
                links=video["links"],
                actors=video["actors"],
                tags=video["tags"],
                director=video["director"],
                area=video["area"],
                language=video["language"],
                year=video["year"],
                status=video["status"],
                desc=video["desc"],
                vclass=video["vclass"],
                createdAt=Database.datenow(),
                updatedAt=Database.datenow(),
            )
            session.add(video_one)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def create_regist_user(form):
        session = DBConnetor.db()
        try:
            user = User(
                name=form.data["name"],
                pwd=generate_password_hash(form.data["pwd"]),
                email=form.data["email"],
                phone=form.data["phone"],
                sex=None,
                xingzuo=None,
                face=None,
                info=None,
                createdAt=Database.datenow(),
                updatedAt=Database.datenow()
            )
            session.add(user)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def check_login(name, pwd):
        session = DBConnetor.db()
        result = False
        try:
            user = session.query(User).filter_by(name=name).first()
            if user:
                if user.check_pwd(pwd):
                    result = True
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return result

    @staticmethod
    def save_user(form):
        session = DBConnetor.db()
        try:
            session.query(User).filter_by(id=int(form.data["id"])).update({
                "sex": int(form.data["sex"]),
                "xingzuo": int(form.data["xingzuo"]),
                "face": form.data["face"],
                "info": form.data["info"],
                "updatedAt": Database.datenow()
            })
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def get_user(name):
        session = DBConnetor.db()
        user = None
        try:
            user = session.query(User).filter_by(name=name).first()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return user

    @staticmethod
    def create_msg(vid, vsb, content, ipaddr):
        session = DBConnetor.db()
        try:
            msg = Msg(
                vid=vid,
                vsb=vsb,
                ipaddr=ipaddr,
                content=content,
                createdAt=Database.datenow(),
            )
            session.add(msg)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    @staticmethod
    def get_msg(vid):
        session = DBConnetor.db()
        msgs = None
        try:
            msgs = session.query(Msg).filter_by(vid=vid).order_by(Msg.createdAt).limit(200).all()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return msgs

    @staticmethod
    def get_gbook_for_ip(ipaddr):
        session = DBConnetor.db()
        gbook = None
        try:
            gbook = session.query(Gbook).filter(Gbook.ipaddr.like('%{}%'.format(ipaddr))).order_by(
                Gbook.createdAt.desc()).limit(3).all()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return gbook

    @staticmethod
    def delete_gbook(ipaddr):
        session = DBConnetor.db()
        try:
            session.query(Gbook).filter_by(ipaddr=ipaddr).delete(synchronize_session=False)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    @staticmethod
    def get_msg_for_ip(ipaddr):
        session = DBConnetor.db()
        msgs = None
        try:
            msgs = session.query(Msg).filter(Msg.ipaddr.like('%{}%'.format(ipaddr))).order_by(
                Msg.createdAt.desc()).limit(5).all()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return msgs

    @staticmethod
    def get_black():
        session = DBConnetor.db()
        blacks = None
        try:
            blacks = session.query(Black).all()
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return blacks

    @staticmethod
    def create_black(ipaddr):
        session = DBConnetor.db()
        try:
            black = Black(
                ipaddr=ipaddr,
                createdAt=Database.datenow(),
            )
            session.add(black)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

    @staticmethod
    def create_gbook(form, ipaddr):
        session = DBConnetor.db()
        try:
            book = Gbook(
                user=form.data['name'],
                content=form.data['content'],
                ipaddr=ipaddr,
                createdAt=Database.datenow(),
            )
            session.add(book)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return True

# -*- coding: utf-8 -*-
container = {}


class Session:
    def __init__(self, handler):
        self.handler = handler
        self.random_str = None

    def __generate_random_str(self):
        import hashlib
        import time
        obj = hashlib.md5()
        obj.update(bytes(str(time.time()), encoding='utf-8'))
        random_str = obj.hexdigest()
        return random_str

    def __setitem__(self, key, value):
        if not self.random_str:
            random_str = self.handler.get_secure_cookie('random_client_num')
            if not random_str:
                random_str = self.__generate_random_str()
                container[random_str] = {}
            else:
                if random_str in container.keys():
                    pass
                else:
                    random_str = self.__generate_random_str()
                    container[random_str] = {}
            self.random_str = random_str
        container[self.random_str][key] = value
        self.handler.set_secure_cookie('random_client_num', self.random_str)

    def __getitem__(self, key):
        random_str = str(self.handler.get_secure_cookie('random_client_num'), encoding='utf-8')
        if not random_str:
            return None
        user_info_dict = container.get(random_str, None)
        if not user_info_dict:
            return None
        val = user_info_dict.get(key, None)
        return val

# -*- coding: utf-8 -*-
import redis
from app.configs import redis_configs

pool = redis.ConnectionPool(**redis_configs)
rd = redis.Redis(connection_pool=pool)

from .base import *

if MODERATION_PANEL_ENV == "prod":
    from .prod import *

elif MODERATION_PANEL_ENV == "prodpp":
    from .prodpp import *

elif MODERATION_PANEL_ENV == "pp":
    from .pp import *

elif MODERATION_PANEL_ENV == "dev":
    from .dev import *


from mongoengine import connection

for alias, conn_settings in MONGODB_DATABASES.items():
    connection.register_connection(alias, **conn_settings)

# import redis
# from rediscluster import RedisCluster
# from rediscluster.connection import ClusterConnectionPool
#
#
# class RedisConnection(object):
#     startup_nodes = [{"host": REDIS_CONFIG["host"], "port": REDIS_CONFIG["port"]}]
#
#     if PLATO_ADMIN_ENV not in ["prod", "prodpp"]:
#         connection_pool = redis.ConnectionPool(host=REDIS_CONFIG["host"],
#             port=REDIS_CONFIG["port"], db=REDIS_CONFIG["db"])
#     else:
#         connection_pool = ClusterConnectionPool(startup_nodes=startup_nodes,
#             skip_full_coverage_check=True)
#
# REDIS_CONNECTION_POOL = RedisConnection.connection_pool
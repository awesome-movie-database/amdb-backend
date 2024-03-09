from faststream.redis import RedisRoute, RedisRouter

from .export_and_send_my_ratings import export_and_send_my_ratings


router = RedisRouter(
    handlers=[
        RedisRoute(export_and_send_my_ratings, list="tasks"),
    ],
)

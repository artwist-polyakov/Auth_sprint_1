import redis
from configs.test_settings import settings
from utils.wrappers import backoff, ping_service


@backoff()
def get_redis_client(host, port) -> redis.StrictRedis:
    redis_cli = redis.StrictRedis(
        host=host,
        port=port,
        decode_responses=True
    )
    return redis_cli


if __name__ == '__main__':
    service = get_redis_client(settings.redis_host, settings.redis_port)
    ping_service(service, "Redis")

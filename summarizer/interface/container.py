import boto3
from dependency_injector import containers, providers
from redis import Redis

from summarizer.infrastructure.redis_listener import RedisListener
from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoDataRepository)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis = providers.Singleton(Redis, host=config.redis_host, port=config.redis_port)
    event_listener = providers.Factory(RedisListener, redis=redis, key=config.redis_key)

    dynamodb = providers.Singleton(
        boto3.resource, "dynamodb", endpoint_url=config.dynamodb_url
    )
    s3 = providers.Singleton(
        boto3.client, "s3", aws_access_key_id = config.aws_access_key_id, aws_secret_access_key = config.aws_secret_access_key
    )
    
    feature_repository = providers.Singleton(FeatureRepository, dynamodb)
    video_repository = providers.Singleton(
        VideoDataRepository, dynamodb, algorithm=config.detector_model
    )

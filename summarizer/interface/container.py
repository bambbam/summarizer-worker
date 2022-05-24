import boto3
from dependency_injector import containers, providers
from redis import Redis

from summarizer.infrastructure.redis_listener import RedisListener
from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoDataRepository)
from summarizer.infrastructure.repository.s3_repository import S3Repository


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
    s3_repository = providers.Singleton(
        S3Repository, s3, config.aws_s3_bucket_name,
    )
    feature_repository = providers.Singleton(FeatureRepository, dynamodb)
    video_repository = providers.Singleton(
        VideoDataRepository, dynamodb, algorithm=config.detector_model
    )

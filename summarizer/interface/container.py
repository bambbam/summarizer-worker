import pika
import boto3
from dependency_injector import containers, providers
from redis import Redis
from ..infrastructure.rabbit_listener import RabbitListener

from summarizer.infrastructure.redis_listener import RedisListener
from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoDataRepository)
from summarizer.infrastructure.repository.s3_repository import S3Repository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    rabbit_parameter = providers.Singleton(pika.ConnectionParameters, "localhost")
    rabbit = providers.Singleton(pika.BlockingConnection, rabbit_parameter)
    event_listener = providers.Factory(RabbitListener, rabbit, config.rabbit_key)
    
    dynamodb = providers.Singleton(
        boto3.resource, "dynamodb", aws_access_key_id=config.dynamodb_aws_access_key_id,  aws_secret_access_key=config.dynamodb_aws_secret_access_key, endpoint_url=config.dynamodb_url
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

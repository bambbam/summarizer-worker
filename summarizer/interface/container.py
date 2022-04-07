from msilib.schema import Feature
from dependency_injector import containers, providers
from redis import Redis
from summarizer.infrastructure.redis_listener import RedisListener
import boto3
from summarizer.infrastructure.repository import FeatureRepository, VideoRepository, video_repository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    redis = providers.Singleton(Redis, host=config.redis_host, port=config.redis_port)

    redis_listener = providers.Factory(RedisListener, redis=redis, key=config.redis_key)
    
    dynamodb = boto3.resource('dynamodb', endpoint_url=config.dynamodb_url)
    
    feature_repository = providers.Factory(FeatureRepository, dynamodb.Table['Feature'])
    video_repository = providers.Factory(VideoRepository, dynamodb.Table['Video'])
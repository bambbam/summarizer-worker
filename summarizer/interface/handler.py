import json

from dependency_injector import wiring

from summarizer.infrastructure.repository.video_repository import \
    VideoRepository
from summarizer.interface.container import Container
from summarizer.service.command import (COMMAND_HANDLER, Command,
                                        ExtractFeature, extract_feature)


@wiring.inject
def handle_message(
    message: str,
    video_repo=wiring.Provide[Container.video_repository],
    feature_repo=wiring.Provide[Container.feature_repository],
):
    message = json.loads(message)
    cls, handler = COMMAND_HANDLER[message["type"]]
    message = cls(**message)
    handler(message, feature_repo=feature_repo, video_repo=video_repo)

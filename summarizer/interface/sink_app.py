import time

from summarizer.interface import handler
from summarizer.interface.container import Container
from summarizer.interface.settings import Settings
from summarizer.log.logger import MyLogger, log

def callback(ch, method, properties, body):
    handler.handle_message(body.decode())
    ch.basic_ack(delivery_tag = method.delivery_tag)


class SinkApp:
    def __init__(self, settings: Settings):
        cont = Container()
        cont.config.from_pydantic(settings)
        cont.wire(packages=[handler])
        self.event_listener = cont.event_listener()

    def run(self):
        self.run_once()

    @log(MyLogger())
    def run_once(self):
        consume = self.event_listener.get()
        consume(callback)
        self.event_listener.rabbit.start_consuming()

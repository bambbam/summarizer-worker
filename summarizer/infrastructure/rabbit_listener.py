from summarizer.infrastructure.event_listener import EventListener


class RabbitListener(EventListener):
    def __init__(self,  rabbit, key):
        self.rabbit = rabbit.channel()
        self.key = key

    def size(self):
        raise NotImplementedError

    def get(self):
        def consume(callback):
            self.rabbit.basic_consume(queue=self.key,
                                      on_message_callback=callback)
        return consume

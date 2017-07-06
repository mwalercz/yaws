import json


ENCODING = 'utf8'


class JsonSerializer(object):
    def serialize(self, message):
        return json.dumps(message).encode(ENCODING)


class JsonDeserializer(object):
    def deserialize(self, message):
        return json.loads(message.decode(ENCODING))

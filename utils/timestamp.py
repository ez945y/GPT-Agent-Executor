import datetime

class TimestampGenerator:
    _timestamp = None

    @classmethod
    async def generate_timestamp(cls):
        cls._timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return cls._timestamp

    @classmethod
    def get_timestamp(cls):
        return cls._timestamp
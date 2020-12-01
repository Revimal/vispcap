class SkelSingleton:
    _instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
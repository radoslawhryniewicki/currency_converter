import logging

# def setup_logger():
#     logger = getLogger(__name__)
#     logger.setLevel(INFO)

#     formatter = Formatter("%(levelname)s - %(message)s")

#     console_handler = StreamHandler()
#     console_handler.setFormatter(formatter)

#     logger.addHandler(console_handler)

#     return logger


# logger = setup_logger()


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_info(self, msg):
        self.logger.info(msg)

    def log_error(self, msg):
        self.logger.error(msg)


logger = Logger()

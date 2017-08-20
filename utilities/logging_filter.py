import logging
import os


class CustomFilter(logging.Filter):

    def __init__(self):
        settings = os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "configuration.settings")
        self.environment = settings.split('.')[-1]
        super(CustomFilter, self).__init__()

    def filter(self, record):
        record.environment = self.environment
        return True

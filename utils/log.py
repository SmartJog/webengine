# Logging system for webengine.

import logging
import logging.handlers
from django.conf import settings

logger = logging.getLogger("webengine")
logger.setLevel(logging.DEBUG)
if settings.LOG_TO_OUTPUT:
    handler = logging.StreamHandler()
else:
    handler = logging.FileHandler(settings.LOG_FILENAME)
FORMAT = settings.LOG_FORMAT
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Logging system for webengine.

import logging
import logging.handlers
from django.conf import settings

logger = logging.getLogger('webengine')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(settings.LOG_FILENAME)
FORMAT = settings.LOG_FORMAT
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Settings for Exporter module.

# Import project settings
from django.conf.settings import *

# Exportable modules.
# Modules must be a valid python module, in the import path.
EXPORT_MODULES = ('sys', 'os')

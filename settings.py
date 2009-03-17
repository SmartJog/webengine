# Django settings for rxtxmanager project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('Thomas Meson', 'thomas.meson@smartjog.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE     = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME       = 'webengine'             # Or path to database file if using sqlite3.
DATABASE_USER       = 'webengine'             # Not used with sqlite3.
DATABASE_PASSWORD   = 'webengine'         # Not used with sqlite3.
DATABASE_HOST       = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT       = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3=1gkvcqd+4v5xb)!m6b9%s*to%6dye%nk6*^-w5unj&^e3a+b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    # DO NOT use the following loader, it does not make what we want.
    #'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'webengine.urls'

TEMPLATE_DIRS = (
    '/usr/share/webengine/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'webengine.utils',
    # DO NOT put modules here, for one good reason:
    # When looking for templates, django use this tuple and tries
    # to get templates for the templates directory of each installed apps.
    # But this is just stupid, cause if you try to get a 'index.html' template,
    # the first matching template file will be use.
    # Following this, EACH template must be unique, which is totally 
    # impossible with a lot of modules having, for example an 'index.html'
    # But, even if you try to put modules here, the TEMPLATE_LOADER app_directories has been disabled.
)

# The login url.
LOGIN_URL = '/auth/login/'
# If 'next' isn't provided, always redirect to site root.
LOGIN_REDIRECT_URL = '/'

# Default Output mode.
# Choose the default mode in which pages will be rendered.
# Possible values are:
#  - xml
#  - html
#  - json
#  - soap
# Default is html
DEFAULT_OUTPUT_MODE = 'html'
# The given output mode must be contained into ACCEPTABLE_OUTPUT_MODES
ACCEPTABLE_OUTPUT_MODES = {
        'html' : 'text/html',
        'xml'  : 'text/xml',
        'json' : 'application/json',
        'soap' : 'application/soap+xml'}

# Default URL.
DEFAULT_URL = '/extract/'

# Webengine profile
PROFILE = 'tvrbox'

# Logging infos.
LOG_FILENAME = '/tmp/webengine.log'
LOG_FORMAT = "%(asctime)s:%(levelname)s: %(message)s"

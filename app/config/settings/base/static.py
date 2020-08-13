from .paths import *

# Static
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

from settings import *

DEBUG = False

from bundle_config import config
MEDIA_ROOT = config['core']['data_directory']

from .common import *
from .custom import *
from .third_party import *

INSTALLED_APPS += [
    *THIRD_PARTY_APPS,
    *CUSTOM_APPS,
]

MIDDLEWARE += [
    *THIRD_PARTY_MIDDLEWARE,
    *CUSTOM_MIDDLEWARE,
]

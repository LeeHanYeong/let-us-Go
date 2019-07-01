import re

from djangorestframework_camel_case.util import camelize_re, underscore_to_camel


def underscore_to_camelcase(value):
    return re.sub(camelize_re, underscore_to_camel, value)

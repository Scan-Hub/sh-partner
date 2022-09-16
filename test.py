import json
import traceback

from marshmallow import Schema, EXCLUDE, fields, validate

from lib.schema import URLField
from schemas.utils import MaxMinSchema, Phone


class Test(Schema):
    class Meta:
        unknown = EXCLUDE

    link = fields.URL(schemes={"http", "https", "ftp", "ftps", '', 'www'})

print(Test().validate({
    'link': 'w.com'
}))

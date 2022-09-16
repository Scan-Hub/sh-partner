# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

from marshmallow import Schema, EXCLUDE, fields, validate, validates, validates_schema, ValidationError
from pydash import get

from lib import NotBlank


class MaxMinSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    max = fields.Float(validate=validate.Range(min=0))
    min = fields.Float(validate=validate.Range(min=0))

    @validates_schema
    def _check_max_min(self, in_data, *args, **kwargs):
        if get(in_data, 'max') and get(in_data, 'max', 0) < get(in_data, 'min', 0):
            raise ValidationError('max must be greater min', 'max')


import phonenumbers


def phone_validation(_phone, code):
    try:
        if isinstance(_phone, str):
            _phone = _phone.replace(' ', '')
        x = phonenumbers.parse(_phone, code)
        return phonenumbers.is_valid_number(x)
    except:
        traceback.print_exc()
    return False


class Phone(Schema):
    class Meta:
        unknown = EXCLUDE

    number = fields.Str(required=True, validate=NotBlank())
    prefix = fields.Str(required=True, validate=NotBlank())
    code = fields.Str(required=True, validate=NotBlank())

    @validates_schema
    def validate_phone(self, in_data, *args, **kwargs):
        if not phone_validation(get(in_data, 'number'), get(in_data, 'code')):
            raise ValidationError('Not a valid phone number.', 'number')

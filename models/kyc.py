# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from enums.kyc import KYCStatus
from lib import DaoModel


class KYCDao(DaoModel):

    def __init__(self, *args, **kwargs):
        super(KYCDao, self).__init__(*args, **kwargs)

    def get_status(self, user_id):
        return self.find_one({'user_id': user_id})

    def approved(self, user_id):
        return get(self.get_status(user_id), 'status') == KYCStatus.APPROVED

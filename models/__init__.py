# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import DaoModel, AsyncDaoModel
from connect import connect_db, redis_cluster, asyncio_mongo

__models__ = ['PartnerModel', 'KYCModel']

from models.kyc import KYCDao

from models.user import PartnerDao

PartnerModel = PartnerDao(connect_db.db.partners, redis=redis_cluster, broker=Config.BROKER_URL,
                       project=Config.PROJECT)  # broker for write db with queue

KYCModel = KYCDao(connect_db.db.kyc_partners, redis=redis_cluster, broker=Config.BROKER_URL,
                  project=Config.PROJECT)

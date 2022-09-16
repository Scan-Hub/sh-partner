# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback


def str_to_tuple(query: str):
    try:
        return eval(query)
    except:
        traceback.print_exc()
        return tuple()


class IndicatorHelper:
    @staticmethod
    def Range(value, query):
        if value is None:
            value = 0

        if isinstance(query, str):
            query = str_to_tuple(query)
        if isinstance(value, (tuple, dict, list)):
            value = len(value)
        if not isinstance(value, (float, int)):
            value = float(value)

        return query[0] <= value <= query[1]

    @staticmethod
    def In(value, query: tuple):
        if isinstance(query, str):
            query = str_to_tuple(query)
        return value in query

    @staticmethod
    def Contain(value, query):
        if not value:
            return False
        query = str_to_tuple(query)
        if isinstance(query, (tuple, list)):
            query = query[0]

        if not isinstance(value, str):
            value = str(value)

        return value.find(query) != -1

